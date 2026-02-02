from __future__ import annotations

from pathlib import Path


def summarize_log(path: str | Path) -> dict[str, int]:
    p = Path(path)
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()

    errors = 0
    warnings = 0

    for line in lines:
        upper = line.upper()
        if "ERROR" in upper:
            errors += 1
        if "WARN" in upper:
            warnings += 1

    return {"lines": len(lines), "errors": errors, "warnings": warnings}
