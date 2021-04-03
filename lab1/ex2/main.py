# 3 вариант текста
import matplotlib.pyplot as plt
import mplcyberpunk
import math

plt.style.use('cyberpunk')

alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '
#freq_alphabet = ' оеаинтсрвлкмдпуяыьгзбчйхжшюцщэфёъ'
freq_alphabet = ' оеаНИтсВДРЛУГКБМЧЯXПЬЫШЗжЙюцщФЭёъ'
freq_alphabet = freq_alphabet.lower()

with open('input.txt') as file:
    text = file.read()
    text = text.lower()


def freq_analysis(input_text: str) -> None:
    character_freq = [input_text.count(i) for i in alphabet]
    table = dict(zip(alphabet, character_freq))  # словарь{буква_алфавита: частота_в_шифротексте}
    print(table)

    table1 = list(table.items())

    table1.sort(key=lambda i: i[1], reverse=True)  # словарь в список с сортировкой по value
    table1 = [x[0] for x in table1]

    # словарь {буква_в_частотном алфавите : буква_алфавита_с_макс_частотой }
    new_table = dict(zip(table1, freq_alphabet))  # словарь {шифр_символ: настоящий_символ}
    print(new_table)

    table2 = list(table.items())
    table2.sort(key=lambda i: i[1], reverse=True)
    table2 = [x[1] for x in table2]

    plt.bar(table.keys(), table.values(), width=0.7)
    plt.show()
    plt.bar(new_table.keys(), table2, width=0.7)
    mplcyberpunk.make_lines_glow()
    mplcyberpunk.add_underglow()
    plt.show()

    # output_text = [(i, char) for i in len(text) for char in text ]
    '''
    Теперь надо заменить буквы в input.txt по словарю new_table:
    если буква = ключу словаря, то заменяем ее на значение словаря
    '''

    new_table = list(new_table.items())
    print(new_table)
    new_text = ''

    for i in text:
        for j in new_table:
            if i in j and i == j[0]:
                i = j[1]
                new_text += i
                break

    with open('output.txt', mode='w') as file:
        file.write(new_text)


def entropy(str: text) -> None:
    character_freq = [text.count(i) for i in alphabet]
    sm = 0
    for i in range(len(alphabet)):
        if character_freq[i]:
            sm -= character_freq[i] / len(text) * math.log(character_freq[i] / len(text), 2)
    print(sm)


if __name__ == '__main__':
    freq_analysis(text)
    entropy(list(text))

