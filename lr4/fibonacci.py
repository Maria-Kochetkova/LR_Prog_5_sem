import functools


def fibonacci_element():
    """Генератор, возвращающий элементы ряда Фибоначчи."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def my_genn():
    """Сопрограмма для получения списка чисел Фибоначчи."""
    fib_gen = fibonacci_element()
    while True:
        number_of_fib_elem = yield
        print(number_of_fib_elem)
        fib_list = [str(number_of_fib_elem)+":"]
        for i in range(number_of_fib_elem):
            fib_list.append(next(fib_gen))
        yield fib_list

def fib_coroutine(g):
    """Декоратор для инициализации сопрограммы"""
    @functools.wraps(g)
    def inner(*args, **kwargs):
        genn = g(*args, **kwargs)
        genn.send(None)
        return genn
    return inner

my_gen = fib_coroutine(my_genn)
gen = my_gen()
