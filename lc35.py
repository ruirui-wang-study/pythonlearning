def searchInsert(nums, target):
    s = len(nums)
    l, r = 0, s - 1
    if target < nums[0]:
        return 0
    if target > nums[-1]:
        return s
    while l < r:
        mid = (l + r) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] > target:
            r = mid - 1
        else:
            l = mid + 1
    if l == r:
        if nums[l] > target:
            return l
        else:
            return l + 1
    else:
        return l


l = [1]
print(searchInsert(l, 1))
