def firstUniqChar(s: str) -> int:
    freq = {}

    for i in s:
        freq[i] = freq.get(i, 0) + 1

    for index, char in enumerate(s):
        if freq[char] == 1:
            return index

    return -1


print(firstUniqChar("aabb"))