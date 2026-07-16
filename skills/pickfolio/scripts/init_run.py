#!/usr/bin/env python3
"""Create an immutable Pickfolio run package."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS = SKILL_ROOT / "assets"
MODES = {"select", "position", "full", "refresh", "review"}
RETAIN_LEVELS = {"minimal", "standard", "audit"}
DATA_POLICIES = {"reuse", "refresh-missing", "refresh-all"}
CONFIG_KEYS = {
    "market",
    "mode",
    "as_of",
    "capital",
    "currency",
    "horizon",
    "max_loss_pct",
    "cash_floor_pct",
    "leverage_allowed",
    "benchmark",
    "existing_holdings",
    "candidate_limit",
    "bottleneck_analysis",
    "bottleneck_scoring",
    "data_policy",
    "retain",
    "language",
    "selection_approval",
    "position_approval",
    "execution",
}
SOURCE_AUDIT_FIELDS = [
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
]


def parse_decimal(value: str | None, field: str) -> float | None:
    if value is None or value == "":
        return None
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        raise argparse.ArgumentTypeError(f"{field} must be numeric") from exc
    if not parsed.is_finite() or parsed < 0:
        raise argparse.ArgumentTypeError(f"{field} must be a non-negative number")
    return float(parsed)


def parse_percent(value: str | None, field: str) -> float | None:
    parsed = parse_decimal(value, field)
    if parsed is not None and parsed > 100:
        raise argparse.ArgumentTypeError(f"{field} must be between 0 and 100")
    return parsed


def normalize_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise argparse.ArgumentTypeError("slug must contain a letter or digit")
    return slug[:64]


def parse_iso_date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("as-of must use YYYY-MM-DD") from exc


def parse_symbols(value: str) -> list[str]:
    if not value.strip():
        return []
    symbols = []
    for item in value.split(","):
        symbol = item.strip().upper()
        if symbol and symbol not in symbols:
            symbols.append(symbol)
    return symbols


def load_selection_manifest(path: str | None) -> tuple[dict | None, Path | None]:
    if not path:
        return None, None
    manifest_path = Path(path).expanduser().resolve()
    if not manifest_path.is_file():
        raise SystemExit(f"Selection manifest not found: {manifest_path}")
    with manifest_path.open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    status = manifest.get("selection", {}).get("status")
    if status != "frozen":
        raise SystemExit(
            f"Position mode requires a frozen selection manifest; found {status!r}"
        )
    return manifest, manifest_path


def render_template(template_name: str, destination: Path, values: dict[str, str]) -> None:
    text = (ASSETS / template_name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    destination.write_text(text, encoding="utf-8")


def write_source_audit(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=SOURCE_AUDIT_FIELDS).writeheader()


def load_config(path: str | None) -> tuple[dict, str | None]:
    if not path:
        return {}, None
    config_path = Path(path).expanduser().resolve()
    if not config_path.is_file():
        raise SystemExit(f"Config not found: {config_path}")
    try:
        with config_path.open(encoding="utf-8") as handle:
            config = json.load(handle)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON config {config_path}: {exc}") from exc
    if not isinstance(config, dict):
        raise SystemExit("Config root must be a JSON object")
    unknown = set(config) - CONFIG_KEYS
    if unknown:
        raise SystemExit("Unknown config keys: " + ", ".join(sorted(unknown)))
    if config.get("as_of") in {None, "latest"}:
        config.pop("as_of", None)
    if config.get("bottleneck_analysis", "required") != "required":
        raise SystemExit("Version 1 requires bottleneck_analysis=required")
    if config.get("execution", "disabled") != "disabled":
        raise SystemExit("Pickfolio execution must remain disabled")
    return config, str(config_path)


def build_parser(defaults: dict | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=None, help="JSON project configuration")
    parser.add_argument("--output-root", required=True, help="Parent directory for runs")
    parser.add_argument("--slug", required=True, type=normalize_slug)
    parser.add_argument("--mode", choices=sorted(MODES), default="full")
    parser.add_argument("--market", default="US")
    parser.add_argument("--as-of", type=parse_iso_date, default=date.today().isoformat())
    parser.add_argument("--capital", default=None)
    parser.add_argument("--currency", default="USD")
    parser.add_argument("--horizon", default="3-5y")
    parser.add_argument("--max-loss-pct", default=None)
    parser.add_argument("--cash-floor-pct", default="15")
    parser.add_argument(
        "--leverage-allowed",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument("--benchmark", default="SPY")
    parser.add_argument("--existing-holdings", default="")
    parser.add_argument("--candidate-limit", type=int, default=25)
    parser.add_argument(
        "--bottleneck-scoring",
        choices=("qualitative", "weighted"),
        default="qualitative",
    )
    parser.add_argument("--data-policy", choices=sorted(DATA_POLICIES), default="refresh-missing")
    parser.add_argument("--retain", choices=sorted(RETAIN_LEVELS), default="standard")
    parser.add_argument("--language", default="zh-CN")
    parser.add_argument("--selection-approval", choices=("required",), default="required")
    parser.add_argument("--position-approval", choices=("required",), default="required")
    parser.add_argument("--execution", choices=("disabled",), default="disabled")
    parser.add_argument("--selection-manifest", default=None)
    if defaults:
        parser.set_defaults(**defaults)
    return parser


def main() -> None:
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument("--config")
    config_args, _ = config_parser.parse_known_args()
    config, config_path = load_config(config_args.config)
    args = build_parser(config).parse_args()
    market = args.market.upper()
    if market != "US":
        raise SystemExit("Pickfolio version 1 supports market=US only")
    if args.candidate_limit <= 0:
        raise SystemExit("candidate-limit must be positive")

    capital = parse_decimal(args.capital, "capital")
    max_loss_pct = parse_percent(args.max_loss_pct, "max-loss-pct")
    cash_floor_pct = parse_percent(args.cash_floor_pct, "cash-floor-pct")
    if args.mode == "position" and capital is None:
        raise SystemExit("position mode requires --capital")

    selection_source, selection_source_path = load_selection_manifest(
        args.selection_manifest
    )
    if args.mode == "position" and selection_source is None:
        raise SystemExit("position mode requires --selection-manifest")

    run_id = f"{args.as_of}-{args.slug}"
    output_root = Path(args.output_root).expanduser().resolve()
    run_dir = output_root / run_id
    if run_dir.exists():
        raise SystemExit(f"Run directory already exists; refusing to overwrite: {run_dir}")
    run_dir.mkdir(parents=True)

    created_at = datetime.now(timezone.utc).isoformat()
    selected_symbols = []
    selection_status = "not_applicable"
    bottleneck_status = "not_applicable"
    selection_reference = None
    if args.mode in {"select", "full"}:
        selection_status = "draft"
        bottleneck_status = "pending"
    elif selection_source is not None:
        selection_status = "frozen"
        bottleneck_status = selection_source.get("selection", {}).get(
            "bottleneck_status"
        )
        if bottleneck_status != "complete":
            raise SystemExit(
                "Position mode requires bottleneck_status=complete in the selection manifest"
            )
        selected_symbols = selection_source.get("selection", {}).get(
            "selected_symbols", []
        )
        selection_reference = str(selection_source_path)

    position_status = "not_applicable"
    blockers = []
    if args.mode == "full":
        position_status = "blocked"
        blockers.append("Freeze the selection before drafting the position plan.")
    elif args.mode == "position":
        position_status = "draft" if max_loss_pct is not None else "blocked"
        if max_loss_pct is None:
            blockers.append("Approve max_loss_pct before position review.")
    if args.mode == "full" and capital is None:
        blockers.append("Set capital before position planning.")

    outputs: dict[str, str] = {
        "manifest": "manifest.json",
        "source_audit": "source-audit.csv",
    }
    mode_templates = {
        "select": [("selection", "selection-report.template.md", "selection.md")],
        "position": [("position", "position-report.template.md", "position.md")],
        "full": [
            ("selection", "selection-report.template.md", "selection.md"),
            ("position", "position-report.template.md", "position.md"),
        ],
        "refresh": [("change_report", "change-report.template.md", "change-report.md")],
        "review": [("review", "review.template.md", "review.md")],
    }
    values = {
        "RUN_ID": run_id,
        "AS_OF": args.as_of,
        "MODE": args.mode,
        "MARKET": market,
        "BENCHMARK": args.benchmark.upper(),
        "HORIZON": args.horizon,
        "SELECTION_STATUS": selection_status,
        "POSITION_STATUS": position_status,
        "CURRENCY": args.currency.upper(),
        "CAPITAL": "unset" if capital is None else f"{capital:g}",
        "CASH_FLOOR_PCT": f"{cash_floor_pct:g}",
        "LEVERAGE": "enabled" if args.leverage_allowed else "disabled",
    }
    for output_key, template_name, output_name in mode_templates[args.mode]:
        render_template(template_name, run_dir / output_name, values)
        outputs[output_key] = output_name

    write_source_audit(run_dir / "source-audit.csv")
    if args.retain in {"standard", "audit"}:
        for name in ("evidence", "tables", "snapshots"):
            (run_dir / name).mkdir()
        if args.mode in {"select", "full"}:
            render_template(
                "bottleneck-analysis.template.md",
                run_dir / "evidence" / "bottleneck-analysis.md",
                values,
            )
            outputs["bottleneck_analysis"] = "evidence/bottleneck-analysis.md"
        (run_dir / "decision-log.md").write_text(
            f"# Decision Log\n\nRun: `{run_id}`\n\n", encoding="utf-8"
        )
        outputs["decision_log"] = "decision-log.md"
    if args.retain == "audit":
        for name in ("raw", "logs"):
            (run_dir / name).mkdir()

    if selection_source_path is not None:
        snapshot_target = run_dir / "selection-manifest.json"
        shutil.copy2(selection_source_path, snapshot_target)
        outputs["selection_manifest_snapshot"] = snapshot_target.name

    existing_holdings = (
        [str(item).upper() for item in args.existing_holdings]
        if isinstance(args.existing_holdings, list)
        else parse_symbols(args.existing_holdings)
    )
    manifest = {
        "schema_version": "0.1",
        "run": {
            "id": run_id,
            "created_at": created_at,
            "as_of": args.as_of,
            "mode": args.mode,
            "market": market,
            "language": args.language,
            "retain": args.retain,
            "config": config_path,
        },
        "mandate": {
            "status": "draft",
            "capital": capital,
            "currency": args.currency.upper(),
            "horizon": args.horizon,
            "max_loss_pct": max_loss_pct,
            "cash_floor_pct": cash_floor_pct,
            "leverage_allowed": args.leverage_allowed,
            "benchmark": args.benchmark.upper(),
            "existing_holdings": existing_holdings,
            "candidate_limit": args.candidate_limit,
        },
        "data": {
            "status": "pending",
            "policy": args.data_policy,
            "snapshots": [],
        },
        "selection": {
            "status": selection_status,
            "bottleneck_status": bottleneck_status,
            "bottleneck_analysis": "required",
            "bottleneck_scoring": args.bottleneck_scoring,
            "selected_symbols": selected_symbols,
            "source_manifest": selection_reference,
        },
        "position": {
            "status": position_status,
            "positions": [],
            "cash_pct": cash_floor_pct,
            "single_name_cap_pct": None,
            "risk_groups": [],
            "stages": [],
        },
        "approvals": [],
        "approval_policy": {
            "selection": args.selection_approval,
            "position": args.position_approval,
        },
        "outputs": outputs,
        "blockers": blockers,
        "execution": args.execution,
    }
    with (run_dir / "manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(run_dir)


if __name__ == "__main__":
    main()
