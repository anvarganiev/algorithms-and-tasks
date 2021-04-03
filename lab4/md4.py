import struct
import random
import time
import matplotlib.pyplot as plt
import mplcyberpunk
import binascii
from numba import njit, prange

plt.style.use("cyberpunk")


class MD4:
    width = 32
    mask = 0xFFFFFFFF  # маска для умножения чисел, чтобы длина не превосходила длины маски

    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]  # A B C D

    def __init__(self, msg=None):
        """:param ByteString msg: The message to be hashed."""
        if msg is None:
            msg = b""

        self.msg = msg

        # Pre-processing: Total length is a multiple of 512 bits.
        ml = len(msg) * 8
        msg += b"\x80"  # \x80 = decimal 128
        msg += b"\x00" * (-(len(msg) + 8) % 64)  # add zeros
        msg += struct.pack("<Q", ml)  # < - little-endian, Q - integer 8 bytes

        # Process the message in successive 512-bit chunks.
        self._process([msg[i: i + 64] for i in range(0, len(msg), 64)])  # разделение на блоки

    def bytes(self):
        """:return: The final hash value as a `bytes` object."""
        return struct.pack("<4L", *self.h)  # < - little-endian

    def hexdigest(self):
        """:return: The final hash value as a hexstring."""
        return "".join(f"{value:02x}" for value in self.bytes())  # 02x для записи в hexadecimal

    def _process(self, chunks):
        for chunk in chunks:
            X, h = list(struct.unpack("<16I", chunk)), self.h.copy()

            # Round 1.
            Xi = [3, 7, 11, 19]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = n, Xi[n % 4]
                hn = h[i] + MD4.F(h[j], h[k], h[l]) + X[K]
                h[i] = MD4.lrot(hn & MD4.mask, S)

            # Round 2.
            Xi = [3, 5, 9, 13]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = n % 4 * 4 + n // 4, Xi[n % 4]
                hn = h[i] + MD4.G(h[j], h[k], h[l]) + X[K] + 0x5A827999
                h[i] = MD4.lrot(hn & MD4.mask, S)

            # Round 3.
            Xi = [3, 9, 11, 15]
            Ki = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
            for n in range(16):
                i, j, k, l = map(lambda x: x % 4, range(-n, -n + 4))
                K, S = Ki[n], Xi[n % 4]
                hn = h[i] + MD4.H(h[j], h[k], h[l]) + X[K] + 0x6ED9EBA1
                h[i] = MD4.lrot(hn & MD4.mask, S)

            self.h = [((v + n) & MD4.mask) for v, n in zip(self.h, h)]

    @staticmethod
    def F(x, y, z):
        return (x & y) | (~x & z)

    @staticmethod
    def G(x, y, z):
        return (x & y) | (x & z) | (y & z)

    @staticmethod
    def H(x, y, z):
        return x ^ y ^ z

    @staticmethod
    def lrot(value, n):
        lbits, rbits = (value << n) & MD4.mask, value >> (MD4.width - n)
        return lbits | rbits


def generate_random_string() -> str:
    letters = 'abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+={}[]:"<>?/'
    length = random.randint(2, 2)
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


# @njit(fastmath=True)
def collision_of_2_random():
    #  Exercise #3

    hashes = [bytes(generate_random_string().encode()), bytes(generate_random_string().encode())]

    hashes = [MD4(generate_random_string().encode()).hexdigest(),
              MD4(generate_random_string().encode()).hexdigest()]

    k_max = 7
    count = 0
    times = []

    for k in range(1, k_max + 1):
        start_timing = time.time()
        while hashes[0][:k] not in hashes[1]:
            count += 1
            hashes = [MD4(generate_random_string().encode()).hexdigest(),
                      MD4(generate_random_string().encode()).hexdigest()]
        print(time.time() - start_timing)
        times.append(time.time() - start_timing)
    print(f'Collision detected for hashes: \n{hashes[0]}\n{hashes[1]}\ncounter={count}')
    plt.plot(range(1, k_max + 1), times)
    mplcyberpunk.add_glow_effects()
    plt.show()


# @njit(fastmath=True, parallel=True)
def collision_of_pswd():
    #  Exercise #4

    pswd = b'password'
    hash = bytes(generate_random_string().encode())

    print(f'hash_rand = {MD4(hash).hexdigest()}, hash_pswd = {MD4(pswd).hexdigest()}')
    hash_pswd = MD4(pswd).hexdigest()
    hash_rand = MD4(hash).hexdigest()

    k_max = 5
    count = 0
    times = []

    for k in range(1, k_max + 1):
        start_timing = time.time()
        while hash_pswd[:k] not in hash_rand:
            count += 1
            hash_rand = MD4(generate_random_string().encode()).hexdigest()
            # print(hashes)
        times.append(time.time() - start_timing)
    plt.plot(range(1, k_max + 1), times)
    mplcyberpunk.add_glow_effects()
    plt.show()

    print(f'Collision detected for pswd: \n{hash_pswd}\n{hash_rand}\ncounter={count}\n')


def main():
    def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))

    # messages = [b"06-751", b'']
    # known_hashes = [
    #     "31d6cfe0d16ae931b73c59d7e0c089c0",
    #     "a448017aaf21d8525fc10ae87aa6729d",
    # ]
    #
    # print("Testing the MD4 class.")
    # print()
    #
    # for message, expected in zip(messages, known_hashes):
    #     print("Message: ", message)
    #     print("Expected:", expected)
    #     print("Actual:  ", MD4(message).hexdigest())
    #     print()

    print('Avalanche effect for "abcdef" and "abcdeh"\n', MD4(b'abcdef').hexdigest(), '\n', MD4(b'abcdea').hexdigest())

    # mes1 = text_to_bits(MD4(b'abcdef').hexdigest())
    # mes2 = text_to_bits(MD4(b'abcdeh').hexdigest())

    mes1 = "{0:08b}".format(int(MD4(b'abcdef').hexdigest(), 16))
    mes2 = "{0:08b}".format(int(MD4(b'abcdea').hexdigest(), 16))

    print(mes1, mes2)

    counter = 0
    count = sum([counter + 1 for i, j in zip(mes1, mes2) if i == j])

    print(f'Число совпадений в хешах в бинарном виде {count} при длине {len(mes1)}')

    #  Exercise #3

    # collision_of_2_random()

    #  Exercise #4

    # collision_of_pswd()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
