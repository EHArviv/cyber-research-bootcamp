# cyber-research-bootcamp

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install black ruff pytest

#For Example - Run CLI
printf "INFO hello\nWARN something\nERROR bad\n" > sample.log
python -m crb.cli sample.log

#The Output
Lines:    3
Errors:   1
Warnings: 1

#Run tests
pytest -q

#Format/Lint
black .
ruff check .

---

## התוצר הסופי (מה צריך להיות לך)
- `tests/test_log_parser.py` עם **5+ בדיקות** ✅
- `pytest -q` עובר בלי כשלונות ✅
- `README.md` מסביר איך להריץ ✅


