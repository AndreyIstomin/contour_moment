import math
import unittest
from polynome import Polynome
from contracts import contract


class PolynomeTest(unittest.TestCase):

    @staticmethod
    @contract
    def compute_reference(poly: list, x_value: 'float|int', y_value: 'float|int'):

        return sum(k * (x_value**x_pow) * (y_value**y_pow) for k, x_pow, y_pow in poly)

    def test_simple(self):

        test_polynome = [
            [(6.0, 2, 2), (-0.5, 0, 3), (7.6, 4, 0)],
            [(5.0, 6, 3), (-77.0, 4, 0), (9.11, 3, 8)],
            [(-176, 8, 3), (11, 1, 3), (9999.0, 0, 0), (77, 1, 9)],
            [(-435, 0, 6), (0, 0, 0), (878, 1, 1)]
        ]

        test_values = [
            (1.2, 34),
            (-17, 0.1),
            (123.6, -7.9)
        ]

        for i, poly in enumerate(test_polynome):

            polynome = Polynome()

            for member in poly:
                polynome.add_member(*member)

            for x, y in test_values:

                with self.subTest(i=i, x=x, y=y):

                    self.assertTrue(math.isclose(polynome.compute(x, y), self.compute_reference(poly, x, y)),
                                    'result is not close to the reference')

    def test_multiplication(self):

        test_polynome = [
            [(6.0, 2, 2), (-0.5, 0, 3), (7.6, 4, 0)],
            [(5.0, 6, 3), (-77.0, 4, 0), (9.11, 3, 8)],
            [(-176, 8, 3), (11, 1, 3), (9999.0, 0, 0), (77, 1, 9)],
            [(-435, 0, 6), (0, 0, 0), (878, 1, 1)]
        ]

        test_values = [
            (1.2, 34),
            (-17, 0.1),
            (123.6, -7.9)
        ]

        for i, poly_1 in enumerate(test_polynome):
            for j, poly_2 in enumerate(test_polynome):

                polynome_1 = Polynome()
                polynome_2 = Polynome()

                for member in poly_1:
                    polynome_1.add_member(*member)

                for member in poly_2:
                    polynome_2.add_member(*member)

                for x, y in test_values:

                    with self.subTest(i=i, j=j, x=x, y=y):

                        self.assertTrue(math.isclose((polynome_1 * polynome_2).compute(x, y),
                                                     self.compute_reference(poly_1, x, y) *
                                                     self.compute_reference(poly_2,x, y)))

    def test_binomial_theorem(self):

        pass
        # polynome_3 = Polynome.binomial_theorem(x_coef=1.1, y_coef=2, power=2)
        #
        # def near(val, ref_val, diff=1e-6):
        #
        #     return abs(val - ref_val) < abs(ref_val * diff)
        #
        # assert near(polynome_3.compute(x, y), (1.1 * x + 2 * y)**2)

    def test_integral_x(self):
        pass


if __name__ == '__main__':

    unittest.main()


# # 6 * x**2 * y**2 - 0.5 * x**0 * y**3 + 7.6 * x**4 * y**0
# polynome_1 = Polynome().add_member(6, 2, 2).add_member(-0.5, 0, 3).add_member(7.6, 4, 0)
#
# # 7.8 * x**4 * y**1 - 0.1 * x**5 * y **2 + 32 * x**3 * y**1
# polynome_2 = Polynome().add_member(7.8, 4, 1).add_member(-0.1, 5, 2).add_member(32, 3, 1)
#
# x, y = 1, 3
#
# assert polynome_1.compute(x, y) == 6 * x**2 * y**2 - 0.5 * x**0 * y**3 + 7.6 * x**4 * y**0
#
# assert polynome_2.compute(x, y) == 7.8 * x**4 * y**1 - 0.1 * x**5 * y **2 + 32 * x**3 * y**1
#
# assert (polynome_1 * polynome_2).compute(x, y) == \
#        (6 * x**2 * y**2 - 0.5 * x**0 * y**3 + 7.6 * x**4 * y**0) * (7.8 * x**4 * y**1 - 0.1 * x**5 * y **2 + 32 * x**3 * y**1)
#
# polynome_3 = Polynome.binomial_theorem(x_coef=1.1, y_coef=2, power=2)
#
# def near(val, ref_val, diff=1e-6):
#
#     return abs(val - ref_val) < abs(ref_val * diff)
#
# assert near(polynome_3.compute(x, y), (1.1 * x + 2 * y)**2)
#
# polynome_4 = Polynome().add_member(4.7, 7, 0).add_member(3.3, 1, 2)
#
# def fun(x, y):
#
#     return 4.7 * x**8 / 8.0 + 3.3 * x * y**2
#
# assert near(polynome_4.compute_integral_x(x_begin=56.6, x_end=100.3, y_value=11.2), fun(100.3, 11.2) - fun(56.6, 11.2))
#
# x0 = 2.0
# y0 = 2.0
# dx = dy = -1.0 / math.sqrt(2.0)
#
# I_1_1 = (Polynome().add_member(x0, 0, 0).add_member(dx, 1, 0) *
#          Polynome().add_member(y0, 0, 0).add_member(dy, 1, 0)).compute_integral_x(
#     0, math.sqrt(2.0), 0)
#
# print(I_1_1)

