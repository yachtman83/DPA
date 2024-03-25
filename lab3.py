import csv

data_dict = {}
with open("data.csv", "r") as file:
    reader = csv.DictReader(file, delimiter=';')

    for row in reader:
        # Получаем значения по ключам из каждой строки
        num = row['number'] # извлечение столбца номера блюда
        start = row['t_start'] # извлечение столбца времени начала
        end = row['t_end'] # извлечение столбца времени конца смены
        balance = row['balance'] # извлечение столбца остатка
        quant = row['quantity'] # извлечение столбца количества
        name = row['dish'] # извлечение столбца названия блюда
        data_dict[num] = {'Dish': name, 'Quantity': quant, 'Start meal': start, 'End meal': end, 'Balance': balance} # загрузка извлеченной информации в словарь

def print_d(data):
    for k, v in data.items():
        print(str(k) + ' ' + "Dish: " + v['Dish'] + " Quantity: " + v['Quantity'] + " Balance: " + v['Balance'] + " Start: " + v['Start meal'] + ' End: ' + v['End meal'])


def sort1(data, name): # функция сортировки по строкову и числовому полю
    # создается новый словарь отсортированный по ключу name
    return dict(sorted(data.items(), key=lambda f: f[1][name])) # f[1] - сортирвока по значению, а не по ключу

def sort2(data, val): # функция вывода данных по параметру, в данном случае сравнение остатка, передается словарь и необходимое число,
    # выведится информация об остатке блюда которая меньше заданного числа
    for key, value in data.items(): # цикл которые перебирает по ключу и значению
        if int(value['Balance']) < val:
            print('| Dish: ' + value['Dish'] + ' | Balance: ' + value['Balance'])

def add_record(file, dict, dish, quantity, start, end, balance): # функция добавления нового объекта
    for key, value in dict.items():
        file.write(f"{key};{value['Dish']};{value['Quantity']};{value['Start meal']};{value['End meal']};{value['Balance']}\n")
    file.write(f"{len(dict)+1};{dish};{quantity};{start};{end};{balance}\n")

#print_d(data_dict)
#print(sort1(data_dict, 'Balance'))
#sort2(data_dict, 100)
file = open("data1.csv", "w")
add_record(file, data_dict, 'fu', '50', '17:55', '18:30', '0')