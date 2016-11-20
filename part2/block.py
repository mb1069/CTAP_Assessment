# Convert a decimal number into a chunked 16 bit binary number, outputted in an array of chunks of 4 bits
def dec2bin_chunks(key_val):
    val = "{0:b}".format(key_val)
    while len(val) < 16:
        val = "0" + val
    n = 4
    return [val[i:i + n] for i in range(0, len(val), n)]


# Convert a decimal to a binary string of minimum length
def dec2bin(val, length):
    out = "{0:0b}".format(val)
    while len(out) < length:
        out = "0" + out
    return out


# Convert a binary value to a decimal
def bin2dec(val):
    return int(val, 2)


# Execute an s_box substitution on a 4 bit input value
def substitute(in_val):
    arr = [0x4, 0x0, 0xC, 0x3, 0x8, 0xB, 0xA, 0x9, 0xD, 0xE, 0x2, 0x7, 0x6, 0x5, 0xF, 0x1]
    return arr[int(in_val)]


# Execute an s_box submission for all 16 bits
def do_substitution(val):
    bin_vals = dec2bin_chunks(val)
    sub_vals = [dec2bin(substitute(bin2dec(x)), 4) for x in bin_vals]
    sub_vals = "".join(sub_vals)
    return bin2dec(sub_vals)


# Executes a permutation of the 16 bit value according to the provided network structure
def permute(val):
    a = list(dec2bin(val, 16))
    permuted_val = [a[0], a[4], a[8], a[12], a[1], a[5], a[9], a[13], a[2], a[6], a[10], a[14], a[3], a[7], a[11],
                    a[15]]
    return bin2dec("".join(permuted_val))


# xor a value with a subkey
def apply_subkey(val, subkey):
    return val ^ subkey


# Execute a single round of subkey mixing, substitution and optionally permutation
def do_round(val, subkey, last):
    val = apply_subkey(val, subkey)
    val = do_substitution(val)
    if not last:
        val = permute(val)
    return val


# Executes all 4 rounds of the algorithm
def do_4_rounds(val, subkeys):
    for x in range(0, 4):
        print " "
        val = do_round(val, subkeys[x], x > 2)
        print "Round: {0} Val: {2} Subkey: {1} Last: {3}".format(x, subkeys[x], val, x > 2)

    val = apply_subkey(val, subkeys[4])
    return val


def main():
    subkeys = [4132, 8165, 14287, 54321, 53124]
    print do_4_rounds(13571, subkeys)


if __name__ == "__main__":
    main()
