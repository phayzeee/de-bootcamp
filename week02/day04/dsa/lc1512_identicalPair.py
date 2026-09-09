from typing import List


def numIdenticalPairs(nums: List[int]) -> int:
    freq = {}
    count = 0

    for num in nums:
        if num in freq:
            count += freq[num]
            freq[num] += 1
        else:
            freq[num] = 1

    return count

print(numIdenticalPairs([1,2,3,1,1,3]))
