"""Enter the Matrix."""
from collections import deque
from fractions import Fraction, gcd

def answer(fuel):
    unstable = []
    unstable_rows = []

    # Let's start with the unstable fractions
    for index, row in enumerate(fuel):
        rowtotal = sum(row)
        if rowtotal:    # If it's not 0!
            newrow = []
            unstable_rows.append(index)
            for item in row:
                if item:
                    newrow.append(Fraction(item, rowtotal))
                else:
                    newrow.append(0)
            unstable.append(newrow)

    if not unstable_rows:
        total = []
        for i in xrange(len(fuel)+1):
            total.append(1)
        return total

    print("Unstable rows", unstable_rows)

    if not unstable_rows:
        return
    # Let's create the matrices

    # Sub matrices; those that lead to the end
    sub_matrixQ = []
    sub_matrixR = []
    for y in xrange(len(unstable)):
        new_rowQ = []
        new_rowR = []
        for x in xrange(len(unstable[0])):
            if x in unstable_rows:
                new_rowQ.append(unstable[y][x])
            else:
                new_rowR.append(unstable[y][x])
        if new_rowQ:
            sub_matrixQ.append(new_rowQ)
        if new_rowR:
            sub_matrixR.append(new_rowR)
    print("================")
    print("Sub-matrix Q")
    for x in sub_matrixQ:
        print(x)
    print("Sub-matrix R")
    for x in sub_matrixR:
        print(x)

    sm_x = len(sub_matrixQ[0])
    sm_y = len(sub_matrixQ)

    # We're trimming identity to size of sub_matrixQ.
    # Height/Width are inverses
    identity_matrix = []
    for x in xrange(sm_y):
        identity_matrix.append([0 for _ in xrange(sm_x)])
        if x < sm_x:
            identity_matrix[x][x] = 1


    print("================")
    print("Identity-matrix")
    for x in identity_matrix:
        print(x)
    print("================")

    # Doing this prior to matrix multiplication
    pre_mult = []
    for y in xrange(sm_y):
        temp = []
        for x in xrange(sm_x):
            total_sum = identity_matrix[y][x] - sub_matrixQ[y][x]
            temp.append(total_sum)
        pre_mult.append(temp)

    print("================")
    print("Pre_mult")
    for x in pre_mult:
        print(x)
    print("================")

    testing = [[1, Fraction(-1, 2)],
        [Fraction(-4,9), 1]]


    # Inverse
    # CURRENTLY ONLY WORKS FOR 2x2
    # FIX THIS LATER

    pre_mult[0][0], pre_mult[1][1] = pre_mult[1][1], pre_mult[0][0]
    pre_mult[0][1] = pre_mult[0][1] * -1
    pre_mult[1][0] = pre_mult[1][0] * -1


    result = 1 / ((pre_mult[0][0] * pre_mult[1][1]) - (pre_mult[0][1] * pre_mult[1][0]))

    for y in xrange(len(pre_mult)):
        for x in xrange(len(pre_mult)):
            pre_mult[y][x] = result * pre_mult[y][x]
    print("================")
    print("Post_mult")
    for x in pre_mult:
        print(x)
    print("================")

    print("===========")
    print("Sub-matrix R")
    for x in sub_matrixR:
        print(x)
    print("===========")
    final = []

    for y in xrange(len(sub_matrixR)):
        row = []
        to_mult = pre_mult[y]
        for x in xrange(len(sub_matrixR[0])):
            total = 0
            for index, item in enumerate(to_mult):
                total += (sub_matrixR[index][x] * item)
            row.append(total)
        final.append(row)
    print("===========")
    numer = []
    denom = []
    print(final)
    for x in final[0]:
        denom.append(x.denominator)

    lcm = 1
    for x in denom:
        lcm = lcm * x/gcd(lcm, x)

    for x in final[0]:
        num = x.numerator
        dem = x.denominator
        if num and dem != lcm:
            num = num * (lcm/dem)
        numer.append(num)

    numer.append(lcm)

    return numer






fuel = [
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]

# fuel = [
#     [0, 2, 1, 0, 0],
#     [0, 0, 0, 3, 4],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0]]

print(answer(fuel))
