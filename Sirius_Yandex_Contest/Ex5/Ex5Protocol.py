from itertools import permutations


def foo(abc, x, y):
    a = int(abc[:x])
    b = int(abc[x:y])
    c = int(abc[y:])
    return [a, b, c] if a + b == c else []


with open('input_ex5.txt') as file:
    s = file.readline()

perm = permutations(range(len(s)), 2)
perm = filter(lambda x: 0 < x[0] < x[1] <= len(s) * 2 / 3, perm)

for el in perm:
    res = foo(s, el[0], el[1])
    if res:
        print('{0}+{1}={2}'.format(*res))
        break

# 1 + 2 =? 3123246 -
# 12 + 3 =? 123246 -
# 1 + 23 =? 123246 -
# 12 + 31 =? 23246 -
# 123 + 12 =? 3246 -
# 123 + 123 =? 246 +

# 110011002 -> 1+1001 = 1002
