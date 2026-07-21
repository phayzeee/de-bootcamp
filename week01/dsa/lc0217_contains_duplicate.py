from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()

        for num in nums:
            if num in seen:
                return True
            seen.add(num)

        return False

arr = [1, 2, 3, 1]
sol = Solution()
print(sol.containsDuplicate(arr))