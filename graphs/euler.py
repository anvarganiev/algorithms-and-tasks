from queue import Queue
import random as rand


def find_path(N):
    if check_if_eiler(N):
        # задаем начальный узел в вершине нечетной степени
        v = 0;
        for i in N.keys():
            if len(N[i]) % 2 == 1:
                v = i
                break
        # теперь наша вершина start = 3, те вершина D

        stack = []  # Создаем временный стек
        finalst = []  # финальный список - ответ

        n_copy = N.copy();
        stack.append(v)

        while (len(stack) != 0):
            v = stack[-1]
            if len(n_copy[v]) == 0:
                finalst.append(v)
                stack.pop()
            else:
                index = rand.randrange(len(n_copy[v]))
                stack.append(n_copy[v][index])
                del n_copy[v][index]  # удаление ребра по которму прошли
                try:
                    n_copy[stack[-1]].remove(v)  # удаление ребра по которму прошли 2 (в обратную сторону)
                except ValueError:
                    print("петля")

    return finalst


def check_if_eiler(N):
    # проверка на нечетность вершин - на Эйлеровость
    count = 0
    is_eiler = True
    for i in N.keys():
        if len(N[i]) % 2 != 0:
            count += 1
        if count > 2:  # если нечетных вершин больше 2-х, то break, так как граф неэйлеров
            print("Более 2-х вершин нечетной степени - граф не эйлеров")
            is_eiler = False
            break
    return is_eiler

N = {
    'a': ['b', 'c'],
    'b': ['a', 'c', 'd', 'e'],
    'c': ['a', 'b', 'd', 'e'],
    'd': ['b', 'c', 'e'],
    'e': ['b', 'c', 'd']
}

print(find_path(N))
