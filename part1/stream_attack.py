
class Lfsr:

    def __init__(self, length, taps, initial_val):
        self.taps = []
        self.length = length
        for tap in taps:
            self.taps.append(tap)
        self.reg_val = initial_val

    # Calculate the tap output for the current register value
    def calc_tap(self):
        val = self.reg_val[self.taps[0]]
        for x in self.taps[1::]:
            val = (val ^ self.reg_val[x])
        return val

    # Calculate the tap, push the value to the front of the register, and pop the last value
    def shift(self):
        new_val = self.calc_tap()
        self.reg_val = [new_val] + self.reg_val
        return self.reg_val.pop()

    def set_reg(self, new_reg_val):
        self.reg_val = new_reg_val

    def get_taps(self):
        return self.taps

    def get_length(self):
        return self.length


# Implements the given boolean function
def combine_lfsr_outputs(out_1, out_2, out_3):
    val = str(out_1) + str(out_2) + str(out_3)
    val = int(val, 2)
    sub_arr = [1, 1, 0, 1, 0, 0, 1, 0]
    return str(sub_arr[val])

# Execute the shift registers and return their combined output for the requested number of bits
def test_combined(lfsr1, lfsr2, lfsr3, num_vals):
    out = ""
    for x in range(num_vals):
        out_1 = lfsr1.shift()
        out_2 = lfsr2.shift()
        out_3 = lfsr3.shift()
        out += combine_lfsr_outputs(out_1, out_2, out_3)
    return out


# Convert a decimal value to a binary array of given length
def dec2bin(length, key_val):
    val = [int(c) for c in '{0:b}'.format(key_val)]
    while len(val) < length:
        val.insert(0, 0)
    return val


# Brute force a single LFSR by finding a subkey with maximal agreement
def crack(lfsr, data):
    length = lfsr.get_length()
    lfsr_max_key = (2 ** length)
    data_len = len(data)
    max_agreement_val = -1.0
    max_agreement_ind = -1
    for x in range(0, lfsr_max_key):
        # Reset LFSR with hypothetical subkey
        lfsr.reg_val = dec2bin(lfsr.length, x)
        output = []
        for y in range(0, data_len):
            output.append(lfsr.shift())
        # Calculate normalised agreement
        agreement = abs(0.5 - calc_agreement(data, output))
        if agreement > max_agreement_val:
            # Store best subkey so far
            max_agreement_val = agreement
            max_agreement_ind = x
    # Return best subkeys
    return max_agreement_ind, max_agreement_val


# Crack an LFSR using a known LFSR (lfsr2) and it's subkey (key_2)
def crack_with(lfsr, lfsr2, key_2, data):
    length = lfsr.get_length()
    lfsr_max_key = (2 ** length)
    data_len = len(data)
    max_agreement_val = -1.0
    max_agreement_ind = -1
    for x in range(1, lfsr_max_key):
        key_val = dec2bin(length, x)
        lfsr.reg_val = key_val[0:length]
        lfsr2.reg_val = key_2
        output = []
        for y in range(0, data_len):
            # XOR output of cracking LFSR with output from second LFSR (which has an independently checked key)
            output.append(lfsr.shift() ^ lfsr2.shift())
        agreement = abs(0.5 - calc_agreement(data, output))
        if agreement > max_agreement_val:
            # Store best subkey so far
            max_agreement_val = agreement
            max_agreement_ind = x
    # Return best subkeys
    return max_agreement_ind, max_agreement_val


# Calculate agreement of output from a single or multiple LFSR (xor'd together) with an expected output
def calc_agreement(data1, data2):
    length = len(data1)
    agreements = 0
    for x in range(0, length):
        if data1[x] == data2[x]:
            agreements += 1
    return float(agreements) / float(length)


# Convert a binary array into a decimal value
def bin2dec(arr):
    return int("".join([str(x) for x in arr]), 2)


arr = [0, 1, 0, 1, 1, 0, 0]
l = Lfsr(7, [5, 6], arr)
arr1 = [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1]
l1 = Lfsr(11, [8, 10], arr1)
arr2 = [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0]
l2 = Lfsr(13, [7, 10, 11, 12], arr2)

lsrs = [l, l1, l2]


def main():
    # Read ciphertext from file and convert to binary array
    with open('stream.txt', 'r') as myfile:
        data_raw = myfile.read().replace('\n', '').replace(' ', '')
        data = [int(c) for c in data_raw]

        key_l = crack(l, data)[0]
        print "L0: " + str(key_l)

        key_l1 = crack_with(l1, l, dec2bin(l.length, key_l), data)[0]
        print "L1: " + str(key_l1)

        key_l2 = crack_with(l2, l, dec2bin(l.length, key_l), data)[0]
        print "L2: " + str(key_l2)


if __name__ == "__main__":
    # execute only if run as the entry point into the program
    main()
