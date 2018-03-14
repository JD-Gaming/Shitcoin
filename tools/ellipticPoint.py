from ellipticCurve import EllipticCurve


class EllipticPoint(object):
    zero = lambda: None
    zero.x = 0
    zero.y = 0

    def __init__(self, x, y, curve=None):
        self.x = x
        self.y = y
        self.ec = curve

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __repr__(self):
        return "EllipticPoint%s" % self.__str__()

    def __eq__(self, other):
        """
        Compare two points, all params must be equal for the points to be.
        """
        # If both curves are set, compare them make sure they're equal
        try:
            if self.ec and other.ec and self.ec != other.ec:
                return False
        except AttributeError:
            pass

        return self.x == other.x and self.y == other.y

    def isValid(self):
        return self.ec.pointValidate(self)

    def order(self):
        """
        An incredibly naive function for finding the order of a generator.  It
        simply loops through all multiples to see when the result is the zero
        point, indicating that the generator has gone through its entire span.
        """
        for i in range(1, self.ec.q + 1):
            if self.multiply(i) == EllipticCurve.zero:
                return i

        raise ValueError("Unable to find the order of %s" % self.__str__())

    def negate(self):
        """
        Returns the negation of the point, i.e. the mirror point over the
        x axis:

        -(x, y) == (x, -y).
        """
        return EllipticPoint(self.x, -self.y % self.ec.q, self.ec)

    def add(self, P):
        """
        Returns the sum of this point and point P on the elliptic curve.
        """
        if self == self.zero:
            return P

        if P == self.zero:
            return self

        if self.x == P.x and (self.y != P.y or self.y == 0):
            # P1 - P1 = 0
            return self.ec.zero

        if self.x == P.x:
            tmp1 = 3 * pow(self.x, 2)
            inv = self.ec.modInvert(2 * self.y)
            slant = ((tmp1 + self.ec.a) * inv)
        else:
            slant = ((P.y - self.y) * self.ec.modInvert(P.x - self.x))

        x = (slant**2 - self.x - P.x) % self.ec.q
        y = (slant * (self.x - x) - self.y) % self.ec.q

        return EllipticPoint(x, y, self.ec)

    def multiply(self, n):
        """
        Multiplies by the double-and-add algorithm.  Needs to be iterative
        rather than recursive in order to handle really large numbers.
        """
        if n == 0:
            return self.ec.zero

        if n == 1:
            return self

        if n % 2 == 1:
            P1 = EllipticPoint(self.x, self.y, self.ec)
            P2 = EllipticPoint(self.x, self.y, self.ec)
            return P1.add(P2.multiply(n - 1))

        return self.add(self).multiply(n // 2)


def main():
    ec = EllipticCurve(2, 2, 17, EllipticPoint(0, 0))
    ep = EllipticPoint(0, 6, ec)

    expected = [
        EllipticPoint(0, 0, ec),
        EllipticPoint(0, 6, ec),
        EllipticPoint(9, 1, ec),
        EllipticPoint(6, 3, ec),
        EllipticPoint(7, 6, ec),
        EllipticPoint(10, 11, ec),
        EllipticPoint(3, 1, ec),
        EllipticPoint(13, 10, ec),
        EllipticPoint(5, 16, ec),
        EllipticPoint(16, 13, ec),
        EllipticPoint(16, 4, ec),
        EllipticPoint(5, 1, ec),
        EllipticPoint(13, 7, ec),
        EllipticPoint(3, 16, ec),
        EllipticPoint(10, 6, ec),
        EllipticPoint(7, 11, ec),
        EllipticPoint(6, 14, ec),
        EllipticPoint(9, 16, ec),
        EllipticPoint(0, 11, ec),
        EllipticPoint(0, 0, ec)
    ]

    pp = EllipticPoint(0, 0, ec)
    for i in range(0, 20):
        print("%2d: %8s / %8s - %s" % (
            i, pp, expected[i], "true" if (pp == expected[i]) else "false"))
        pp = pp.add(ep)


if __name__ == '__main__':
    main()
