import hashlib
import math
import struct
import sys
import time

from dumpBlock import dumpBlock


def genericBlock(version,
                 previous_block_id, nonce,
                 block_type,
                 timestamp=None,
                 payload=bytes()):
    if timestamp is None:
        timestamp = time.time()

    length = (
        2 +  # Version
        256 // 8 +  # Block ID
        2 * 256 // 8 +  # Previous block ID and nonce
        2 +  # Block type
        8 +  # Timestamp
        4 +  # Block size
        len(payload))

    # Everything is network byte order, aka big endian
    previous_parts = [(previous_block_id & (0xffffffff << i)) >> i
                      for i in range(256-32, -32, -32)]
    nonce_parts = [(nonce & (0xffffffff << i)) >> i
                   for i in range(256-32, -32, -32)]

    header_format_str = ('!IIIIIIII' +  # Previous block in 32 bit chunks
                         'IIIIIIII' +  # Nonce in 32 bit chunks
                         'HQI')  # Block type, timestamp and block length
    header_format = struct.Struct(header_format_str)
    header = header_format.pack(
        # Previous block ID, split into parts because it's loong
        *previous_parts,
        # Nonce, split into parts because it's loong
        *nonce_parts,
        # Block type
        block_type,
        # Timestamp as seconds since epoch in 64 bit
        int(timestamp),
        # Block size
        length
    )

    version_format_str = '!H'
    version_format = struct.Struct(version_format_str)
    version = version_format.pack(1)

    hash_object = hashlib.sha256(version + header + payload)
    hash_value = hash_object.digest()

    block = bytes(version) + bytes(hash_value) + bytes(header) + bytes(payload)

    return block


def main(progname, argv):
    b = genericBlock(1,
                     0x0000000011111111222222223333333344444444555555556666666677777777,
                     0x8888888899999999aaaaaaaabbbbbbbbccccccccddddddddeeeeeeeeffffffff,
                     0,
                     payload=bytearray([x for x in range(256)]))

    dumpBlock(b)


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
