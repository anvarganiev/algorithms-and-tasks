import time
import random
import math
import matplotlib.pyplot as plt
import mplcyberpunk

plt.style.use("cyberpunk")


def p_q_generation(length: int = 90) -> None:
    # 1 этап - генерация 2 простых p и q

    times = []
    relations = []
    for l in range(25, 55, 5):
        p, q = 0, 0
        r = l / 100
        relations.append(r)
        length1 = int(r * length)
        length2 = int((1 - r) * length)
        print(length1, length2)
        random.seed(time.time())
        while p % 2 == 0:  # если число четное, генерируем снова
            p = random.getrandbits(length1)
        # к этому моменту имеем нечетное p
        # miller-rabin test
        while not isPrime(p, int(math.log(length1, 2))):  # пока p не простое
            p = random.getrandbits(length1)  # генерируем p

        while q % 2 == 0:  # если число четное, генерируем снова
            q = random.getrandbits(length2)
        # к этому моменту имеем нечетное p
        # miller-rabin test
        while not isPrime(q, int(math.log(length2, 2))):  # пока p не простое
            q = random.getrandbits(length2)  # генерируем p

        print('p = {0} q = {1}'.format(p, q))
        times.append(pollard_euristic(p*q)[1])
        # pollard_euristic(p * q)
    plt.plot(relations, times)
    mplcyberpunk.add_glow_effects()
    plt.show()




def isPrime(n, k):  # miller-rabin
    from random import randint
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            return n == p
    s, d = 0, n - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    for i in range(k):
        x = pow(randint(2, n - 1), d, n)
        if x == 1 or x == n - 1:
            continue
        for r in range(1, s):
            x = (x * x) % n
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False
    return True


# алгоритм Евклида для НОД
def gcd(a, b) -> int:
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a

    return a + b


# Extended Euclid algorithm
def gcd_extended(num1, num2):
    if num1 == 0:
        return num2, 0, 1
    else:
        div, x, y = gcd_extended(num2 % num1, num1)
    return div, y - (num2 // num1) * x, x


def pollard_euristic(n, seed=2, f=lambda x: x ** 2 + 1) -> tuple:
    x, y, d = seed, seed, 1
    iteration = 0
    timing = time.time()
    while d == 1:
        x = f(x) % n
        y = f(f(y)) % n
        d = gcd((x - y) % n, n)
        iteration += 1
    if d != n:
        print(d, n // d)
        print('Кол-во итераций: ', iteration)
        print('Затраченное время: ', time.time() - timing)
        return d, time.time() - timing
