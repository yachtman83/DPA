class Row:
    idx = 0

    def __init__(self, idx: int):
        self.idx = idx

    def get_idx(self):
        return self.idx

    def set_idx(self, val):
        self.idx = val


class Model(Row):

    idx, dish, quantity, start, end, balance = 0, '', '', '', '', 0

    def __init__(self, idx: int, dish: str, quantity: str, start: str, end: str, balance: int):
        super().__init__(idx)
        self.idx = idx
        self.dish = dish
        self.quantity = quantity
        self.start = start
        self.end = end
        self.balance = balance

    def __str__(self):
        return f'id: {self.idx}, Dish: {self.dish}, Quantity: {self.quantity}, ' \
               f' Start of meal: {self.start}, End of meal: {self.end}, Balance of meal: {self.balance}'

    def __repr__(self):
        return f'model(idx={self.idx},dish={self.dish},quantity={self.quantity},' \
               f'start={self.start},end={self.end},balance={self.balance})'

    def __setattr__(self, __name, __value):
        self.__dict__[__name] = __value


class Data:

    file_path = ''
    data = {}
    pointer = 0

    def __init__(self, file):
        self.file_path = file
        self.data = self.parse(file)

    def __str__(self):
        d_str = '\n'.join([str(rm) for rm in self.data])
        return f'Контейнер хранит в себе следущее:\n{d_str}'

    def __repr__(self):
        return f'Data({[repr(rm) for rm in self.data]})'

    def __iter__(self):
        return self

    def __next__(self):
        if self.pointer >= len(self.data):
            self.pointer = 0
            raise StopIteration
        else:
            self.pointer += 1
            return self.data[self.pointer - 1]

    def __getitem__(self, ite):
        if not isinstance(ite, int):
            raise TypeError('Индекс должен быть целым числом')
        if 0 <= ite < len(self.data):
            return self.data[ite]
        else:
            raise IndexError('Неверный индекс')

    def as_generator(self):
        self.pointer = 0
        while self.pointer < len(self.data):
            yield self.data[self.pointer]
            self.pointer += 1

    @staticmethod
    def parse(file):
        parsed = []
        with open(file, "r") as raw_csv:
            for line in raw_csv:
                (idx, dish, quantity, start, end, balance) = line.replace("\n", "").split(";")
                parsed.append(Model(int(idx), str(dish), str(quantity), str(start), str(end), str(balance)))
        return parsed

    def sorted_by_str(self):
        return sorted(self.data, key=lambda f: f.dish)

    def sorted_by_number(self):
        return sorted(self.data, key=lambda f: f.balance)

    def value(self, value):
        r = []
        for d in self.data:
            if d.idx > value:
                r.append(d)
        return r

    def add_record(self, dish, quantity, start, end, balance):
        self.data.append(Model(len(self.data) + 1, dish, quantity, start, end, balance))
        self.save(self.file_path, self.data)

    @staticmethod
    def save(file, new_data):
        with open(file, "w", encoding='utf-8') as f:
            for r in new_data:
                f.write(f"{r.idx},{r.dish},{r.quantity},{r.start},{r.end},{r.balance}\n")

    def print(self):
        for r in self.data:
            print(f'id: {r.idx}, dish: {r.dish}, quantity: {r.quantity}, '
                  f'start: {r.start}, end: {r.end}, balance: {r.balance}')

    @staticmethod
    def print_d(d):
        for r in d:
            print(f'id: {r.idx}, dish: {r.dish}, quantity: {r.quantity}, '
                  f'start: {r.start}, end: {r.end}, balance: {r.balance}')


data = Data("data1.csv")

# __repr__()
#print(repr(data), "\n")

# __str__()
#print(data, "\n")

# Итератор
for item in iter(data):
    print(item)
print('')
# Генератор
#for item in data.as_generator():
#    print(item)
#print('')
#data.print_d(data.sorted_by_number())  # сортировка по номеру
##print('')
#data.print_d(data.sorted_by_str())  # сортировка по имени
#print('')
#data.print_d(data.value(3))  # номер больше 3