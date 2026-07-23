#TWO SUM BRUTE FORCE
from typing import List


class Solution:
    def twoSumBruteForce(self, nums: List[int], target: int) -> List[int]:
        result = []

        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] + nums[j] == target:
                    result.append(i)
                    result.append(j)

        return result

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        result = {}

        for i, v in enumerate(nums):
            compliment = target - v

            if compliment in result:
                return [result[compliment], i]

            result[v] = i

sol = Solution()
print(sol.twoSum([3,4,2], 6))