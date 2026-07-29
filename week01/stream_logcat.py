import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


@dataclass
class LogLine:
    time: str
    level: str
    tag: str
    message: str


def read_lines(path) -> Iterator[str]:
    """Yield lines one at a time — file never fully loaded into memory."""
    with open(path) as f:
        for line in f:
            yield line.rstrip()


def parse_line(line: str) -> LogLine | None:
    try:
        parts = line.split(maxsplit=6)
        if parts[5] not in "VDIWEF":
            return None
        return LogLine(
            time=parts[0] + " " + parts[1],
            level=parts[5],
            tag=parts[3],
            message=parts[6].strip(),
        )
    except (IndexError, ValueError):
        return None


def parse_all(lines: Iterator[str]) -> Iterator[LogLine]:
    """Generator: yields LogLine, skipping garbage lines."""
    for line in lines:
        rec = parse_line(line)
        if rec is None:
            continue
        yield rec


def errors_only(records: Iterator[LogLine]) -> Iterator[LogLine]:
    """Generator: filters to level == 'E' only."""
    for rec in records:
        if rec.level == "E":
            yield rec


def main():
    default_path = Path(__file__).parent / "logcat.txt"
    path = sys.argv[1] if len(sys.argv) > 1 else default_path

    # Proof of laziness — this prints the generator object, NOT parsed data:
    # <generator object parse_all at 0x1029f3f80>
    print(parse_all(read_lines(path)))

    # Real work — loop over the generator directly, Counter counts as it goes,
    # koi list() kahin nahi banayi:
    counts = Counter()
    for rec in parse_all(read_lines(path)):
        counts[rec.level] += 1

    print("\nBy level:")
    for level in "VDIWEF":
        if level in counts:
            print(f"  {level}: {counts[level]}")

    # Bonus — errors_only bhi generator-chain se demo:
    error_count = sum(1 for _ in errors_only(parse_all(read_lines(path))))
    print(f"\nTotal errors (level E): {error_count}")


if __name__ == "__main__":
    main()