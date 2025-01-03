class FibonacciLst:
    def __init__(self, lst):
        """Инициализация класса с заданным списком."""
        if lst == []:
            raise ValueError("Список не должен быть пустым.")
        self.lst = lst
        self.fib_set = self.generate_fibonacci_up_to(max(lst))
        self.index = 0

    def generate_fibonacci_up_to(self, n):
        """Генерация чисел Фибоначчи до указанного предела."""
        fib_numbers = []
        a, b = 0, 1
        while a <= n:
            fib_numbers.append(a)
            a, b = b, a + b
        return set(fib_numbers)

    def __iter__(self):
        """Возврат итератора."""
        return self

    def __next__(self):
        """Возврат следующего элемента из ряда Фибоначчи."""
        while self.index < len(self.lst):
            value = self.lst[self.index]
            self.index += 1
            if value in self.fib_set:
                return value
        raise StopIteration

lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
fib_iterator = FibonacciLst(lst)
print([x for x in fib_iterator])

