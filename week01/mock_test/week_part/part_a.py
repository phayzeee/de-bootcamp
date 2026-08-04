#QUESTION 01

from typing import List, Iterator
from unittest import result


def top_n_words(path : str | None, n: int) -> list[tuple[str,int]]:
    result = []
    with open(path) as f:
        for raw in f:
            words = raw.split()

            for word in words:
                clean_word = removePunctuationAndCaseSensitive(word)
                result.append(clean_word)


    word_count = word_counter(result)
    sorted_words = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))

    return sorted_words[:n]


#
def removePunctuationAndCaseSensitive(word: str) -> str:
    word = word.lower()
    punc = ".,!?;:'\""
    word = word.strip(punc)

    return word

def word_counter(words : List[str]) -> dict:
    freq = {}

    for word in words:
        freq[word] = freq.get(word, 0) + 1

    return freq


# print(top_n_words("speech.txt", 3))


#QUESTION 02

def running_avg(nums) -> Iterator[float]:
    total = 0
    count = 0

    for num in nums:
        total += num
        count += 1
        avg = total / count
        yield avg

print(list(running_avg([2,4,6])))

