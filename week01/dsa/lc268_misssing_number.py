# My Solution:
from typing import List


def missingNumber(self, nums: List[int]) -> int:
    nums.sort()
    count = 0
    for i in nums:
        if i == count:
            count += 1
        else:
            break
    return count


# Recommended:
def missingRecNumber(self, nums: List[int]) -> int:
    n = len(nums)
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)

    return expected_sum - actual_sum

def missingSetNum(self, nums: List[int]) -> int:
    num_set = set(nums)

    for i in range(len(nums) + 1):
        if i not in num_set:
            return i
    return None
