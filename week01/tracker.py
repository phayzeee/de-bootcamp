import csv
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

CSV_PATH = Path(__file__).parent / "expenses.csv"
FIELDNAMES = ["id", "date", "category", "amount", "note"]


def load_expenses() -> list[dict]:
    if not CSV_PATH.exists():
        return []

    with open(CSV_PATH, newline= "") as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_expense(row: dict) -> None:
    file_exists = CSV_PATH.exists()
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def next_id(expenses: list[dict]) -> int:
    if not expenses:
        return 1
    return max(int(e["id"]) for e in expenses) + 1

def cmd_add(args: list[str]) -> None:
    if len(args) < 2:
        print("Usage: tracker.py add <amount> <category> [note]")
        sys.exit(1)

    amount_str, category = args[0], args[1]
    note = args[2] if len(args) > 2 else ""

    try:
        amount = Decimal(amount_str)
    except InvalidOperation:
        print(f"Error: '{amount_str}' is not a valid amount")
        sys.exit(1)

    if amount < 0:
        print("Error: amount cannot be negative")
        sys.exit(1)

    expenses = load_expenses()
    new_id = next_id(expenses)

    row = {
        "id": str(new_id),
        "date": date.today().isoformat(),
        "category": category,
        "amount": str(amount.quantize(Decimal("0.01"))),
        "note": note,
    }
    save_expense(row)
    print(f"Added #{new_id}: {category} {amount:.2f}")


def cmd_list(args: list[str]) -> None:
    expenses = load_expenses()
    for e in expenses:
        amount = Decimal(e["amount"])
        line = f"#{e['id']:<3}{e['date']}  {e['category']:<10} {amount:>8.2f}"
        if e["note"]:
            line += f"  {e['note']}"
        print(line)


def cmd_summary(args: list[str]) -> None:
    expenses = load_expenses()
    totals: dict[str, Decimal] = {}
    for e in expenses:
        amount = Decimal(e["amount"])
        totals[e["category"]] = totals.get(e["category"], Decimal("0")) + amount

    grand_total = Decimal("0")
    for category, total in totals.items():
        print(f"{category:<10} {total:>8.2f}")
        grand_total += total

    print(f"{'TOTAL':<10} {grand_total:>8.2f}")


def main():
    if len(sys.argv) < 2:
        print("Usage: tracker.py <add|list|summary> [args]")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "add":
        cmd_add(args)
    elif command == "list":
        cmd_list(args)
    elif command == "summary":
        cmd_summary(args)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()