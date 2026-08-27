"""Run route A on the frozen independent v2 real-history panel."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from nvidia_survey.spec_prediction.agent_quantitative import (  # type: ignore[import-untyped]
    PredictorDefinition,
    QuantitativeModelConfig,
    backtest_hyperparameter_sensitivity,
    backtest_quantitative_model,
    build_quantitative_folds,
    forecast_quantitative_sensitivity,
)
from nvidia_survey.spec_prediction.dataset import (  # type: ignore[import-untyped]
    audit_research_dataset,
    load_research_dataset,
)
from nvidia_survey.spec_prediction.panel import (  # type: ignore[import-untyped]
    MetricSemantics,
)

DEMAND = PredictorDefinition(
    "ln_frontier_training_compute_flop",
    "ln(FLOP)",
    "difference",
)

SUPPLY_BY_METRIC: dict[str, PredictorDefinition] = {
    "transistor_count": PredictorDefinition(
        "logic_density_mtr_per_mm2", "MTr/mm2", "log-difference"
    ),
    "enabled_sm_count": PredictorDefinition(
        "logic_density_mtr_per_mm2", "MTr/mm2", "log-difference"
    ),
    "hbm_capacity": PredictorDefinition(
        "hbm_stack_capacity_gb", "GB/stack", "log-difference"
    ),
    "hbm_bandwidth": PredictorDefinition(
        "hbm_stack_bandwidth_gbs", "GB/s/stack", "log-difference"
    ),
    "scaleup_bandwidth": PredictorDefinition(
        "scaleup_link_bandwidth_gbs", "GB/s", "log-difference"
    ),
    "card_power": PredictorDefinition(
        "card_power_envelope_w", "W", "log-difference"
    ),
}


def parse_args() -> argparse.Namespace:
    """Parse the immutable panel and result destination.

    Returns
    -------
    argparse.Namespace
        Input and output paths.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("panel", type=Path)
    parser.add_argument("output", type=Path)
    return parser.parse_args()


def metric_index(labels: tuple[Any, ...]) -> dict[str, MetricSemantics]:
    """Resolve one exact semantics object per modeled metric."""

    index: dict[str, MetricSemantics] = {}
    for label in labels:
        current = index.get(label.semantics.metric_id)
        if current is not None and current.key != label.semantics.key:
            raise ValueError(
                f"metric has multiple semantics: {label.semantics.metric_id}"
            )
        index[label.semantics.metric_id] = label.semantics
    return index


def run_variant(
    *,
    dataset: Any,
    semantics: MetricSemantics,
    variant_id: str,
    predictors: tuple[PredictorDefinition, ...],
    config: QuantitativeModelConfig,
) -> dict[str, Any]:
    """Run one predeclared predictor variant through folds and forecast."""

    folds = build_quantitative_folds(
        dataset.events[:-1],
        dataset.observations,
        dataset.labels,
        predictors,
        semantics,
        product_by_generation=dataset.representative_products,
        config=config,
    )
    inventory = {
        "built_count": len(folds.folds),
        "rejected_count": len(folds.rejections),
        "rejections": [asdict(item) for item in folds.rejections],
    }
    if not folds.folds:
        return {
            "variant_id": variant_id,
            "role": (
                "pre_registered_primary"
                if variant_id == "mechanism-supply"
                else "reported_sensitivity"
            ),
            "predictors": [asdict(item) for item in predictors],
            "execution_status": "rejected",
            "execution_refusal_reasons": ["no-scoreable-rolling-origin-folds"],
            "fold_inventory": inventory,
            "backtest": None,
            "forecast": None,
        }
    backtest = backtest_quantitative_model(folds, config=config)
    forecast = forecast_quantitative_sensitivity(
        dataset.events,
        dataset.observations,
        dataset.labels,
        predictors,
        semantics,
        target_generation="feynman",
        product_by_generation=dataset.representative_products,
        backtest=backtest,
        evidence_audit_accepted=False,
        config=config,
    )
    return {
        "variant_id": variant_id,
        "role": (
            "pre_registered_primary"
            if variant_id == "mechanism-supply"
            else "reported_sensitivity"
        ),
        "predictors": [asdict(item) for item in predictors],
        "execution_status": "completed",
        "execution_refusal_reasons": [],
        "fold_inventory": inventory,
        "backtest": asdict(backtest),
        "forecast": asdict(forecast),
    }


