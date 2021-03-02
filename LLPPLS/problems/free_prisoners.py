from itertools import combinations
# from math import comb


def solution(count, required):
    # no bunny required, don't needs to keep keys
    if required > count:
        return [[] for _ in range(count)]

    # need all bunnies to open the door, each carry a unique key
    if count == required:
        return [[i] for i in range(count)]

    # need 1 bunny, each of them carries just the first key
    if required == 1:
        return [[0] for _ in range(count)]

    # need 2 bunnies, take 1 key off from each bunny
    if required == 2:
        return [list(set([j for j in range(count)]) - {count - 1 - i}) for i in range(count)]

    # how many times a key can appear among in all key chains
    key_count = count - (required - 1)
    bunnies = [[] for _ in range(count)]

    # the key # to be distributed among `count` bunnies
    key_num = 0

    # each key shall be distributed to `count - (required - 1)` bunnies, without repeating
    # sequence (otherwise we may have a chance to choose less bunny and still open the lock);
    # so the idea is to pick `key_count` bunnies and give them all a key, and the bunnies
    # combination shall not repeat, hence we use the `combinations` to generate unique bunny
    # combos with `key_count` length: pick `key_count` bunnies from total of `count` bunnies.
    for g in combinations(range(count), key_count):
        # n is the bunny #n that will hold this key -- #key_num, assign
        # the key by appending the key number to the bunny's key chain
        for n in g:
            bunnies[n].append(key_num)

        print(f"key {key_num} is distributed to groups: {g}")
        key_num += 1

    return bunnies


def test_free_prisoners():
    tests = [
        [5, 2],
        [6, 5],
        [5, 3],
        [4, 4],
    ]

    for t in tests:
        print(solution(t[0], t[1]))


'''
    for c in list(combinations([0, 1, 2, 3, 4, 5], 3)):
        print(c)

    s = {2, 4}
    s.add(2)
    s.add(6)
    print("set:", s)
    print(list({1, 2, 3, 4, 5, 4, 7, 8, 2, 4}))
'''
