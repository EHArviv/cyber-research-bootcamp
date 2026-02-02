from __future__ import annotations

import argparse
from pathlib import Path

from crb.log_parser import summarize_log


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="crb", description="Log summary tool")
    parser.add_argument("logfile", type=Path, help="Path to a log file")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.logfile.exists():
        parser.error(f"File not found: {args.logfile}")

    summary = summarize_log(args.logfile)
    print(f"Lines:    {summary['lines']}")
    print(f"Errors:   {summary['errors']}")
    print(f"Warnings: {summary['warnings']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
