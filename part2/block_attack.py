# S-box
s_box = [0x4, 0x0, 0xC, 0x3, 0x8, 0xB, 0xA, 0x9, 0xD, 0xE, 0x2, 0x7, 0x6, 0x5, 0xF, 0x1]

# Generate the reverse s-box to avoid searching through entire array for every substitution
reverse_s_box = []
for x in range(16):
    reverse_s_box.append(s_box.index(x))


# Convert a decimal value to an array of 4-bit binary chunks
def dec2bin_chunks(key_val):
    val = "{0:b}".format(key_val)
    while len(val) < 16:
        val = "0" + val
    n = 4
    return [val[i:i + n] for i in range(0, len(val), n)]


# Convert a decimal value to a binary value padded to length
def dec2bin(val, length):
    out = "{0:0b}".format(val)
    while len(out) < length:
        out = "0" + out
    return out


# Convert a binary value to decimal
def bin2dec(val):
    return int(val, 2)


# Execute a reverse s_box substitution for a single 4 bit value
def reverse_substitute(in_val):
    return reverse_s_box[in_val]


# Execute a reverse s_box substitution for the full 16 bit value
def do_reverse_substitution(val):
    bin_vals = dec2bin_chunks(val)
    sub_vals = [dec2bin(reverse_substitute(bin2dec(x)), 4) for x in bin_vals]
    sub_vals = "".join(sub_vals)
    return bin2dec(sub_vals)


# Method used to calculate XOR profile for all differential pairs
def calculate_xor_profiles():
    maxs = 0
    differential_pairs = []
    for x in range(0, 15):
        for y in range(0, 15):
            s = 0
            for z in range(0, 15):
                if (s_box[z] ^ s_box[z ^ x]) == y:
                    s += 1
            if not (x == 0 and y == 0):
                if maxs < s:
                    maxs = s
            differential_pairs.append((x, y, s))
    differential_pairs.sort(key=lambda x: x[2], reverse=True)
    print differential_pairs


# Method to find most agreeable subkey for a given s-box, plaintext difference and ciphertext difference pair
def crack_section_subkey(plain_diff, cipher_diff, shift):
    mask = 0xF << shift
    vals = {}
    subkeys = []
    with open('block.txt', 'r') as myfile:
        for line in myfile:
            (key, val) = line.split()
            vals[int(key)] = int(val)
        for subkey in range(0, 15):
            prob = 0
            for plaintext in vals:
                cipher1 = vals[plaintext]
                cipher2 = vals[plaintext ^ plain_diff]
                # Shift subkey to correct index, xor to cipher text and mask to find agreement over only those 4 bits
                cipher1 = (cipher1 ^ (subkey << shift)) & mask
                cipher2 = (cipher2 ^ (subkey << shift)) & mask

                cipher1 = do_reverse_substitution(cipher1)
                cipher2 = do_reverse_substitution(cipher2)
                if (cipher1 ^ cipher2) == (cipher_diff & mask):
                    prob += 1
            prob = float(prob) / len(vals)
            subkeys.append((subkey, prob))
    subkeys.sort(key=lambda x: x[1], reverse=True)
    return subkeys[0]


def main():
    crack = crack_section_subkey(12, 12288, 12)
    print "Bits 1..4: value:    {0},    prob:  {1}".format(crack[0], crack[1])
    crack = crack_section_subkey(13, 768, 8)
    print "Bits 5..8: value:    {0},    prob:  {1}".format(crack[0], crack[1])
    crack = crack_section_subkey(2, 48, 4)
    print "Bits 9..12: value:   {0},    prob:  {1}".format(crack[0], crack[1])
    crack = crack_section_subkey(17, 1, 0)
    print "Bits 13..16: value:  {0},    prob:  {1}".format(crack[0], crack[1])


if __name__ == "__main__":
    main()
