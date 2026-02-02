from pathlib import Path

import pytest

from crb.log_parser import summarize_log


def write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


def test_counts_basic(tmp_path: Path) -> None:
    p = write(tmp_path, "a.log", "INFO hello\nWARN something\nERROR bad\n")
    s = summarize_log(p)
    assert s["lines"] == 3
    assert s["warnings"] == 1
    assert s["errors"] == 1


def test_empty_file(tmp_path: Path) -> None:
    p = write(tmp_path, "empty.log", "")
    s = summarize_log(p)
    assert s == {"lines": 0, "errors": 0, "warnings": 0}


def test_case_insensitive(tmp_path: Path) -> None:
    p = write(tmp_path, "case.log", "error one\nWarn two\nwArNiNg three\n")
    s = summarize_log(p)
    assert s["lines"] == 3
    assert s["errors"] == 1
    # summarize_log מזהה "WARN" כתת-מחרוזת, לכן Warning גם נספר
    assert s["warnings"] == 2


def test_warn_and_error_in_same_line_count_both(tmp_path: Path) -> None:
    p = write(tmp_path, "both.log", "WARN something ERROR happened\n")
    s = summarize_log(p)
    assert s["lines"] == 1
    assert s["warnings"] == 1
    assert s["errors"] == 1


def test_multiple_occurrences_in_one_line_are_counted_once(tmp_path: Path) -> None:
    # לפי המימוש הנוכחי: כל שורה תוסיף לכל היותר 1 לשגיאות ו-1 לאזהרות
    p = write(tmp_path, "multi.log", "ERROR ERROR ERROR\nWARN WARN\n")
    s = summarize_log(p)
    assert s["lines"] == 2
    assert s["errors"] == 1
    assert s["warnings"] == 1


def test_non_utf8_bytes_do_not_crash(tmp_path: Path) -> None:
    # ניצור קובץ עם בתים "לא תקינים" עבור utf-8 כדי לוודא errors="replace" עובד
    p = tmp_path / "bad-encoding.log"
    p.write_bytes(b"\xff\xfeERROR\xff\nWARN\xfe\n")
    s = summarize_log(p)
    assert s["lines"] == 2
    assert s["errors"] == 1
    assert s["warnings"] == 1


def test_returns_expected_keys(tmp_path: Path) -> None:
    p = write(tmp_path, "keys.log", "INFO\n")
    s = summarize_log(p)
    assert set(s.keys()) == {"lines", "errors", "warnings"}
    assert all(isinstance(v, int) for v in s.values())
