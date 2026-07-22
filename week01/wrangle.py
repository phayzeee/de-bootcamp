# Five typed functions. The example calls below go in each docstring as doctests; python -m doctest wrangle.py must pass silently.
#
# word_freq(text: str) -> dict[str, int] — lowercase, strip .,!?;:'" (use str.translate or a comprehension over cleaned words). word_freq("The cat and the hat.") → {'the': 2, 'cat': 1, 'and': 1, 'hat': 1}
# invert(d: dict[str, int]) -> dict[int, list[str]] — group keys by value, defaultdict(list). invert({'a': 1, 'b': 2, 'c': 1}) → {1: ['a', 'c'], 2: ['b']}
# flatten(matrix: list[list[int]]) -> list[int] — one nested comprehension. flatten([[1, 2], [3], []]) → [1, 2, 3]
# top_n(freq: dict[str, int], n: int) -> list[tuple[str, int]] — sort by count desc, ties alphabetical: key=lambda kv: (-kv[1], kv[0]). top_n({'b': 2, 'a': 2, 'c': 1}, 2) → [('a', 2), ('b', 2)]
# dedupe(items: list[str]) -> list[str] — order-preserving, via dict.fromkeys. dedupe(['x', 'y', 'x']) → ['x', 'y']

# if __name__ == "__main__":
#     word = "The cat and the hat."
#     print(word_freq(word))
#
#     print(invert({'a': 1, 'b': 2, 'c': 1}))
#
#     print(flatten([[1, 2], [3], []]))
#
#     print(top_n({'b': 2, 'a': 2, 'c': 1}, 2))
#
#     print(dedupe(['x', 'y', 'x']))
#
#

from collections import defaultdict


def word_freq(text: str) -> dict[str, int]:
    """
    >>> word_freq("The cat and the hat.")
    {'the': 2, 'cat': 1, 'and': 1, 'hat': 1}
    """
    table = str.maketrans("", "", ".,!?;:'\"")
    result = {}
    for word in text.lower().translate(table).split():
        result[word] = result.get(word, 0) + 1
    return result


def invert(d: dict[str, int]) -> dict[int, list[str]]:
    """
    >>> invert({'a': 1, 'b': 2, 'c': 1})
    {1: ['a', 'c'], 2: ['b']}
    """
    grouped = defaultdict(list)
    for k, v in d.items():
        grouped[v].append(k)
    return dict(grouped)


def flatten(matrix: list[list[int]]) -> list[int]:
    """
    >>> flatten([[1, 2], [3], []])
    [1, 2, 3]
    """
    return [num for row in matrix for num in row]


def top_n(freq: dict[str, int], n: int) -> list[tuple[str, int]]:
    """
    >>> top_n({'b': 2, 'a': 2, 'c': 1}, 2)
    [('a', 2), ('b', 2)]
    """
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def dedupe(items: list[str]) -> list[str]:
    """
    >>> dedupe(['x', 'y', 'x'])
    ['x', 'y']
    """
    return list(dict.fromkeys(items))


if __name__ == "__main__":
    print(word_freq("The cat and the hat."))
    print(invert({'a': 1, 'b': 2, 'c': 1}))
    print(flatten([[1, 2], [3], []]))
    print(top_n({'b': 2, 'a': 2, 'c': 1}, 2))
    print(dedupe(['x', 'y', 'x']))