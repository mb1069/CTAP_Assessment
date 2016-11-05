import operator

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

    def get_reg(self):
        return self.reg_val
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


def test_combined(lfsr1, lfsr2, lfsr3, num_vals):
    out = ""
    for x in range(num_vals):
        out_1 = lfsr1.shift()
        out_2 = lfsr2.shift()
        out_3 = lfsr3.shift()
        out += combine_lfsr_outputs(out_1, out_2, out_3)
    return out

def set_lfsr_key(lfsr, key_val):
    val = [int (c) for c in '{0:b}'.format(key_val)]
    while len(val)<lfsr.get_length():
        val.insert(0, 0)
    lfsr.set_reg(val)

def crack(lfsr, seq):
    length = lfsr.get_length()
    lfsr_max_key = (2**length)
    seq_len = len(seq)
    max_agreement_val = -1.0
    max_agreement_ind = -1
    f = open('l.txt', 'w')
    for x in range(0, lfsr_max_key):
        set_lfsr_key(lfsr, x)
        output = []
        for y in range(0, seq_len):
            output.append(lfsr.shift())
        agreement = calc_agreement(seq, output)
        f.write(str(x) + " " + str(agreement) + "\n")
        print x
        # print x, agreement
        if agreement>max_agreement_val:
            max_agreement_val = agreement
            max_agreement_ind = x
    f.close()
    return (x, max_agreement_ind)

def get_agreements(lfsr, seq):
    length = lfsr.get_length()
    lfsr_max_key = (2**length)
    seq_len = len(seq)
    max_agreement_val = -1.0
    max_agreement_ind = -1
    agreements = []
    for x in range(0, lfsr_max_key):
        val = [int (c) for c in '{0:b}'.format(x)]
        while len(val)<length:
            val.insert(0, 0)
        lfsr.set_reg(val)
        output = []
        for y in range(0, seq_len):
            output.append(lfsr.shift())
        agreement = calc_agreement(seq, output)
        agreements.append((x, agreement))
    return agreements

def calc_agreement(seq1, seq2):
    length = len(seq1)
    agreements = 0
    for x in range (0, length):
        if (seq1[x]==seq2[x]):
            agreements += 1
    return float(agreements)/float(length)

arr = [1,1,0,0,0,0,1]
l = Lfsr(7, [5, 6], arr)
arr1 = [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
l1 = Lfsr(11, [8, 10], arr1) # 0.749 00101101101
arr2 = [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0]
l2 = Lfsr(13, [7, 10, 11, 12], arr2) # 0.752  1110011110101

def cracker(lfsr):
    with open('stream.txt', 'r') as myfile:
        data_raw = myfile.read().replace('\n', '').replace(' ', '')
        data = [int(c) for c in data_raw]
        print crack(lfsr, data)

def crack_all(lfsrs):
    agreements = list()
    with open('stream.txt', 'r') as myfile:
        data_raw = myfile.read().replace('\n', '').replace(' ', '')
        data = [int(c) for c in data_raw]
        for index, lfsr in enumerate(lfsrs):
            agreement = get_agreements(lfsr, data)
            agreement.sort(key=operator.itemgetter(1), reverse=True)
            agreements.append([int(i[0]) for i in agreement])
        return find_all_subkeys(lfsrs, agreements, data)

def find_all_subkeys(lfsrs, agreements, data):
    agreement = -1
    depth = 5
    i = 0
    while (True):
        for k0 in range(depth):
            set_lfsr_key(lfsrs[0], agreements[0][k0])
            for k1 in range(depth):
                set_lfsr_key(lfsrs[1], agreements[1][k1])
                for k2 in range(depth):
                    set_lfsr_key(lfsrs[2], agreements[2][k2])
                    out = test_combined(lfsrs[0], lfsrs[1], lfsrs[2], len(data))
                    agreement = calc_agreement(out, data)
                    print agreements[0][k0], agreements[1][k1], agreements[2][k2], agreement
                    if (agreement==1.0):
                        return k0, k1, k2

        depth*=2

def main():
    crack_all([l, l1, l2])

# def main():
#     with open('StreamFile.txt', 'r') as myfile:
#         data_raw = myfile.read().replace('\n', '').replace(' ', '')
#         data = [int(c) for c in data_raw]
#         lfsrs = set()
#
#         keyValue = -1
#
#         for x in range (0, 128):
#             arr2 = [0,0,1,0,1,1,0,1,1,0,1]
#             l2 = Lfsr(11, [1, 10], arr2) # 0.749 00101101101
#             arr3 = [1,1,1,0,0,1,1,1,1,0,1,0,1]
#             l3 = Lfsr(13, [1, 10, 11, 13], arr3) # 0.752  1110011110101
#
#             key_val = [int (c) for c in '{0:07b}'.format(x)]
#             l1 = Lfsr(7, [1,7], key_val)
#             flag = True
#
#             for i, val in enumerate(data):
#                 l1_val = l1.shift()
#                 l2_val = l2.shift()
#                 l3_val = l3.shift()
#                 exp_val = -1
#                 if (l1_val==0 and l2_val==0 and l3_val==0 and val==0):
#                     continue
#                 elif (l1_val==0 and l2_val==0 and l3_val==1 and val==1):
#                     continue
#                 elif (l1_val==0 and l2_val==1 and l3_val==0 and val==0):
#                     continue
#                 elif (l1_val==0 and l2_val==1 and l3_val==1 and val==1):
#                     continue
#                 elif (l1_val==1 and l2_val==0 and l3_val==0 and val==0):
#                     continue
#                 elif (l1_val==1 and l2_val==0 and l3_val==1 and val==0):
#                     continue
#                 elif (l1_val==1 and l2_val==1 and l3_val==0 and val==1):
#                     continue
#                 elif (l1_val==1 and l2_val==1 and l3_val==1 and val==1):
#                     continue
#                 else:
#                     flag = False
#                     break
#             if flag:
#                 return x





if __name__ == "__main__":
    # execute only if run as the entry point into the program
    print main()
