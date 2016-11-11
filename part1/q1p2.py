import operator
import math

class Lfsr:

    def __init__(self, length, taps, initial_val):
        self.taps = []
        self.length = length
        for tap in taps:
            self.taps.append(tap)
        self.reg_val = initial_val

    def calc_tap(self):
        val = self.reg_val[self.taps[0]]
        for x in self.taps[1::]:
            val = (val ^ self.reg_val[x])
        return val

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

def test_individual(lfsr, num_vals):
    out = ""
    for x in range(num_vals):
        out += str(lfsr.shift())
    return out

def combine_lfsr_outputs(out_1, out_2, out_3):
    if out_1==0 and out_2==0 and out_3==0:
        return "1"
    elif out_1==0 and out_2==0 and out_3==1:
        return "1"
    elif out_1==0 and out_2==1 and out_3==0:
        return "0"
    elif out_1==0 and out_2==1 and out_3==1:
        return "1"
    elif out_1==1 and out_2==0 and out_3==0:
        return "0"
    elif out_1==1 and out_2==0 and out_3==1:
        return "0"
    elif out_1==1 and out_2==1 and out_3==0:
        return "1"
    elif out_1==1 and out_2==1 and out_3==1:
        return "0"
    else:
        return ""


def test_combined(lfsr1, lfsr2, lfsr3, num_vals):
    out = ""
    for x in range(num_vals):
        out_1 = lfsr1.shift()
        out_2 = lfsr2.shift()
        out_3 = lfsr3.shift()
        out += combine_lfsr_outputs(out_1, out_2, out_3)
    return out

def dec2bin(length, key_val):
    val = [int (c) for c in '{0:b}'.format(key_val)]
    while len(val)<length:
        val.insert(0, 0)
    return val


def crack(lfsr, data):
    length = lfsr.get_length()
    lfsr_max_key = (2**length)
    data_len = len(data)
    max_agreement_val = -1.0
    max_agreement_ind = -1
    for x in range(0, lfsr_max_key):
        lfsr.reg_val = dec2bin(lfsr.length, x)
        output = []
        for y in range(0, data_len):
            output.append(lfsr.shift())
        agreement = abs(0.5-calc_agreement(data, output))
        if agreement>max_agreement_val:
            max_agreement_val = agreement
            max_agreement_ind = x
    return (max_agreement_ind, max_agreement_val)

def crack_with(lfsr, lfsr2, key_2, data):
    length = lfsr.get_length()
    lfsr_max_key = (2**length)
    data_len = len(data)
    max_agreement_val = -1.0
    max_agreement_ind = -1
    for x in range(1, lfsr_max_key):
        keyVal = dec2bin(length, x)
        lfsr.reg_val = keyVal[0:length]
        lfsr2.reg_val = key_2
        output = []
        for y in range(0, data_len):
            output.append(lfsr.shift()^lfsr2.shift())
        agreement = abs(0.5-calc_agreement(data, output))
        if agreement>max_agreement_val:
            max_agreement_val = agreement
            max_agreement_ind = x
    return (max_agreement_ind, max_agreement_val)

def get_agreements(lfsr, data):
    length = lfsr.get_length()
    lfsr_max_key = (2**length)
    data_len = len(data)
    max_agreement_val = -1.0
    max_agreement_ind = -1
    agreements = []
    for x in range(0, lfsr_max_key):
        val = [int (c) for c in '{0:b}'.format(x)]
        while len(val)<length:
            val.insert(0, 0)
        lfsr.set_reg(val)
        output = []
        for y in range(0, data_len):
            output.append(lfsr.shift())
        agreement = calc_agreement(data, output)
        agreements.append((x, agreement))
    return agreements

def calc_agreement(data1, data2):
    length = len(data1)
    agreements = 0
    for x in range (0, length):
        if (data1[x]==data2[x]):
            agreements += 1
    return float(agreements)/float(length)

def bin2dec(arr):
    return int("".join([str(x) for x in arr]), 2)

def crack_last(l0, l1, l2, l0_key, l2_key, data):
    keyValue = -1
    max_key_val = (2**l1.length)-1
    for x in range (0, max_key_val):
        bin_key = dec2bin(l2.length, x)
        l0.set_reg(l0_key)
        l1.set_reg(bin_key)
        l2.set_reg(l2_key)
        flag = True
        for i, val in enumerate(data):
            l0_val = l0.shift()
            l1_val = l1.shift()
            l2_val = l2.shift()
            exp_val = -1
            if combine_lfsr_outputs(l0_val, l1_val, l2_val)!=str(val):
                flag = False
                break
        if flag:
            return x


arr = [0, 1, 0, 1, 1, 0, 0]
l = Lfsr(7, [5, 6], arr)
arr1 = [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1]
l1 = Lfsr(11, [8, 10], arr1)
arr2 = [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0]
l2 = Lfsr(13, [7, 10, 11, 12], arr2)

lsrs = [l, l1, l2]


def main():
    # Read ciphertext from file
    with open('stream.txt', 'r') as myfile:
        data_raw = myfile.read().replace('\n', '').replace(' ', '')
        data = [int(c) for c in data_raw]

        key_l = crack(l, data)[0]
        print "L0: "+str(key_l)


        key_l1 = crack_with(l1, l, dec2bin(l.length, key_l), data)[0]
        print "L1: "+str(key_l1)

        print crack_with(l2, l, dec2bin(l.length, key_l), data)
        key_l2 = crack_with(l2, l, dec2bin(l.length, key_l), data)[0]
        print "L2: "+str(key_l2)


if __name__ == "__main__":
    # execute only if run as the entry point into the program
    main()
