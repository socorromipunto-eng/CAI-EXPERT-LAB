"""Command-line interface for the CAI Engine.

Usage:
    python -m cai_engine init
    python -m cai_engine status
    python -m cai_engine set <fact> <true|false>
    python -m cai_engine ingest <telemetry.json>
    python -m cai_engine propose <action.json>
    python -m cai_engine approve <action_id> --by <name>
    python -m cai_engine deny <action_id> --by <name> --reason "<text>"
    python -m cai_engine transition <STATE>
    python -m cai_engine verify
    python -m cai_engine report [--out report.md]

All commands accept --home <dir> to choose the runtime directory
(default: ./cai_runtime).
"""
from __future__ import annotations

import argparse
import json
import sys

from .engine import CAIEngine, EngineError
from .governed_agent import GovernedAgent


def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _print(obj) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cai_engine", description="CAI-EXPERT-LAB execution engine")
    p.add_argument("--home", default="cai_runtime", help="runtime directory (default: cai_runtime)")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="initialize/reset the engine (state=MODEL, fresh evidence)")
    sub.add_parser("status", help="show current state, allowed transitions and facts")

    sp = sub.add_parser("set", help="set a context fact (entry condition) true/false")
    sp.add_argument("fact")
    sp.add_argument("value", choices=["true", "false"])

    sp = sub.add_parser("ingest", help="ingest a telemetry event from a JSON file")
    sp.add_argument("file")

    sp = sub.add_parser("propose", help="propose an action (runs policy + safety + oversight)")
    sp.add_argument("file")

    sp = sub.add_parser("govern", help="govern an AI proposal (regulatory + CAI layers)")
    sp.add_argument("file")
    sp.add_argument("--jurisdiction", choices=["EU", "USA"],
                    help="override the jurisdiction (else taken from the proposal, default EU)")

    sp = sub.add_parser("approve", help="human-approve a pending action")
    sp.add_argument("action_id")
    sp.add_argument("--by", required=True, help="name of the approving human")

    sp = sub.add_parser("deny", help="human-deny a pending action")
    sp.add_argument("action_id")
    sp.add_argument("--by", required=True)
    sp.add_argument("--reason", default="")

    sp = sub.add_parser("transition", help="attempt a state transition")
    sp.add_argument("state")

    sub.add_parser("verify", help="verify the evidence hash chain integrity")

    sp = sub.add_parser("report", help="print a Markdown execution/assurance report")
    sp.add_argument("--out", help="write the report to this file instead of stdout")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    eng = CAIEngine(home=args.home)
    try:
        if args.command == "init":
            _print(eng.init())
        elif args.command == "status":
            _print(eng.status())
        elif args.command == "set":
            _print(eng.set_fact(args.fact, args.value == "true"))
        elif args.command == "ingest":
            _print(eng.ingest(_load_json(args.file)))
        elif args.command == "propose":
            _print(eng.propose(_load_json(args.file)))
        elif args.command == "govern":
            _print(GovernedAgent(eng).govern(_load_json(args.file), jurisdiction=args.jurisdiction))
        elif args.command == "approve":
            _print(eng.approve(args.action_id, args.by))
        elif args.command == "deny":
            _print(eng.deny(args.action_id, args.by, args.reason))
        elif args.command == "transition":
            _print(eng.transition(args.state))
        elif args.command == "verify":
            _print(eng.verify())
        elif args.command == "report":
            text = eng.report()
            if args.out:
                with open(args.out, "w", encoding="utf-8") as fh:
                    fh.write(text)
                print(f"report written to {args.out}")
            else:
                print(text)
    except EngineError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"error: file not found: {exc.filename}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
