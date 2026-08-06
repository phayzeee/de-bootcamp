def running_avg(nums):
    count = 0
    total = 0

    for num in nums:
        count += 1
        total += num
        avg = total / count
        yield avg

print(list(running_avg([2,4,6])))