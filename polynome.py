import math
from collections import defaultdict
from scipy.special import binom
from contracts import contract


class Polynome:

    def __init__(self):

        self._members = defaultdict(float)

    @contract
    def add_member(self, coef: 'float|int', pow_x: 'int,>=0,<=10', pow_y: 'int,>=0,<=10'):

        self._members[(int(pow_x), int(pow_y))] += coef

        return self

    def __mul__(self, other):

        if not isinstance(other, Polynome):
            raise TypeError

        result = Polynome()

        for (pow_x1, pow_y1), coef1 in self._members.items():

            for (pow_x2, pow_y2), coef2 in other._members.items():

                result._members[(pow_x1 + pow_x2, pow_y1 + pow_y2)] += coef1 * coef2

        return result

    def compute(self, x_value, y_value):

        if not len(self._members):

            return 0

        return sum(((x_value ** pow_x) * (y_value ** pow_y) * coef for (pow_x, pow_y), coef in self._members.items()))

    @classmethod
    @contract
    def binomial_theorem(cls, x_coef: 'float|int', y_coef: 'float|int', power: 'int,>=0,<=10'):

        """
        Returns (x_coef x + y_coef y) ^ power in form of PolynomialRepresentation
        """

        instance = cls()
        n = power
        instance._members = defaultdict(
            float, {(n - i, i): binom(n, n - i) * x_coef ** (n - i) * y_coef**i for i in range(n + 1)})

        return instance

    def integral_x(self):

        instance = Polynome()

        instance._members = defaultdict(
            float, {(pow_x + 1, pow_y): 1.0 / (pow_x + 1.0) * k for (pow_x, pow_y), k in self._members.items()})

        return instance

    def compute_integral_x(self, x_begin, x_end, y_value):

        integral = self.integral_x()
        return integral.compute(x_value=x_end, y_value=y_value) - integral.compute(x_value=x_begin, y_value=y_value)


if __name__ == '__main__':

    # 6 * x**2 * y**2 - 0.5 * x**0 * y**3 + 7.6 * x**4 * y**0
    polynome_1 = Polynome().add_member(6, 2, 2).add_member(-0.5, 0, 3).add_member(7.6, 4, 0)

    # 7.8 * x**4 * y**1 - 0.1 * x**5 * y **2 + 32 * x**3 * y**1
    polynome_2 = Polynome().add_member(7.8, 4, 1).add_member(-0.1, 5, 2).add_member(32, 3, 1)

    x, y = 1, 3

    assert polynome_1.compute(x, y) == 6 * x**2 * y**2 - 0.5 * x**0 * y**3 + 7.6 * x**4 * y**0

    assert polynome_2.compute(x, y) == 7.8 * x**4 * y**1 - 0.1 * x**5 * y **2 + 32 * x**3 * y**1

    assert (polynome_1 * polynome_2).compute(x, y) == \
           (6 * x**2 * y**2 - 0.5 * x**0 * y**3 + 7.6 * x**4 * y**0) * \
           (7.8 * x**4 * y**1 - 0.1 * x**5 * y **2 + 32 * x**3 * y**1)

    polynome_3 = Polynome.binomial_theorem(x_coef=1.1, y_coef=2, power=2)

    def near(val, ref_val, diff=1e-6):

        return abs(val - ref_val) < abs(ref_val * diff)

    assert near(polynome_3.compute(x, y), (1.1 * x + 2 * y)**2)

    polynome_4 = Polynome().add_member(4.7, 7, 0).add_member(3.3, 1, 2)

    def fun(x, y):

        return 4.7 * x**8 / 8.0 + 3.3 * x * y**2

    assert near(polynome_4.compute_integral_x(x_begin=56.6, x_end=100.3, y_value=11.2),
                fun(100.3, 11.2) - fun(56.6, 11.2))

    x0 = 2.0
    y0 = 2.0
    dx = dy = -1.0 / math.sqrt(2.0)

    I_1_1 = (Polynome().add_member(x0, 0, 0).add_member(dx, 1, 0) *
             Polynome().add_member(y0, 0, 0).add_member(dy, 1, 0)).compute_integral_x(
        0, math.sqrt(2.0), 0)

    print(I_1_1)