def main() -> None:
    """Run all six exact outputs and three fixed predictor variants."""

    args = parse_args()
    dataset = load_research_dataset(args.panel)
    audit = audit_research_dataset(dataset)
    if not audit.claim_ready:
        raise RuntimeError(f"panel is not claim-ready: {audit.claim_blockers}")
    if dataset.events[-1].generation != "feynman":
        raise ValueError("latest event must be the answer-free Feynman target")
    metrics = metric_index(dataset.labels)
    config = QuantitativeModelConfig(
        posterior_draw_count=4096,
        predictor_prior_precision=4.0,
        annual_log_scale_floor=0.05,
        minimum_scored_folds=3,
        random_seed=20260827,
    )
    outputs: list[dict[str, Any]] = []
    sensitivities: list[dict[str, Any]] = []
    for metric_id in sorted(SUPPLY_BY_METRIC):
        metric_semantics = metrics[metric_id]
        supply = SUPPLY_BY_METRIC[metric_id]
        variants = (
            ("mechanism-supply", (supply,)),
            ("workload-demand", (DEMAND,)),
            ("demand-plus-supply", (DEMAND, supply)),
        )
        for variant_id, predictors in variants:
            outputs.append(
                {
                    "metric_id": metric_id,
                    "semantics_key": metric_semantics.key,
                    **run_variant(
                        dataset=dataset,
                        semantics=metric_semantics,
                        variant_id=variant_id,
                        predictors=predictors,
                        config=config,
                    ),
                }
            )
        primary_predictors = (supply,)
        primary_folds = build_quantitative_folds(
            dataset.events[:-1],
            dataset.observations,
            dataset.labels,
            primary_predictors,
            metric_semantics,
            product_by_generation=dataset.representative_products,
            config=config,
        )
        if primary_folds.folds:
            grid = backtest_hyperparameter_sensitivity(
                primary_folds,
                predictor_prior_precisions=(1.0, 4.0, 16.0),
                annual_log_scale_floors=(0.03, 0.05, 0.1),
                base_config=config,
            )
            serialized_grid = [asdict(item) for item in grid]
            sensitivity_status = "completed"
        else:
            serialized_grid = []
            sensitivity_status = "rejected-no-scoreable-folds"
        sensitivities.append(
            {
                "metric_id": metric_id,
                "variant_id": "mechanism-supply",
                "execution_status": sensitivity_status,
                "grid": serialized_grid,
            }
        )

    payload = {
        "schema_version": "nvidia-survey-real-quantitative-route-a.v1",
        "topic_id": dataset.topic_id,
        "dataset_checksum": dataset.source_checksum,
        "target_generation": "feynman",
        "observation_date": "2026-08-27",
        "model": {
            "response": "annualized log specification change",
            "likelihood": "Gaussian annualized growth with conjugate empirical-Bayes ridge",
            "predictive_distribution": "Student-t on log specification",
            "freeze_leads_months": list(config.lead_months),
            "strict_time_rule": "public_available_date < cutoff_date",
            "primary_variant_rule": (
                "one predeclared mechanism-specific supply predictor per output"
            ),
            "sensitivity_variants": ["workload-demand", "demand-plus-supply"],
        },
        "dataset_audit": audit.as_dict(),
        "outputs": outputs,
        "hyperparameter_sensitivity": sensitivities,
        "evidence_audit_accepted": False,
        "publication_claim_authorized": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
