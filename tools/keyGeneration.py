import base58
import hashlib
import math
import struct
import sys

from ellipticPoint import EllipticPoint
from ellipticCurve import EllipticCurve


class KeySystem(object):
    def __init__(self, curve, generator, order, cofactor=1):
        self.ec = curve
        self.G = generator
        self.n = order
        self.h = cofactor

    def privateToPublic(self, private):
        if private < 1 or private >= self.n:
            raise ValueError(
                "Valid key region is 1 ... 0x%x, 0x%0x is invalid" % (
                    self.n-1, private))

        return self.G.multiply(private)

    def privateToAddress(self, private, network_version=0):
        public_point = self.privateToPublic(private)

        x_bytes = [(public_point.x & (0xffffffff << i)) >> i
                   for i in range(256-32, -32, -32)]
        y_bytes = [(public_point.y & (0xffffffff << i)) >> i
                   for i in range(256-32, -32, -32)]

        key_format = '!BIIIIIIIIIIIIIIII'
        key_struct = struct.Struct(key_format)

        full_key = key_struct.pack(
            4,
            *x_bytes,
            *y_bytes,
        )

        sha256_digest = hashlib.sha256(full_key).digest()

        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_digest)
        ripemd160_digest = ripemd160.digest()

        extended_ripemd = bytearray([network_version])
        extended_ripemd.extend(ripemd160_digest)

        sha256_checksum_1 = hashlib.sha256(extended_ripemd).digest()
        sha256_checksum_2 = hashlib.sha256(sha256_checksum_1).digest()

        checksum = sha256_checksum_2[:4]

        raw_address = bytearray([])
        raw_address.extend(extended_ripemd)
        raw_address.extend(checksum)

        b58_address = base58.b58encode(bytes(raw_address))

        return b58_address


def main(progname, argv):
    # The Koblitz curve secp256k1 used by Bitcoin et al.
    ec = EllipticCurve(
        0, 7,
        0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
        EllipticPoint(0, 0)
    )
    G = EllipticPoint(
        0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
        0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
        ec
    )
    order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    ks = KeySystem(ec, G, order)

    priv_key = int(
        '18e14a7b6a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321725', 16)
    public_key = ks.privateToPublic(priv_key)

    print("Priv hex:   %x" % priv_key)
    print("Priv dec:   %d" % priv_key)
    print("Public key: 0x%064x, 0x%064x" % (public_key.x, public_key.y))
    print("Address:    %s" % ks.privateToAddress(priv_key))


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
