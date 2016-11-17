
# Assessment
s_box = [0x4, 0x0, 0xC, 0x3, 0x8, 0xB, 0xA, 0x9, 0xD, 0xE, 0x2, 0x7, 0x6, 0x5, 0xF, 0x1]
# Practice
# s_box = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]


def dec2bin_chunks(key_val):
    val = "{0:b}".format(key_val)
    while len(val)<16:
        val = "0"+val
    n = 4
    return [val[i:i+n] for i in range(0, len(val), n)]

def dec2bin(val, length):
    out = "{0:0b}".format(val)
    while len(out)<length:
        out = "0"+out
    return out

def bin2dec(val):
    return int(val, 2)


def substitute(in_val):
    return s_box[int(in_val)]

def do_substitution(val):
    bin_vals = dec2bin_chunks(val)
    # print dec2bin(val, 16)
    # print bin_vals
    sub_vals = [dec2bin(substitute(bin2dec(x)),4) for x in bin_vals]
    sub_vals = "".join(sub_vals)
    return bin2dec(sub_vals)

def reverse_substitute(in_val):
    return s_box.index(int(in_val))

def do_reverse_substitution(val):
    bin_vals = dec2bin_chunks(val)
    sub_vals = [dec2bin(reverse_substitute(bin2dec(x)),4) for x in bin_vals]
    sub_vals = "".join(sub_vals)
    return bin2dec(sub_vals)

def permute(val):
    a = list(dec2bin(val, 16))
    permuted_val = [a[0], a[4], a[8], a[12], a[1], a[5], a[9], a[13], a[2], a[6], a[10], a[14], a[3], a[7], a[11], a[15]]
    return bin2dec("".join(permuted_val))

def apply_subkey(val, subkey):
    return val ^ subkey

def round(val, last):
    val = do_substitution(val)
    if not last:
        val = permute(val)
    return val

def calculate_xor_profiles():
    inputs = 15

    maxs = 0
    differential_pairs = []
    for x in range(0, 15):
        for y in range(0, 15):
            s = 0
            for z in range(0, 15):
                if (s_box[z] ^ s_box[z ^ x]) == y:
                    s +=1
            if not (x==0 and y==0):
                if (maxs < s):
                    maxs = s
            differential_pairs.append((x,y,s))
    # sorted(differential_pairs, key=lambda x: x[2])
    differential_pairs.sort(key = lambda x:x[2], reverse=True)
    print differential_pairs

def check_wtf():
    vals = {}
    subkeys = []
    diff = 17
    cipher_diff = 1
    mask = 0xF
    shift = 0
    prev_key = 0xF
    with open('block.txt', 'r') as myfile:
        for line in myfile:
            (key, val) = line.split()
            vals[int(key)] = int(val)
        for subkey in range(0,15):
            prob = 0
            for plaintext in vals:
                cipher1 = vals[plaintext]
                cipher2 = vals[plaintext^diff]
                cipher1 = (cipher1 ^ ((subkey<<shift) & prev_key)) & mask
                cipher2 = (cipher2 ^ ((subkey<<shift) & prev_key)) & mask

                cipher1 = do_reverse_substitution(cipher1)
                cipher2 = do_reverse_substitution(cipher2)
                if (cipher1^cipher2)==(cipher_diff & mask):
                    prob = prob + 1
            prob = float(prob) / len(vals)
            subkeys.append((subkey, prob))
            print subkey, prob, prob*len(vals), len(vals)
    subkeys.sort(key = lambda x:x[1], reverse=True)
    print subkeys



    # for every subkey
        # for every line in block.txt
        # XOR with subkey
        # reverse substitute
        # check difference with difference in plaintext at that stage



def do_3_rounds(val):
    for x in range(0, 4):
        # print " "
        val = round(val, x>2)
        # print "Round: {0} Val: {1} Last: {2}".format(x, val, x==4)
    return val

def main():
    # print do_substitution(291)
    # print do_substitution(17767)
    # print do_substitution(33623)
    # print do_substitution(30001)
    # print do_substitution(23130)
    # print permute(61440)
    # print permute(3840)
    # print permute(240)
    # print permute(15)
    # print permute(23130)
    subkeys = [4132,  8165,  14287,  54321, 53124]
    check_wtf()
    # calculate_xor_profiles()


if __name__=="__main__":
    main()
