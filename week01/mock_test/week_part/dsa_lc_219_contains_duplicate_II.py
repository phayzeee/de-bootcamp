from typing import List


def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
    new_dict = {}

    for i in range(len(nums)):
        if nums[i] in new_dict:
            if i - new_dict[nums[i]] <= k:
                return True

        new_dict[nums[i]] = i

    return False

print(containsNearbyDuplicate([1,2,3,1], 4))
