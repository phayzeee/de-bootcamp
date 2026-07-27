from typing import Counter


def reConstruct(ransomNote: str, magazine: str):

    # Counter version
    # return not (Counter(ransomNote) - Counter(magazine))

    freq = {}

    for ch in magazine:
        freq[ch] = freq.get(ch, 0) + 1

    for i in ransomNote:
        if i not in ransomNote or freq[i] == 0:
            return False

        freq[i] -= 1

    return True


print(reConstruct("aa", "aab"))
