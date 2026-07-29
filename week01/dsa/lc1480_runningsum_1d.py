from typing import List


def runningSum( nums: List[int]) -> List[int]:
    sumList = []
    total = 0

    for i in nums:
        total = total + i
        sumList.append(total)

    return sumList
