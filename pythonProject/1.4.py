import math
#n = int(input("Введите количество элементов массива: ")) # ввод количество элементов
#my_arr = [];                                             # объявление массива
#for i in range (n):                                      # цикл для того чтобы заполнить массив
#    my_arr.append(int(input("Введите элемент массива: "))) # функция append для того чтобы заполнить массив (заполняется с конца)
#print(my_arr)

def quick_sort(arr, left, right): # менеджер
    if left < right:
        pivot_index = partition(arr, left, right) # вызов функции partition чтобы узнать индекс опорного элемента
        quick_sort(arr, left, pivot_index - 1) # рекурсивно вызываем функцию и передаем левую часть подмассива (опорный элемент не трогаем)
        quick_sort(arr, pivot_index + 1, right) # рекурсивно вызываем функцию и передаем правую часть подмассива (опорный элемент не трогаем)


def partition(arr, left, right):
    i = left
    j = right - 1
    pivot = arr[right] # в качестве опорного элемента берем последний элемент

    while i < j:
        while i < right and arr[i] < pivot: # i идёт с начала массива и ищет элемент больше опорного,
            i += 1                          # если на текущей итерации не находит, то увеливается на 1
        print("i", i, arr[i])
        while j > left and arr[j] >= pivot:
            #print("j", j, arr[j])
            j -= 1
        print("j", j, arr[j])
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
    if arr[i] > pivot:
        arr[i], arr[right] = arr[right], arr[i]
    print(arr)
    return i
arr = [22, 11, 88, 66, 55, 77, 33, 44]
partition(arr, 0, len(arr) - 1)
partition(arr, 0, 1)
