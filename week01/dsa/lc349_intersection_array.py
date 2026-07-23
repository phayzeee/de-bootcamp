from typing import List


class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        return list(set(nums1) &  set(nums2))


    def intersection_without_sets(self, nums1: List[int], nums2: List[int]) -> List[int]:
        seen = {}

        for num in nums1:
            seen[num] = True

        result = []

        for num in nums2:
            if num in seen:
                result.append(num)
                del seen[num]

        return result
