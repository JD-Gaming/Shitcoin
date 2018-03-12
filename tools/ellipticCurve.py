import numpy as np

from cipolla import cipolla


class EllipticPoint(object):
    def __init__(self, x, y):
        """
        Defines a point on an elliptic curve.
        """
        self.x = x
        self.y = y

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __repr__(self):
        return "EllipticPoint%s" % self.__str__()


class EllipticCurve(object):
    Zero = EllipticPoint(0, 0)

    def __init__(self, a, b, q):
        """
        Creates an elliptic curve using the definition:

        y**3 = x**2 + ax + b  mod  m
        """
        self.a = a
        self.b = b
        self.q = q

        # Validate?  (4 * (a ** 3) + 27 * (b **2)) % q != 0

    def euclidian_gcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.euclidian_gcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(self, a):
        while a < 0:
            a += self.q

        g, x, y = self.euclidian_gcd(a, self.q)
        if g != 1:
            raise ValueError("No modular inverse of %d and %d exists" % (a, self.q))
        else:
            return x % self.q

    def invert(self, val):
        t = 0
        r = self.q
        new_t = 1
        new_r = val

        while new_r != 0:
            quotient = r // new_r
            (t, new_t) = (new_t, t - quotient * new_t)
            (r, new_r) = (new_r, r - quotient * new_r)

        if r > 1:
            raise ValueError("Unable to invert %d (%d)" % (val, r))

        while t < 0:
            t += self.q

        return t

    def sqrt(self, val):
        try:
            return cipolla(val, self.q)

        except ValueError:
            raise ValueError("Unable to find a square root of %d" % val)

    def pointOrder(self, G):
        for i in range(1, self.q + 1):
            if self.pointMultiply(G, i) == EllipticCurve.Zero:
                return i

        raise ValueError("Unable to find the order of %s" % G)

    def pointsAtX(self, x):
        ysq = (pow(x, 3, self.q) + self.a * x + self.b) % self.q
        y1, y2 = self.sqrt(ysq)

        return EllipticPoint(x, y1), EllipticPoint(x, y2)

    def pointValidate(self, P):
        if P == self.Zero:
            return True

        left = (P.y ** 2) % self.q
        right = ((P.x ** 3) + self.a * P.x + self.b) % self.q

        return left == right

    def pointNegate(self, P):
        return EllipticPoint(P.x, -P.y % self.q)

    def pointAdd(self, P1, P2):
        """
        Returns the sum of points P1 and P2 on the elliptic curve.
        """
        if P1 == EllipticCurve.Zero:
            return P2
        if P2 == EllipticCurve.Zero:
            return P1
        if P1.x == P2.x and (P1.y != P2.y or P1.y == 0):
            # P1 - P1 = 0
            return EllipticCurve.Zero
        if P1.x == P2.x:
            tmp1 = 3 * pow(P1.x, 2)
            #inv = self.invert(2 * P1.y)
            inv = self.modinv(2 * P1.y)
            slant = ((tmp1 + self.a) * inv)
        else:
            #slant = ((P2.y - P1.y) * self.invert(P2.x - P1.x))
            slant = ((P2.y - P1.y) * self.modinv(P2.x - P1.x))

        x = (slant**2 - P1.x - P2.x) % self.q
        y = (slant * (P1.x - x) - P1.y) % self.q

        return EllipticPoint(x, y)

    def pointMultiply(self, P, n):
        """
        Multiplies by the double-and-add algorithm.  Needs to be iterative
        rather than recursive in order to handle 256 bit numbers.
        """
        if n == 0:
            return EllipticCurve.Zero

        if n == 1:
            return P

        if n % 2 == 1:
            return self.pointAdd(P, self.pointMultiply(P, n - 1))

        return self.pointMultiply(self.pointAdd(P, P), n // 2)


def bitcoinTest():
    # Bitcoin curve
    ec = EllipticCurve(0, 7,
            0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F)  # noqa

    Pp = ec.pointsAtX(3)
    print(ec.pointMultiply(Pp[0], 3).x)
    print(ec.pointAdd(Pp[0], ec.pointAdd(Pp[0], Pp[0])).x)

    Pp = ec.pointsAtX(
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364146)
    print(ec.pointMultiply(
        Pp[0], 0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC20).x)

    for i in range(1000):
        if not ec.pointValidate(ec.pointMultiply(Pp[0], 0x1 << i)):
            print("Failed at 1 << %d" % i)


def smallTest():
    ec = EllipticCurve(2, 2, 17)
    P = EllipticPoint(0, 6)

    img = np.ones((17, 17), dtype=np.uint8)

    for i in range(1, 20):
        pp = ec.pointMultiply(P, i)
        print("%2d: %s" % (i, pp))
        img[pp.y, pp.x] = 0

    print(img)

    expected = [
        EllipticPoint(0, 0),
        EllipticPoint(0, 6),
        EllipticPoint(9, 1),
        EllipticPoint(6, 3),
        EllipticPoint(7, 6),
        EllipticPoint(10, 11),
        EllipticPoint(3, 1),
        EllipticPoint(13, 10),
        EllipticPoint(5, 16),
        EllipticPoint(16, 13),
        EllipticPoint(16, 4),
        EllipticPoint(5, 1),
        EllipticPoint(13, 7),
        EllipticPoint(3, 16),
        EllipticPoint(10, 6),
        EllipticPoint(7, 11),
        EllipticPoint(6, 14),
        EllipticPoint(9, 16),
        EllipticPoint(0, 11),
        EllipticPoint(0, 1),
    ]
    pp = EllipticCurve.Zero
    for i in range(1, 20):
        pp = ec.pointAdd(pp, P)
        print("%2d: %8s / %8s" % (i, pp, expected[i]))


def main():
    smallTest()


if __name__ == '__main__':
    main()
