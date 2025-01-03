from fibonacci import my_gen, fibonacci_element
import unittest

class TestFibonacci(unittest.TestCase):

    def test_fibonacci_element(self):
        gen = fibonacci_element()
        self.assertEqual([next(gen) for i in range(10)], [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

    def test_my_genn_1(self):
        gen = my_gen()
        self.assertEqual(gen.send(3), ['3:', 0, 1, 1])

    def test_my_genn_2(self):
        gen = my_gen()
        self.assertEqual(gen.send(5), ['5:', 0, 1, 1, 2, 3])

    def test_my_genn_3(self):
        gen = my_gen()
        self.assertEqual(gen.send(0), ['0:'])

if __name__ == '__main__':
    unittest.main()

