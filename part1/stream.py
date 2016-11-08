class Lfsr:
    # Initialisation method for a LFSR
    def __init__(self, length, taps, initial_val):
        self.taps = []
        self.length = length
        for tap in taps:
            self.taps.append(tap)
        self.reg_val = initial_val

    # Calculates the tap value for the current LFSR's state
    def calc_tap(self):
        val = self.reg_val[self.taps[0]]
        for x in self.taps[1::]:
            val = (val ^ self.reg_val[x])
        return val

    # Calculate the tap value, shift the register and return the
    # value outputted by the register
    def shift(self):
        new_val = self.calc_tap()
        self.reg_val = [new_val] + self.reg_val
        return self.reg_val.pop()

# Implements the boolean function combining LFSR outputs
def combine_lfsr_outputs(out_1, out_2, out_3):
    val = str(out_1) + str(out_2) + str(out_3)
    val = int(val, 2)
    sub_arr = [1, 1, 0, 1, 0, 0, 1, 0]
    return str(sub_arr[val])

# Static instantiation of every LFSR
arr0 = [1,1,0,0,0,0,1]
l0 = Lfsr(7, [5, 6], arr0)

arr1 = [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
l1 = Lfsr(11, [8, 10], arr1)

arr2 = [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0]
l2 = Lfsr(13, [7, 10, 11, 12], arr2)


def main():
    # Shift and combine output of LFSR's for 25 bits
    out = ""
    for x in range(25):
        out_0 = l0.shift()
        out_1 = l1.shift()
        out_2 = l2.shift()
        out += combine_lfsr_outputs(out_0, out_1, out_2)
    print "\nChallenge output: " + str(out)


if __name__ == "__main__":
    # execute only if run as the entry point into the program
    main()
