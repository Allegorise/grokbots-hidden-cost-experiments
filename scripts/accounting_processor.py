#!/usr/bin/env python3
"""Deterministic invoice register builder for TokenLab email exports.

Reads an email CSV (ID, date, sender, subject, body, processed), selects records
whose subject contains the word "invoice" (case-insensitive), extracts the invoice
amount, currency and payment terms from the body using regular expressions, and
writes the register to a CSV. Records with missing or invalid data are reported
as exceptions and never filled with invented values.
"""
import csv
import re
import sys
from pathlib import Path
from decimal import Decimal, InvalidOperation

ROOT = Path(__file__).resolve().parent.parent
INPUT_PATH = ROOT / "data/tokenlab_emails.csv"
OUTPUT_PATH = "reproduced.csv"
EXCEPTIONS_PATH = "reproduced_exceptions.csv"

OUTPUT_FIELDS = ["Email ID", "Sender", "Subject", "Invoice amount", "Currency", "Payment terms"]
REQUIRED_INPUT = ["ID", "sender", "subject", "body"]

SUBJECT_RE = re.compile(r"\binvoice\b", re.IGNORECASE)
CURRENCY_CODES = r"EUR|USD|GBP|CZK|CHF|PLN|SEK|NOK|DKK|HUF|JPY|CAD|AUD"
SYMBOLS = {"€": "EUR", "$": "USD", "£": "GBP"}
NUM = r"\d{1,3}(?:[ ,.]\d{3})*(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?"
AMOUNT_PATTERNS = [
    re.compile(rf"(?:total|amount|amount due|sum)[^.\d€$£]{{0,40}}?(?P<num>{NUM})\s*(?P<cur>{CURRENCY_CODES})\b", re.I),
    re.compile(rf"(?:total|amount|amount due|sum)[^.\d€$£]{{0,40}}?(?P<cur>{CURRENCY_CODES})\s*(?P<num>{NUM})", re.I),
    re.compile(rf"(?:total|amount|amount due|sum)[^.\d€$£]{{0,40}}?(?P<sym>[€$£])\s*(?P<num>{NUM})", re.I),
]
TERMS_RE = re.compile(r"\b(?:payable|due|payment(?: is)? due)\s+(?P<terms>within\s+\d+\s+days?(?:\s+of\s+(?:the\s+)?[a-z ]+?date)?)\b", re.I)


def parse_amount(raw):
    s = raw.replace(" ", "")
    # Decide decimal separator: a trailing group of 1-2 digits after , or . is decimals.
    m = re.match(r"^(.*?)([.,])(\d{1,2})$", s)
    if m:
        whole = re.sub(r"[.,]", "", m.group(1))
        s = f"{whole}.{m.group(3)}"
    else:
        s = re.sub(r"[.,]", "", s)
    try:
        value = Decimal(s)
    except InvalidOperation:
        return None
    if value <= 0:
        return None
    return format(value.normalize(), "f")


def normalize_terms(t):
    t = re.sub(r"\s+", " ", t.strip())
    t = re.sub(r"\bof the\b", "of", t, flags=re.I)
    return t[0].upper() + t[1:]


def extract(row):
    problems = []
    rid = (row.get("ID") or "").strip()
    sender = (row.get("sender") or "").strip()
    subject = (row.get("subject") or "").strip()
    body = row.get("body") or ""
    if not rid or not rid.isdigit():
        problems.append("missing or invalid Email ID")
    if not sender:
        problems.append("missing sender")
    if not body.strip():
        problems.append("missing body")

    amount = currency = None
    for pat in AMOUNT_PATTERNS:
        m = pat.search(body)
        if m:
            amount = parse_amount(m.group("num"))
            currency = (m.groupdict().get("cur") or SYMBOLS.get(m.groupdict().get("sym") or "", "")).upper() or None
            break
    if amount is None:
        problems.append("invoice amount not found or invalid")
    if currency is None:
        problems.append("currency not found")

    tm = TERMS_RE.search(body)
    terms = normalize_terms(tm.group("terms")) if tm else None
    if terms is None:
        problems.append("payment terms not found")

    record = {
        "Email ID": rid, "Sender": sender, "Subject": subject,
        "Invoice amount": amount, "Currency": currency, "Payment terms": terms,
    }
    return record, problems


def main(input_path=INPUT_PATH, output_path=OUTPUT_PATH, exceptions_path=EXCEPTIONS_PATH):
    processed, exceptions = [], []
    try:
        with open(input_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            missing_cols = [c for c in REQUIRED_INPUT if c not in (reader.fieldnames or [])]
            if missing_cols:
                print(f"Error: input is missing columns: {', '.join(missing_cols)}", file=sys.stderr)
                return 1
            for line_no, row in enumerate(reader, start=2):
                if not SUBJECT_RE.search(row.get("subject") or ""):
                    continue
                record, problems = extract(row)
                if problems:
                    exceptions.append({"Email ID": record["Email ID"] or f"(row {line_no})",
                                       "Subject": record["Subject"], "Issue": "; ".join(problems)})
                else:
                    processed.append(record)
    except (OSError, csv.Error, UnicodeDecodeError) as e:
        print(f"Error reading {input_path}: {e}", file=sys.stderr)
        return 1

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        w.writeheader()
        w.writerows(processed)
    if exceptions:
        with open(exceptions_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["Email ID", "Subject", "Issue"])
            w.writeheader()
            w.writerows(exceptions)

    print(f"Processed records: {len(processed)}")
    print(f"Exceptions: {len(exceptions)}")
    print(f"Output file: {output_path}")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(main(*args) if args else main())
