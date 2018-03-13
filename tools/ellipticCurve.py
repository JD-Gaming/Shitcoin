from cipolla import cipolla
from ellipticPoint import *


class EllipticCurve(object):
    def __init__(self, a, b, q):
        """
        Creates an elliptic curve using the definition:

        y**3 = x**2 + ax + b  mod  m
        """
        self.a = a
        self.b = b
        self.q = q
        self.zero = EllipticPoint(0, 0, self)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.q == other.q

    def euclidian_gcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.euclidian_gcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modInvert(self, val):
        """
        Calculate the value of val^-1 % q.  It is defined as the value which
        when multiplied with val modulo q gives the value 1:

        val * val^-1 == 1 (mod q)
        """
        while val < 0:
            val += self.q

        g, x, y = self.euclidian_gcd(val, self.q)
        if g != 1:
            raise ValueError("No modular inverse of %d and %d exists" % (
                val, self.q))
        else:
            return x % self.q

    def modSqrt(self, val):
        """
        Calculate the square roots of val mod q, defined as the values that
        multiplied with themselves modulo q give the result val:

        x1^2 == val (mod q)
        x2^2 == val (mod q)
        """
        try:
            return cipolla(val, self.q)

        except ValueError:
            raise ValueError("Unable to find a square root of %d" % val)

    def pointsAtX(self, x):
        """
        Finds the two valid points at x == x.
        """
        ysq = (pow(x, 3, self.q) + self.a * x + self.b) % self.q
        y1, y2 = self.modSqrt(ysq)

        return EllipticPoint(x, y1, self), EllipticPoint(x, y2, self)

    def pointValidate(self, P):
        """
        Finds out if a point P can exist on the curve.
        """
        if P == self.zero:
            return True

        left = (P.y ** 2) % self.q
        right = ((P.x ** 3) + self.a * P.x + self.b) % self.q

        return left == right


def main():
    print(("There are no tests for the elliptic curve class at the "
           "moment, try the elliptic point class instead."))


if __name__ == '__main__':
    main()
