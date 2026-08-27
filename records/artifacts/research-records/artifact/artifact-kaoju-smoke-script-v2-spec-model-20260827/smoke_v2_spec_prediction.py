"""Task-critical smoke check for the independent v2 specification model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from nvidia_survey.spec_prediction.agent_quantitative import (  # type: ignore[import-untyped]
    PredictorDefinition,
    QuantitativeModelConfig,
    build_quantitative_folds,
)
from nvidia_survey.spec_prediction.dataset import (  # type: ignore[import-untyped]
    audit_research_dataset,
    load_research_dataset,
)


def parse_args() -> argparse.Namespace:
    """Parse the frozen-panel path.

    Returns
    -------
    argparse.Namespace
        Parsed command-line arguments.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("panel", type=Path)
    return parser.parse_args()


def main() -> None:
    """Verify imports, panel integrity, answer exclusion, and fold construction."""

    args = parse_args()
    dataset = load_research_dataset(args.panel)
    audit = audit_research_dataset(dataset)
    if not audit.claim_ready:
        raise RuntimeError(f"panel audit failed: {audit.claim_blockers}")
    if any(label.generation == "feynman" for label in dataset.labels):
        raise RuntimeError("prospective Feynman answer leaked into historical labels")
    semantics = next(
        label.semantics
        for label in dataset.labels
        if label.semantics.metric_id == "transistor_count"
    )
    folds = build_quantitative_folds(
        dataset.events[:-1],
        dataset.observations,
        dataset.labels,
        (PredictorDefinition("ln_frontier_training_compute_flop", "ln(FLOP)"),),
        semantics,
        product_by_generation=dataset.representative_products,
        config=QuantitativeModelConfig(posterior_draw_count=128),
    )
    if not folds.folds:
        raise RuntimeError("no task-critical rolling-origin fold could be built")
    print(
        json.dumps(
            {
                "claim_ready": audit.claim_ready,
                "dataset_checksum": dataset.source_checksum,
                "feynman_label_count": 0,
                "scoreable_fold_count": len(folds.folds),
                "status": "passed",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
