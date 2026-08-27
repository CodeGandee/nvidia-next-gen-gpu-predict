"""Run the pinned, answer-free three-route Feynman prediction trial.

This wrapper is the durable execution boundary for the independent v2 survey.
It verifies the exact historical panel, rejects target-label leakage, invokes the
three predeclared model runners in the current Pixi Python environment, and
writes an integrity manifest for the resulting JSON files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from nvidia_survey.spec_prediction.dataset import (  # type: ignore[import-untyped]
    audit_research_dataset,
    load_research_dataset,
)

TOPIC_ID = "nvidia-next-gen-dc-gpu-v2"
TARGET_GENERATION = "feynman"
EXPECTED_PANEL_SHA256 = "1bed7326efaae56c85c5b4a0c9fa63bf5c2907bf1ad25126766d3dbd10e579e3"
SEED = 20260827
BACKTEST_DRAWS = 4_000
FORECAST_DRAWS = 20_000
ENGINEERING_DRAWS = 1_024


def parse_args() -> argparse.Namespace:
    """Parse the pinned panel and new immutable output directory.

    Returns
    -------
    argparse.Namespace
        Input panel and output-directory paths.
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("panel", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--repository-root", type=Path, required=True)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    """Return one lowercase hexadecimal SHA-256 digest.

    Parameters
    ----------
    path
        File to hash.

    Returns
    -------
    str
        Hexadecimal digest without a prefix.
    """

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    """Load one JSON object or reject a non-object payload.

    Parameters
    ----------
    path
        JSON file to load.

    Returns
    -------
    dict[str, Any]
        Parsed top-level object.
    """

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected a JSON object: {path}")
    return value


def run_child(command: list[str], repository_root: Path) -> dict[str, object]:
    """Run one fixed child command and return bounded execution metadata.

    Parameters
    ----------
    command
        Exact command vector.
    repository_root
        Working directory for the child process.

    Returns
    -------
    dict[str, object]
        Command, timing, status, and bounded standard streams.
    """

    started = time.perf_counter()
    completed = subprocess.run(
        command,
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
    )
    elapsed = time.perf_counter() - started
    record: dict[str, object] = {
        "command": command,
        "returncode": completed.returncode,
        "elapsed_seconds": elapsed,
        "stdout": completed.stdout[-20_000:],
        "stderr": completed.stderr[-20_000:],
        "streams_truncated_to_last_characters": 20_000,
    }
    if completed.returncode != 0:
        raise RuntimeError(json.dumps(record, ensure_ascii=False, sort_keys=True))
    return record


def _source_hashes(repository_root: Path) -> dict[str, str]:
    """Hash every repo-owned Python source affecting the three-route run."""

    paths = [
        *sorted((repository_root / "src/nvidia_survey/spec_prediction").glob("*.py")),
        repository_root / "scripts/run_v2_real_quantitative_model.py",
        repository_root / "scripts/run_v2_evidence_calibrated_bayesian_model.py",
        repository_root / "scripts/run_v2_engineering_robustness.py",
        Path(__file__).resolve(),
    ]
    return {str(path.relative_to(repository_root)): sha256_file(path) for path in paths}


def _verify_answer_free_panel(panel: Path) -> tuple[dict[str, Any], dict[str, object]]:
    """Verify identity, structural readiness, and absence of target answers."""

    panel_digest = sha256_file(panel)
    if panel_digest != EXPECTED_PANEL_SHA256:
        raise ValueError(
            "panel checksum differs from the reviewed trial input: "
            f"expected {EXPECTED_PANEL_SHA256}, observed {panel_digest}"
        )
    raw = read_json(panel)
    dataset = load_research_dataset(panel)
    audit = audit_research_dataset(dataset)
    if dataset.topic_id != TOPIC_ID:
        raise ValueError(f"unexpected topic id: {dataset.topic_id}")
    if not audit.claim_ready:
        raise ValueError(f"panel is not claim-ready: {audit.claim_blockers}")
    events = raw.get("events")
    labels = raw.get("labels")
    feature_labels = raw.get("feature_labels")
    if not isinstance(events, list) or not isinstance(labels, list):
        raise TypeError("panel events and labels must be lists")
    if not isinstance(feature_labels, list):
        raise TypeError("panel feature_labels must be a list")
    target_events = [row for row in events if row.get("generation") == TARGET_GENERATION]
    target_labels = [row for row in labels if row.get("generation") == TARGET_GENERATION]
    target_feature_labels = [
        row for row in feature_labels if row.get("generation") == TARGET_GENERATION
    ]
    if len(target_events) != 1:
        raise ValueError("panel must contain exactly one answer-free Feynman event")
    if target_labels or target_feature_labels:
        raise ValueError("Feynman target labels are forbidden in the trial panel")
    return raw, {
        "dataset_audit": audit.as_dict(),
        "target_event_count": len(target_events),
        "target_numeric_label_count": len(target_labels),
        "target_feature_label_count": len(target_feature_labels),
        "answer_free": True,
    }


def _verify_outputs(
    panel_digest: str,
    route_a: dict[str, Any],
    route_b: dict[str, Any],
    route_c: dict[str, Any],
) -> dict[str, object]:
    """Check cross-route identity and count the frozen Route-C conditions."""

    expected_dataset_checksum = f"sha256:{panel_digest}"
    if route_a.get("dataset_checksum") != expected_dataset_checksum:
        raise ValueError("Route A dataset checksum does not match the trial panel")
    if route_b.get("dataset_checksum") != expected_dataset_checksum:
        raise ValueError("Route B dataset checksum does not match the trial panel")
    if route_a.get("publication_claim_authorized") is not False:
        raise ValueError("Route A must not self-authorize a publication claim")
    if route_b.get("publication_claim_authorized") is not False:
        raise ValueError("Route B must not self-authorize a publication claim")
    vintages = route_c.get("vintages")
    if not isinstance(vintages, list):
        raise TypeError("Route C vintages must be a list")
    condition_count = 0
    for vintage in vintages:
        if not isinstance(vintage, dict):
            raise TypeError("Route C vintage must be an object")
        conditions = vintage.get("conditional_runs")
        if not isinstance(conditions, list):
            raise TypeError("Route C conditional_runs must be a list")
        condition_count += len(conditions)
    if condition_count != 75:
        raise ValueError(f"Route C must execute 75 conditions, observed {condition_count}")
    return {
        "route_a_dataset_match": True,
        "route_b_dataset_match": True,
        "route_c_condition_count": condition_count,
        "all_route_checks_passed": True,
    }


def main() -> None:
    """Execute the reviewed three-route trial and write an integrity manifest."""

    args = parse_args()
    repository_root = args.repository_root.resolve()
    if not (repository_root / "pyproject.toml").is_file():
        raise ValueError("repository root must contain pyproject.toml")
    if not (repository_root / "pixi.lock").is_file():
        raise ValueError("repository root must contain pixi.lock")
    panel = args.panel.resolve()
    output_dir = args.output_dir.resolve()
    raw_panel, leakage_audit = _verify_answer_free_panel(panel)
    output_dir.mkdir(parents=True, exist_ok=False)

    route_paths = {
        "route_a": output_dir / "route-a.json",
        "route_b": output_dir / "route-b.json",
        "route_c": output_dir / "route-c.json",
    }
    child_runs = {
        "route_a": run_child(
            [
                sys.executable,
                str(repository_root / "scripts/run_v2_real_quantitative_model.py"),
                str(panel),
                str(route_paths["route_a"]),
            ],
            repository_root,
        ),
        "route_b": run_child(
            [
                sys.executable,
                str(repository_root / "scripts/run_v2_evidence_calibrated_bayesian_model.py"),
                str(panel),
                str(route_paths["route_b"]),
                "--backtest-draws",
                str(BACKTEST_DRAWS),
                "--forecast-draws",
                str(FORECAST_DRAWS),
                "--seed",
                str(SEED),
            ],
            repository_root,
        ),
        "route_c": run_child(
            [
                sys.executable,
                str(repository_root / "scripts/run_v2_engineering_robustness.py"),
                str(route_paths["route_c"]),
                "--draws",
                str(ENGINEERING_DRAWS),
                "--seed",
                str(SEED),
            ],
            repository_root,
        ),
    }
    route_payloads = {name: read_json(path) for name, path in route_paths.items()}
    output_checks = _verify_outputs(
        EXPECTED_PANEL_SHA256,
        route_payloads["route_a"],
        route_payloads["route_b"],
        route_payloads["route_c"],
    )
    source_registry = raw_panel.get("source_registry")
    if not isinstance(source_registry, list):
        raise TypeError("panel source_registry must be a list")
    manifest: dict[str, object] = {
        "schema_version": "nvidia-survey-final-three-route-trial-manifest.v1",
        "topic_id": TOPIC_ID,
        "target_generation": TARGET_GENERATION,
        "trial_purpose": "prospective-forecast-method-trial",
        "verification_depth": "executed",
        "execution_fidelity": "reimplemented",
        "input_basis": {
            "panel_path": str(panel),
            "panel_sha256": EXPECTED_PANEL_SHA256,
            "panel_schema_version": raw_panel.get("schema_version"),
            "source_lineage": [
                {
                    "source_ref": row.get("source_ref"),
                    "content_sha256": row.get("content_sha256"),
                    "evidence_status": row.get("evidence_status"),
                }
                for row in source_registry
                if isinstance(row, dict)
            ],
        },
        "leakage_audit": leakage_audit,
        "controls": {
            "seed": SEED,
            "route_a_posterior_draws": 4_096,
            "route_b_backtest_draws": BACKTEST_DRAWS,
            "route_b_forecast_draws": FORECAST_DRAWS,
            "route_c_draws_per_condition": ENGINEERING_DRAWS,
            "route_c_expected_conditions": 75,
        },
        "environment": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "pixi_lock_sha256": sha256_file(repository_root / "pixi.lock"),
        },
        "source_hashes": _source_hashes(repository_root),
        "child_runs": child_runs,
        "output_checks": output_checks,
        "outputs": {
            name: {
                "path": str(path),
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
                "schema_version": route_payloads[name].get("schema_version"),
            }
            for name, path in route_paths.items()
        },
        "limitations": [
            (
                "This is a bounded prospective model trial, not a reproduction of "
                "NVIDIA's private process."
            ),
            (
                "Route A may reject publication centers when the historical sample "
                "is not identifiable."
            ),
            (
                "Route B contains explicit expert priors and only conditions on "
                "scope-equivalent disclosures."
            ),
            (
                "Route C intervals are conditional engineering envelopes, not "
                "calibrated confidence intervals."
            ),
        ],
        "terminal_status": "complete",
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"manifest": str(manifest_path), **output_checks}, sort_keys=True))


if __name__ == "__main__":
    main()
