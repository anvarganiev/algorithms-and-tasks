import random
import math

alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
with open('key.txt', mode='w') as file:
    key = ''.join(random.sample(alphabet, len(alphabet)))
    for i in range(len(alphabet)):
        if alphabet[i] == key[i]:
            key = ''.join(random.sample(alphabet, len(alphabet)))
            break
    file.write(key)

tb = zip(alphabet, key)
table = dict(tb)

with open('input.txt') as file:
    text = str(file.read())
    text = text.lower()


class Crypto:

    def encrypt(self):
        encrypted = [(i, k) for i in range(len(text)) for k in table.keys() if text[i] == table[k]]
        encrypted = ([el[1] for el in encrypted])
        encrypted_mes = ''.join(encrypted)

        with open('encrypted.txt', mode='w') as file:
            file.write(encrypted_mes)

    def decrypt(self):
        decrypted = [(i, k, v) for i in range(len(text)) for k, v in table.items() if text[i] == table[k]]
        decrypted = ([el[2] for el in decrypted])
        decrypted_mes = ''.join(decrypted)
        #print(decrypted_mes)

        with open('decrypted.txt', mode='w') as file:
            file.write(decrypted_mes)

    def entropy(self: str):
        character_freq = [self.count(i) for i in alphabet]
        sm = 0
        for i in range(len(alphabet)):
            sm -= character_freq[i] / len(alphabet) * math.log(character_freq[i] / len(alphabet), 2)
        print(sm)


if __name__ == '__main__':
    crypto_example = Crypto()
    crypto_example.encrypt()
    crypto_example.decrypt()
    # crypto_example.entropy(text)

    character_freq = [text.count(i) for i in alphabet]
    entrop = 0
    for i in range(len(alphabet)):
        if character_freq[i]:
            entrop -= (character_freq[i] / len(text)) * math.log((character_freq[i] / len(text)), 2)
    print('Entropy is equal:', entrop)
