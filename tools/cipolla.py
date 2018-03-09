def legendre(n, p):
    return pow(n, ((p - 1) // 2), p)


def isSquare(n, p):
    return legendre(n, p) == 1


def mulPt(p1, p2, omega, p):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    x = (x1*x2 + (y1*y2 * omega)) % p
    y = (x1*y2 + x2*y1) % p

    return (x, y)


def cipolla(n, p):
    if not isSquare(n, p):
        raise ValueError("No square exists")

    a = 2

    while True:
        omega_sq = (a**2 + p - n) % p
        if legendre(omega_sq, p) == p-1:
            break

        a += 1

    final_omega = omega_sq

    r = (1, 0)
    s = (a, 1)

    nn = ((p + 1) // 2) % p

    while nn > 0:
        if nn & 1:
            r = mulPt(r, s, final_omega, p)

        s = mulPt(s, s, final_omega, p)
        nn //= 2

    if r[1] != 0:
        return (0, 0)

    if pow(r[0], 2, p) != n:
        return (0, 0)

    return r[0], p - r[0]


def main():
    p = 13
    n = 10

    l = [(10, 13),
         (56, 101),
         (8218, 10007),
         (8219, 10007),
         (331575, 1000003),
         (665165880, 1000000007),
         (881398088036, 1000000000039),
         (34035243914635549601583369544560650254325084643201, 10**50+151)]

    for (n, p) in l:
        try:
            print("%d %% %d: %s" % (n, p, cipolla(n, p)))
        except Exception as e:
            print(str(e))
            print("%d %% %d: False" % (n, p))


if __name__ == '__main__':
    main()
