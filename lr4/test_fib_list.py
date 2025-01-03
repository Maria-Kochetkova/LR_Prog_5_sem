from fib_list import FibonacciLst
import unittest

class TestFibonacciLst(unittest.TestCase):

    def test_no_fibonacci_numbers(self):
        """Тестирование списка без чисел Фибоначчи."""
        fib_iterator = FibonacciLst([4, 6, 7, 9])
        self.assertEqual(list(fib_iterator), [])

    def test_only_fibonacci_numbers(self):
        """Тестирование списка, содержащего только числа Фибоначчи."""
        fib_iterator = FibonacciLst([0, 1, 1, 2, 3, 5, 8])
        self.assertEqual(list(fib_iterator), [0, 1, 1, 2, 3, 5, 8])

    def test_mixed_numbers(self):
        """Тестирование смешанного списка с числами Фибоначчи и без них."""
        fib_iterator = FibonacciLst([0, 1, 2, 4, 5, 6, 7, 8, 9])
        self.assertEqual(list(fib_iterator), [0, 1, 2, 5, 8])

    def test_repeated_fibonacci_numbers(self):
        """Тестирование списка с повторяющимися числами Фибоначчи."""
        fib_iterator = FibonacciLst([0, 1, 1, 2, 3, 3, 5, 8, 8, 13])
        self.assertEqual(list(fib_iterator), [0, 1, 1, 2, 3, 3, 5, 8, 8, 13])

