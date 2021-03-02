def solution0(s):
    # Your code here
    if len(s) <= 1:
        return len(s)

    arr = kmp(s)
    print(arr)

    return arr


def kmp(s):
    l = len(s)
    jumps = [0, 0]
    j = 0

    for i in range(1, l):
        while s[i] != s[j] and j > 0:
            j = jumps[j]

        if s[i] == s[j]:
            j += 1

        jumps.append(j)

    return jumps


# s0 = "abccbaabccbaabccba"
# s1 = "aaaaaaaa"
# s2 = "aabaabaabaab"
#
# s = s2
# l = len(s)
# arr = solution(s)
# count = l / (l - arr[l])
# print(len(s), int(count))


def solution1(total_lambs):
    # Your code here
    if total_lambs == 1:
        return 1

    ans = countFrugal(total_lambs) - countGenerous(total_lambs)
    if ans < 0:
        return 0

    return ans


def countFrugal(total):
    s0 = 1
    s1 = 1
    count = 1
    curr_total = 2

    while curr_total <= total:
        next_lamb = s0 + s1
        s0 = s1
        s1 = next_lamb
        curr_total += next_lamb
        count += 1

    return count


def countGenerous(total):
    s0 = 2
    count = 0

    while s0 - 1 <= total:
        s0 <<= 1
        count += 1

    return count


def solution(src, dest):
    # Your code here
    dirs = [
        [-2, -1], [-2, 1],
        [-1, -2], [-1, 2],
        [1, -2], [1, 2],
        [2, -1], [2, 1],
    ]

    visited = {src: True}
    steps = 1
    curr_pos = [src]

    while len(curr_pos) > 0:
        next_pos = []

        for position in curr_pos:
            x, y = fromKey(position)

            for d in dirs:
                x0 = x + d[0]
                y0 = y + d[1]

                if x0 < 0 or x0 >= 8 or y0 < 0 or y0 >= 8:
                    continue

                pos = toKey(x0, y0)
                if pos == dest:
                    print(x, y, x0, y0)
                    return steps

                if pos in visited.keys():
                    continue

                visited[pos] = True
                next_pos.append(pos)

        curr_pos = next_pos
        steps += 1

    return -1


def toKey(x, y):
    return x * 8 + y


def fromKey(key):
    return int(key / 8), int(key % 8)


print(solution(19, 32))


def solution4(l):
    base = []
    total = 0

    for i in range(len(l)):
        count = 0

        for j in range(i):
            if l[i] % l[j] == 0:
                count += 1

                if i >= 2 and j >= 1:
                    total += base[j]

        base.append(count)

    print(base)

    # for i in range(2, len(l)):
    #     for j in range(i):
    #         if l[i] % l[j] == 0:
    #             count += base[j]

    return total


a0 = [1, 1, 1]
a1 = [1, 2, 3, 4, 5, 6]

print(solution4(a0))


def solution5(map):
    # Your code here
    h, w = len(map), len(map[0])
    steps = []

    for i in range(h):
        arr = []
        for j in range(w):
            arr.append([-1, -1])

        steps.append(arr)

    steps[0][0][0] = 1
    stack = [[0, 0]]
    dirs = [-1, 0, 1, 0, -1]

    # print(steps, len(steps), len(steps[0]), len(steps[0][0]))

    while len(stack) > 0:
        print(stack)

        nextStack = []
        added = {}

        for pos in stack:
            x, y = pos[0], pos[1]

            for i in range(4):
                x0, y0 = x + dirs[i], y + dirs[i + 1]

                if x0 < 0 or x0 >= h or y0 < 0 or y0 >= w:
                    continue

                key = x0 * w + y0

                # the cell is a wall
                if map[x0][y0] == 1:
                    # can't reach this position without taking
                    # down a wall previously
                    if steps[x][y][0] < 0:
                        continue

                    # if we haven't reached this cell, or if we have a better solution
                    if steps[x0][y0][1] < 0: # or steps[x][y][0] + 1 < steps[x0][y0][1]:
                        steps[x0][y0][1] = steps[x][y][0] + 1

                        if key not in added:
                            nextStack.append([x0, y0])
                            added[key] = True
                # the cell is a free pass
                else:
                    if steps[x0][y0][0] < 0 and steps[x][y][0] > 0: # or (steps[x][y][0] >= 1 and steps[x][y][0] + 1 < steps[x0][y0][0]):
                        steps[x0][y0][0] = steps[x][y][0] + 1

                        if key not in added:
                            nextStack.append([x0, y0])
                            added[key] = True

                    if steps[x0][y0][1] < 0 and steps[x][y][1] > 0: # or (steps[x][y][1] >= 1 and steps[x][y][1] + 1 < steps[x0][y0][1]):
                        steps[x0][y0][1] = steps[x][y][1] + 1

                        if key not in added:
                            nextStack.append([x0, y0])
                            added[key] = True

                if x0 == h - 1 and y0 == w - 1:
                    print("done ... ")
                    for row in steps:
                        print(row)

                    if steps[x0][y0][0] > 0:
                        return steps[x0][y0][0]

                    if steps[x0][y0][1] > 0:
                        return steps[x0][y0][1]

        stack = nextStack

    return -1


