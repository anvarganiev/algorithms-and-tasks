def get_val(a: int):
    if a == -1:
        return 1
    elif a <= 6:
        return 2
    else:
        return 3


score = [0, 0]

with open('input_ex4.txt') as file:
    for line in file.readlines()[1:]:
        team, length = tuple(map(int, line.split()))
        score[team - 1] += get_val(length)

print(f"{score[0]}:{score[1]}")
