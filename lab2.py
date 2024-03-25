import copy
import random
import numpy as np

n = int(input("Введите N: ")) # ввод размерности матрицы
m = int(input("Введите M: "))
matrix = [] # list для элементов массива


def no_numpy_random(matrix):
    for _ in range(n):
        row = []
        for _ in range(m):
            value = random.randint(0, 1)
            row.append(value)
        matrix.append(row)

def numpy_random(n, m): # функция для загрузки матрицы случайными величинами
    matrix = np.random.randint(0, 2, size=(n, m)) #Аргументы: low, high, size: от какого, до какого числа (randint не включает в себя это число, поэтому 2)
    return matrix.tolist() # конвертация в тип list, дабы на дальнейших этапах не возникали проблемы с типами переменных

def find_even(matrix):
    for row in matrix: # Подсчитываем количество единиц в текущей строке
        count = row.count(1)
        print(row, count)
        # Если количество единиц нечетное, добавляем единицу в конец строки иначе 0
        if count % 2 != 0:
            row.append(1)
        else:
            row.append(0)

def print_matrix(matrix): #функция для отображения в консоле матрицы в виде таблицы
    for row in matrix: # цикл строки в матрице
        for value in row: # цикл значений в строке
            print(value, end=" ")
        print()


def save_matrix_to_file(matrix, processed_matrix): # функции для записи в файл результатов
    with open('matrix.txt', 'w') as file: # открытие файла для записи
        file.write("Исходная матрица:\n") # запись информации
        for row in matrix:
            file.write(" ".join(str(value) for value in row)) # объединение значений, конвертируемых в тип str в одну строку
            file.write("\n")

        file.write("\nМатрица после обработки:\n")
        for row in processed_matrix:
            file.write(" ".join(str(value) for value in row))
            file.write("\n")

matrix = numpy_random(n, m) # загрузка в матрицу случайных значений
print_matrix(matrix) # вывод матрицы
res_matrix = copy.deepcopy(matrix) #изменения, внесенные в `res_matrix`, не будут влиять на `matrix` c помощью модуля copy и функции deepcopy
find_even(res_matrix) # вызов функции по анализу матрицы на предмет чётных кол-во 1
print_matrix(res_matrix)

save_matrix_to_file(matrix, res_matrix) # запись результатов в файл