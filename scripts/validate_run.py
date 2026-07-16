#!/usr/bin/env python3
"""Validate a Pickfolio run package."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from pathlib import Path


MODES = {"select", "position", "full", "refresh", "review"}
RETAIN_LEVELS = {"minimal", "standard", "audit"}
SELECTION_STATUSES = {"not_applicable", "draft", "reviewed", "frozen"}
BOTTLENECK_STATUSES = {"not_applicable", "pending", "draft", "reviewed", "complete"}
POSITION_STATUSES = {"not_applicable", "blocked", "draft", "reviewed", "approved"}
MANDATE_STATUSES = {"draft", "confirmed"}
DATA_STATUSES = {"pending", "ready", "partial", "blocked"}
REQUIRED_SOURCE_FIELDS = {
    "source_id",
    "provider",
    "field_group",
    "symbol_scope",
    "status",
    "as_of_date",
    "retrieved_at",
    "artifact_path",
    "limitation",
    "error",
}
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")


def load_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read {path}: {exc}") from exc


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.is_file():
        raise SystemExit(f"Missing manifest.json: {run_dir}")
    manifest = load_json(manifest_path)

    if manifest.get("schema_version") != "0.1":
        errors.append("schema_version must be '0.1'")
    run = manifest.get("run", {})
    mode = run.get("mode")
    retain = run.get("retain")
    if mode not in MODES:
        errors.append(f"invalid mode: {mode!r}")
    if run.get("market") != "US":
        errors.append("version 1 requires market=US")
    if retain not in RETAIN_LEVELS:
        errors.append(f"invalid retain level: {retain!r}")
    if manifest.get("execution") != "disabled":
        errors.append("execution must remain disabled")

    mandate = manifest.get("mandate", {})
    mandate_status = mandate.get("status")
    if mandate_status not in MANDATE_STATUSES:
        errors.append(f"invalid mandate status: {mandate_status!r}")
    cash_pct = mandate.get("cash_floor_pct")
    if not is_number(cash_pct) or not 0 <= cash_pct <= 100:
        errors.append("mandate.cash_floor_pct must be between 0 and 100")
    max_loss_pct = mandate.get("max_loss_pct")
    if max_loss_pct is not None and (
        not is_number(max_loss_pct) or not 0 <= max_loss_pct <= 100
    ):
        errors.append("mandate.max_loss_pct must be null or between 0 and 100")
    if not isinstance(mandate.get("leverage_allowed"), bool):
        errors.append("mandate.leverage_allowed must be boolean")

    selection = manifest.get("selection", {})
    position = manifest.get("position", {})
    data_status = manifest.get("data", {}).get("status")
    if data_status not in DATA_STATUSES:
        errors.append(f"invalid data status: {data_status!r}")
    selection_status = selection.get("status")
    bottleneck_status = selection.get("bottleneck_status")
    position_status = position.get("status")
    if selection_status not in SELECTION_STATUSES:
        errors.append(f"invalid selection status: {selection_status!r}")
    if bottleneck_status not in BOTTLENECK_STATUSES:
        errors.append(f"invalid bottleneck status: {bottleneck_status!r}")
    if position_status not in POSITION_STATUSES:
        errors.append(f"invalid position status: {position_status!r}")
    if selection_status == "frozen" and not selection.get("selected_symbols"):
        errors.append("a frozen selection requires selected_symbols")
    if selection_status == "frozen" and bottleneck_status != "complete":
        errors.append("a frozen selection requires bottleneck_status=complete")
    if position_status in {"draft", "reviewed", "approved"} and selection_status != "frozen":
        errors.append("position work requires selection.status=frozen")
    if position_status == "approved" and max_loss_pct is None:
        errors.append("an approved position requires max_loss_pct")

    expected_by_mode = {
        "select": {"selection.md"},
        "position": {"position.md", "selection-manifest.json"},
        "full": {"selection.md", "position.md"},
        "refresh": {"change-report.md"},
        "review": {"review.md"},
    }
    expected_files = {"manifest.json", "source-audit.csv"}
    expected_files.update(expected_by_mode.get(mode, set()))
    if retain in {"standard", "audit"}:
        expected_files.add("decision-log.md")
        for directory in ("evidence", "tables", "snapshots"):
            if not (run_dir / directory).is_dir():
                errors.append(f"missing retention directory: {directory}")
        if mode in {"select", "full"}:
            expected_files.add("evidence/bottleneck-analysis.md")
    if retain == "audit":
        for directory in ("raw", "logs"):
            if not (run_dir / directory).is_dir():
                errors.append(f"missing audit directory: {directory}")
    for name in sorted(expected_files):
        if not (run_dir / name).is_file():
            errors.append(f"missing required file: {name}")

    audit_path = run_dir / "source-audit.csv"
    audit_row_count = 0
    if audit_path.is_file():
        try:
            with audit_path.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                fields = set(reader.fieldnames or [])
                audit_row_count = sum(1 for _ in reader)
        except OSError as exc:
            errors.append(f"cannot read source-audit.csv: {exc}")
        else:
            missing = REQUIRED_SOURCE_FIELDS - fields
            if missing:
                errors.append(
                    "source-audit.csv missing fields: " + ", ".join(sorted(missing))
                )
    if args.strict and mode in {"select", "position", "full", "refresh"} and audit_row_count == 0:
        errors.append("strict validation requires at least one source-audit row")

    report_names = set(expected_by_mode.get(mode, set()))
    if retain in {"standard", "audit"} and mode in {"select", "full"}:
        report_names.add("evidence/bottleneck-analysis.md")
    for name in sorted(report_names):
        path = run_dir / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        placeholders = sorted(set(PLACEHOLDER_RE.findall(text)))
        if placeholders:
            message = f"{name} has unresolved placeholders: {', '.join(placeholders)}"
            if args.strict:
                errors.append(message)
            else:
                warnings.append(message)

    if position_status in {"reviewed", "approved"}:
        positions = position.get("positions", [])
        if not positions:
            errors.append(f"position.status={position_status} requires positions")
        else:
            weights = []
            for item in positions:
                value = item.get("weight_pct")
                if not is_number(value) or not 0 <= value <= 100:
                    errors.append(f"invalid position weight: {item!r}")
                else:
                    weights.append(value)
            portfolio_cash = position.get("cash_pct")
            if not is_number(portfolio_cash):
                errors.append("position.cash_pct must be numeric")
            elif weights and abs(sum(weights) + portfolio_cash - 100) > 0.01:
                errors.append("position weights plus cash must equal 100%")
            cap = position.get("single_name_cap_pct")
            if is_number(cap) and any(weight > cap + 1e-9 for weight in weights):
                errors.append("a position exceeds single_name_cap_pct")

    completion_messages = []
    if mode in {"select", "position", "full"} and mandate_status != "confirmed":
        completion_messages.append("mandate is not confirmed")
    if mode in {"select", "position", "full"} and data_status not in {"ready", "partial"}:
        completion_messages.append(f"data status is {data_status}")
    if mode in {"select", "full"} and bottleneck_status != "complete":
        completion_messages.append("bottleneck analysis is not complete")
    if mode in {"select", "full"} and selection_status != "frozen":
        completion_messages.append("selection is not frozen")
    if mode in {"position", "full"} and position_status != "approved":
        completion_messages.append(f"position status is {position_status}")
    if manifest.get("blockers"):
        completion_messages.append("manifest contains unresolved blockers")
    if args.strict:
        errors.extend(completion_messages)
    else:
        warnings.extend(completion_messages)

    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        raise SystemExit(1)
    print(f"OK: {run_dir}")


if __name__ == "__main__":
    main()
