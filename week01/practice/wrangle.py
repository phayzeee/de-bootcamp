# Five typed functions. The example calls below go in each docstring as doctests; python -m doctest wrangle.py must pass silently.
#
# word_freq(text: str) -> dict[str, int] — lowercase, strip .,!?;:'" (use str.translate or a comprehension over cleaned words). word_freq("The cat and the hat.") → {'the': 2, 'cat': 1, 'and': 1, 'hat': 1}
# invert(d: dict[str, int]) -> dict[int, list[str]] — group keys by value, defaultdict(list). invert({'a': 1, 'b': 2, 'c': 1}) → {1: ['a', 'c'], 2: ['b']}
# flatten(matrix: list[list[int]]) -> list[int] — one nested comprehension. flatten([[1, 2], [3], []]) → [1, 2, 3]
# top_n(freq: dict[str, int], n: int) -> list[tuple[str, int]] — sort by count desc, ties alphabetical: key=lambda kv: (-kv[1], kv[0]). top_n({'b': 2, 'a': 2, 'c': 1}, 2) → [('a', 2), ('b', 2)]
# dedupe(items: list[str]) -> list[str] — order-preserving, via dict.fromkeys. dedupe(['x', 'y', 'x']) → ['x', 'y']
from unittest import result

from mypy.binder import defaultdict


#1
def word_freq(text: str) -> dict[str, int]:
    result = {}
    for c in text.split():
        result[c] = result.get(c, 0) + 1

    return result

word = "The cat and the hat."
print(word_freq(word.lower()))

#2
def invert(d: dict[str, int]) -> dict[int, list[str]]:
    result_one = defaultdict(list)

    for k,v in d.items():
        result_one[v].append(k)

    return dict(result_one)

print(invert({'a': 1, 'b': 2, 'c': 1}))