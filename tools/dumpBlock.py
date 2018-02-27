import math


def dumpBlock(block):
    """
    Prints a block of binary data to stdout in hexadecimal chunks for easy debugging (haha).
    """
    num_lines = int(math.ceil(len(block) / 16.))

    left = len(block)

    for line in range(num_lines):
        s = [""]
        for byte in range(min(4, left)):
            s.append("%02x" % block[16 * line + byte])
        left -= min(4, left)
        s.append(" ")

        for byte in range(min(4, left)):
            s.append("%02x" % block[16 * line + 4 + byte])
        left -= min(4, left)
        s.append(" ")

        for byte in range(min(4, left)):
            s.append("%02x" % block[16 * line + 8 + byte])
        left -= min(4, left)
        s.append(" ")

        for byte in range(min(4, left)):
            s.append("%02x" % block[16 * line + 12 + byte])
        left -= min(4, left)
        s.append(" ")

        print(''.join(s))
