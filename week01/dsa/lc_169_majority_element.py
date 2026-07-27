from typing import List


def majorityElement(self, nums: List[int]) -> int:
    freq = {}
    count = 0
    largestKey = ""

    for i in nums:
        freq[i] = freq.get(i, 0) + 1

    for key, value in freq.items():
        if value > count:
            count = value
            largestKey = key

    #uppar wale ki jaga ye line : max(freq, key= freq.get) bhi use hosakti h

    return largestKey


majorityElement([2,2,1,1,1,2,2])
