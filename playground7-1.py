"""Enter the Matrix."""
from collections import deque
from fractions import Fraction

def answer(fuel):
    terminal = []
    unstable = []
    matrix = []
    # Let's start with the unstable fractions
    for row in fuel:
        rowtotal = sum(row)
        if rowtotal:    # If it's not 0!
            newrow = []
            for item in row:
                if item:
                    newrow.append(Fraction(item, rowtotal))
                else:
                    newrow.append(0)
            unstable.append(newrow)
        # else:
        #     # There's no way out of these ones
        #     terminal.append(row)
        #     term_x = len(terminal) - 1
        #     terminal[term_x][term_x] = 1
    # Let's create the matrices

    # Sub matrices; those that lead to the end
    sub_matrix = []
    for x in unstable:
        sub_matrix.append(x[-len(unstable):])

    sm_x = len(sub_matrix[0])
    sm_y = len(sub_matrix)

    # We're trimming identity to size of sub_matrix.
    # Height/Width are inverses
    identity_matrix = []
    for x in xrange(sm_y):
        identity_matrix.append([0 for _ in xrange(sm_x)])
        if x < sm_x:
            identity_matrix[x][x] = 1


    print(sub_matrix)
    print(identity_matrix)
    print("================")

    probabilities = []
    for y in xrange(sm_y):
        temp = []
        for x in xrange(sm_x):
            total_sum = identity_matrix[x][y] - sub_matrix[x][y]
            temp.append(total_sum)
        probabilities.append(temp)
    print(probabilities)


    # for y in xrange(unstable_y):
    #     temp = []
    #     for x in xrange(terminal_x, unstable_x):
    #         print(terminal[y][x], unstable[y][x])
    #         new_sum = terminal[y][x] - unstable[y][x]
    #         temp.append(new_sum)
    #     sub_matrix.append(temp)
    # print(sub_matrix)


    # for x in terminal:
    #     print(x)
    # for x in unstable:
    #     print(x)



fuel = [
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]

answer(fuel)
