from typing import List, Counter


def singleNumber(nums: List[int]) -> int:
    # freq = {}
    #
    # for i in range(len(nums)):
    #     freq[nums[i]] = freq.get(nums[i], 0) + 1

    for index, value in Counter(nums).items():
        if value == 1:
            return index



#Recommend Version with XOR
def singleNumberWithXOR(nums: List[int]) -> int:
    result = 0
    for i in range(len(nums)):
        result ^= nums[i]

    return result

print(singleNumberWithXOR([2,2,1]))

