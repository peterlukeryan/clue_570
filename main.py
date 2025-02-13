

map = dict()
nums = [1,2,3,2,2, 6, 6, 6,6 ]

for num in nums:
    if num in map:
        map[num] += 1
    else:
        map[num] = 1

max = 0
return_index = -1
for item in map:
    if map[item] > max:
        max = map[item]
        return_index = item
print(return_index)


