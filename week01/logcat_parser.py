import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LogLine:
    time: str
    level: str
    tag: str
    message: str

def parse_line(line: str) -> LogLine | None:
    """Return a LogLine, or None if the line doesn't fit the format.
    Hint: line.split(maxsplit=6) then clean up. Wrap in try/except (IndexError, ValueError).
    Returning None for garbage is fine — no custom exception classes today."""
    try:
        parts = line.split(maxsplit=6)
        if parts[5] not in "VDIWEF":
             return None
        return LogLine(time= parts[0]+" "+parts[1], level= parts[5], tag= parts[3], message= parts[6].strip())
    except (IndexError, ValueError):
        return None

def parse_file(path: str) -> list[LogLine]:
    """Read the file, parse every line, skip the Nones."""
    lines = []
    with open(path) as f:
        for raw in f:
            parsed = parse_line(raw)
            if parsed is not None:
                lines.append(parsed)
    return lines

def count_by_level(lines: list[LogLine]) -> dict[str, int]:
    """Hint: from collections import Counter — Counter(l.level for l in lines)"""
    return Counter(l.level for l in lines)

def noisiest_tags(lines: list[LogLine], n: int = 5) -> list[tuple[str, int]]:
    """Which tag spams your logs the most? Counter(...).most_common(n)"""
    return Counter(l.tag for l in lines).most_common(n)

if __name__ == "__main__":
    default_path = Path(__file__).parent / "logcat.txt"
    path = sys.argv[1] if len(sys.argv) > 1 else default_path

    parsed = parse_file(path)
    with open(path) as f:
        total = sum(1 for _ in f)
    skipped = total - len(parsed)

    print(f"Parsed {len(parsed)} lines ({skipped} skipped)")

    print("\nBy level:")
    counts = count_by_level(parsed)
    for level in "VDIWEF":
        if level in counts:
            print(f"  {level}: {counts[level]}")

    print("\nTop 5 noisiest tags:")
    tags = noisiest_tags(parsed)
    width = max(len(tag) for tag, _ in tags)
    for tag, count in tags:
        print(f"  {tag:<{width}}  {count}")
