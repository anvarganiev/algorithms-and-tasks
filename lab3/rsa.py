import random
import math
import usefulFunctions
from usefulFunctions import pollard_euristic
import matplotlib.pyplot as plt
import mplcyberpunk

plt.style.use("cyberpunk")


def key_generation(length: int) -> tuple:
    # 1 этап - генерация 2 простых p и q
    p, q = 0, 0
    length = length // 2

    while p % 2 == 0:  # если число четное, генерируем снова
        p = random.getrandbits(length)
    # к этому моменту имеем нечетное p
    # miller-rabin test
    while not usefulFunctions.isPrime(p, int(math.log(length, 2))):  # пока p не простое
        p = random.getrandbits(length)  # генерируем p

    while q % 2 == 0:  # если число четное, генерируем снова
        q = random.getrandbits(length)
    # к этому моменту имеем нечетное p
    # miller-rabin test
    while not usefulFunctions.isPrime(q, int(math.log(length, 2))):  # пока p не простое
        q = random.getrandbits(length)  # генерируем p

    # теперь мы имеем простые p и q

    # 2-3 этап: вычиселние n и функции Эйлера
    n = p * q
    phi = (p - 1) * (q - 1)  # Функция Эйлера - кол-во взаимно простых с n чисел

    # 4 этап: Выбирается целое число e < n, взаимно простое с phi. Выберем из чисел Ферма
    pherma: list = [3, 5, 17, 257, 65537]
    exponent = 0
    for elem in pherma:
        if usefulFunctions.gcd(elem, phi) == 1:
            exponent = elem
            break

    # 5 этап: получили открытый ключ (exponent, n)
    open_key = ' '.join(map(str, [exponent, n]))
    with open('open_key.txt', mode='w') as file:
        file.write(open_key)

    # 6 этап: получение закрытого ключа (d, n)
    d = usefulFunctions.gcd_extended(exponent, phi)[1]
    if d < 0:
        d += phi
    # print(d)

    # 7 этап: запишем закрытый ключ в файл
    decryption_key = ' '.join(map(str, [d, n]))
    with open('decryption_key.txt', mode='w') as file:
        file.write(decryption_key)

    return open_key, decryption_key


# Задание 2 - шифрование / дешифрование
def encryption(open_key: str, L: int = 512) -> str:
    exponent, n = open_key.split(' ')
    with open('input.txt') as file:
        input_text = file.readline()
    # if len(input_text) > len(n) // 2:
    #     input_text = input_text[: len(n) // 2]
    binary_code = [format(int.from_bytes(i.encode(), 'big'), '08b') for i in input_text]
    binary_code = ''.join(binary_code)  # объединяем все в одну строку
    print('input text bits: ', binary_code)

    binary_code = [binary_code[x:x + L // 4] for x in
                   range(0, len(binary_code), L // 4)]  # dividing string by L/4 elements
    # print(binary_code)

    C = []
    for el in binary_code:
        el = int(el, 2)  # перевод из bin в dec
        C.append(pow(el, int(exponent), int(n)))
    C = ' '.join(map(str, C))
    with open('encrypted.txt', mode='w') as file:
        file.write(C)
    return C


def decryption(private_key: str, L: int) -> None:
    d, n = private_key.split(' ')
    with open('encrypted.txt') as file:
        C = file.readline()
    C = C.split(' ')
    M = []
    for el in C:
        M.append(pow(int(el), int(d), int(n)))

    M = [bin(el)[2:].zfill(L // 4) for el in M]

    binary_code = ''.join(map(str, M))
    print('output text bits:', binary_code)

    n = int(binary_code, 2)

    decrypted = n.to_bytes((n.bit_length()) + 7 // 8, 'big')
    decrypted = decrypted.decode()
    print(decrypted)

    with open('decrypted.txt', mode='w') as file:
        file.write(decrypted)


if __name__ == '__main__':
    L: int = 512
    open_key, decryption_key = key_generation(L)
    encryption(open_key, L)
    decryption(decryption_key, L)

    # lst = decryption_key.split()
    # n = int(lst[1])
    #
    # # 4-th exercise
    # times = []
    # key = []
    # for key_lenght in range(30, 90, 2):
    #     open_key, decryption_key = key_generation(key_lenght)
    #     lst = decryption_key.split()
    #     n = int(lst[1])
    #     times.append(pollard_euristic(n)[1])
    #     key.append(key_lenght)
    # plt.plot(key, times)
    # mplcyberpunk.add_glow_effects()
    # plt.show()

    #  5-th exercise

    # usefulFunctions.p_q_generation()

