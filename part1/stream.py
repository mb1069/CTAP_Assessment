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
    print out

def calc_agreement(seq1, seq2):
    length = len(seq1)
    agreements = 0
    for x in range (0, length):
        if (seq1[x]==seq2[x]):
            agreements += 1
    return float(agreements)/float(length)

arr0 = [1,1,0,0,0,0,1]
l0 = Lfsr(7, [5, 6], arr0)

arr1 = [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
l1 = Lfsr(11, [8, 10], arr1)

arr2 = [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0]
l2 = Lfsr(13, [7, 10, 11, 12], arr2)

def main():
    num_vals = 25

    print "L0 output: "
    print test_individual(l0, num_vals)
    print "L2 output: "
    print test_individual(l1, num_vals)
    print "L3 output: "
    print test_individual(l2, num_vals)

    print "\nChallenge output: "
    test_combined(l0, l1, l2, num_vals)


if __name__ == "__main__":
    # execute only if run as the entry point into the program
    main()
