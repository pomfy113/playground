"""Enter the Matrix."""
from collections import deque
from fractions import Fraction

def answer(fuel):
    terminal = []
    unstable = []
    unstable_rows = []
    matrix = []
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

    print("Unstable rows", unstable_rows)

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
            total_sum = identity_matrix[x][y] - sub_matrixQ[x][y]
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

    print(pre_mult)


    result = 1 / ((pre_mult[0][0] * pre_mult[1][1]) - (pre_mult[0][1] * pre_mult[1][0]))

    for y in xrange(len(pre_mult)):
        for x in xrange(len(pre_mult)):
            pre_mult[y][x] = result * pre_mult[y][x]
    print(pre_mult)


    final = []

    # for y in xrange(len(sub_matrixR)):
    #     row = []
    #     for x in xrange(len(sub_matrixR[0])):
    #         # print(x, y)
    #         total = pre_mult[y][x] * sub_matrixR[x][y]
    #         row.append(total)
    #     final.append(row)







fuel = [
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]

answer(fuel)
