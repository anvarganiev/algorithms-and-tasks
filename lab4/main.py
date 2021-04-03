from useful_functions import *
import codecs

with open('input.txt') as file:
    input_text = file.read()
binary_code = text_to_bits(input_text) + '1'  # add 1 to a message
b = len(binary_code) - 1  # bit length of message

while len(binary_code) % 512 != 448:
    binary_code += '0'
# print(len(binary_code))

word1 = format(b, '032b')  # add zeros to have 32 bit-lenght
word2 = format(0, '032b')
word = word1 + word2

binary_code += word

blocks = [binary_code[x:x + 512] for x in range(0, len(binary_code), 512)]
#  имеем блоки длиной 512


md4_hash = ''
for block in blocks:
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    h = [A, B, C, D]
    X = [block[x:x + 32] for x in range(0, 512, 32)]  # 16 слов X[i] в каждом блоке по 32 бита (4 байта)
    X = [int(x[::-1]) for x in X]  # каждое слово перевернул
    # Round 1
    s = (3, 7, 11, 19)
    for r in range(16):
        i = (16 - r) % 4
        k = r
        h[i] = leftrotate((h[i] + F(h[(i + 1) % 4], h[(i + 2) % 4], h[(i + 3) % 4]) + X[k]) % 2 ** 32, s[r % 4])
    # Round 2
    s = (3, 5, 9, 13)
    for r in range(16):
        i = (16 - r) % 4
        k = 4 * (r % 4) + r // 4
        h[i] = leftrotate((h[i] + G(h[(i + 1) % 4], h[(i + 2) % 4], h[(i + 3) % 4]) + X[k] + 0x5a827999) % 2 ** 32,
                          s[r % 4])
    # Round 3
    s = (3, 9, 11, 15)
    k = (0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15)
    for r in range(16):
        i = (16 - r) % 4
        h[i] = leftrotate((h[i] + H(h[(i + 1) % 4], h[(i + 2) % 4], h[(i + 3) % 4]) + X[k[r]] + 0x6ed9eba1) % 2 ** 32,
                          s[r % 4])

    for i, v in enumerate(h):
        h[i] = (v + h[i]) % 2 ** 32
        # md4_hash += str(hex(h[i])[2:])
    print([hex(i)[2:] for i in h])
    # print(list(map(hex, h)))
    md4_hash.join(map(str, h))
# print(md4_hash)

#  MD4("abc") = a448017aaf21d8525fc10ae87aa6729d
#  MD4("") =    31d6cfe0d16ae931b73c59d7e0c089c0
