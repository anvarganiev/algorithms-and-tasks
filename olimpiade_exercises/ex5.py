"""
Дан массив из N целых чисел и некоторое число X.
Найдите в массиве непустой подмассив (часть массива между некоторыми индексами l и r) минимальной длины такой, что сумма его элементов не менее X.
"""
print('Input N: ')
N = int(input())

arr = []
print('Input array elements: ')

arr = input().split()

print('Enter X: ')
X = int(input())

lenght = []

if str(X) in arr:
    print(1)
else:
    for i in range(len(arr) - 1):
        temp = int(arr[i])
        for j in range(i+1, len(arr)):
            temp += int(arr[j])
            if temp >= X:
                lenght.append(j - i + 1)
                break
    print(lenght)
    if not lenght:
        print(-1)
    else:
        mx = min(lenght)
        print(mx)
