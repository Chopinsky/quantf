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