a0 = [
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 1, 0, 0],
    [1, 1, 1, 0]
]

a1 = [
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0]
]

print(solution5(a1))


def solution6(x, y):
    a, b = int(x), int(y)
    if a <= b:
        a, b = b, a

    if b == 1:
        return a - 1

    count = 0
    while b > 1:
        count += int(a / b)
        a, b = b, a % b

    count += a - 1
    return str(count)


print(solution6('2', '1'))


# def solution7(times, times_limit):
#     # Your code here
#     h = len(times)
#     timer = times[0][1]
#
#     for i in range(h):
#         for j in range(h):
#             if i != j and times[i][j] < timer:
#                 timer = times[i][j]
#
#     cache = {}
#     bunnies, _, _ = travel(times, cache, times_limit, timer, 0, 0, 0, h)
#     ans = []
#     base = 1
#     idx = 0
#
#     print("meta:", timer, times_limit, h, bunnies)
#
#     while base <= bunnies:
#         if base & bunnies > 0:
#             ans.append(idx)
#
#         base <<= 1
#         idx += 1
#
#     return ans
#
#
# def travel(times, cache, time_left, limit, bunnies, count, pos, h):
#     key = str(time_left) + "," + str(pos) + "," + str(bunnies)
#     if key in cache.keys():
#         return cache[key][0], cache[key][1], cache
#
#     # can't finish the trip
#     if time_left < 0 and time_left - limit < 0:
#         return 0, 0, cache
#
#     if pos == h - 1 and time_left < 0:
#         return 0, 0, cache
#
#     base = 1
#     bestCount = 0
#     bestPickups = 0
#
#     if pos == h-1 and time_left >= 0:
#         bestPickups = bunnies
#         bestCount = count
#         # print("at door:", bestCount, bestCount)
#
#     for i in range(h):
#         # don't sit down
#         if i == pos:
#             continue
#
#         # if (i == 0 or i == h-1) and (times[pos][i] >= time_left):
#         #     continue
#
#         # the bunny is picked up
#         nextRound = bunnies
#         nextCount = count
#
#         if 0 < i < h - 1 and (base & bunnies == 0):
#             # if the next bunny has not been picked up yet
#             nextRound |= base
#             nextCount += 1
#
#         pickups, pickupCount, cache = travel(times, cache, time_left - times[pos][i], limit, nextRound, nextCount, i, h)
#
#         # if pickups > 0:
#         #     print(pos, pickups, pickupCount, nextRound, nextCount)
#
#         if pickupCount > bestCount:
#             bestCount = pickupCount
#             bestPickups = pickups
#         elif (pickupCount > 0) and pickupCount == bestCount and bestPickups != pickups:
#             idx = 1
#             while idx <= pickups and idx <= bestPickups:
#                 if (idx & pickups > 0) and (idx & bestPickups == 0):
#                     bestCount = pickupCount
#                     bestPickups = pickups
#                     break
#
#                 if (idx & pickups == 0) and (idx & bestPickups > 0):
#                     break
#
#                 idx <<= 1
#
#         # all bunnies have been picked up
#         if bestCount == h-2:
#             break
#
#         if i > 0:
#             base <<= 1
#
#     cache[key] = [bestPickups, bestCount]
#     return bestPickups, bestCount, cache
#
#
# aa0 = [
#     [0, 2, 2, 2, -1],
#     [9, 0, 2, 2, -1],
#     [9, 3, 0, 2, -1],
#     [9, 3, 2, 0, -1],
#     [9, 3, 2, 2, 0]
# ]
# t0 = 1
#
# aa1 = [
#     [0, 1, 1, 1, 1],
#     [1, 0, 1, 1, 1],
#     [1, 1, 0, 1, 1],
#     [1, 1, 1, 0, 1],
#     [1, 1, 1, 1, 0]
# ]
# t1 = 3
#
# print(solution7(aa0, t0))
