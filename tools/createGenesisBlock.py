import hashlib
import math
import struct
import sys

from dumpBlock import dumpBlock
from createGenericBlock import genericBlock


def genesisBlock(block_chain_identifier,
                 max_block_size,
                 difficulty,
                 seconds_between_blocks,
                 blocks_between_negotiation):
    chain_id_parts = [(block_chain_identifier & (0xffffffff << i)) >> i for i in range(256-32, -32, -32)]

    payload_format_str = '!IIIIIIIIIIII'
    payload_format = struct.Struct(payload_format_str)
    payload = payload_format.pack(
        *chain_id_parts,
        max_block_size,
        difficulty,
        seconds_between_blocks,
        blocks_between_negotiation)

    return genericBlock(1,
                        0,
                        0,
                        0,
                        timestamp=1519846381,
                        payload=payload)


def main(progname, argv):
    hash_obj = hashlib.sha256(b"DanielJonatanShitcoin")
    block_chain_identifier = int.from_bytes(hash_obj.digest(), byteorder='big')

    b = genesisBlock(block_chain_identifier,
                     0x200000,  # 2 MiB initial size
                     1,  # Not very difficult at all
                     600,  # The traditional ten minute block
                     1008)  # One week
    dumpBlock(b)


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
