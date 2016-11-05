class Lfsr:

    def __init__(self, length, taps, initial_val):
        self.taps = []
        self.length = length
        for tap in taps:
            self.taps.append(length-tap)
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

def crack(lfsr, seq):
    length = lfsr.get_length()
    lfsr_max_key = (2**length)-1
    seq_len = len(seq)
    max_agreement_val = -1.0
    max_agreement_ind = -1
    for x in range(0, lfsr_max_key):
        val = [int (c) for c in '{0:011b}'.format(x)]
        lfsr.set_reg(val)
        output = []
        for y in range(0, seq_len):
            output.append(lfsr.shift())
        agreement = calc_agreement(seq, output)
        if agreement>max_agreement_val:
            max_agreement_val = agreement
            max_agreement_ind = x
            print agreement, x
    return max_agreement_ind


def calc_agreement(seq1, seq2):
    length = len(seq1)
    agreements = 0
    for x in range (0, length):
        if (seq1[x]==seq2[x]):
            agreements += 1
    return float(agreements)/float(length)

l = Lfsr(7, [1, 7], [0,1,0,1,1,0,0)
arr2 = [0,0,1,0,1,1,0,1,1,0,1]
l2 = Lfsr(11, [1, 10], arr2) # 0.749 00101101101
arr3 = [1,1,1,0,0,1,1,1,1,0,1,0,1]
l3 = Lfsr(13, [1, 10, 11, 13], arr3) # 0.752  1110011110101

def cracker():
    with open('StreamFile.txt', 'r') as myfile:
        data_raw = myfile.read().replace('\n', '').replace(' ', '')
        data = [int(c) for c in data_raw]
        crack(l, data)




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
