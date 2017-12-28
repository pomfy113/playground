def answer(x, y):
    return summation(x, y)

def summation(x, y):
    # Need the difference of y
    ydif = y - 1
    xtotal = x + ydif
    #
    # Initial factorial
    factorial = xtotal * (xtotal + 1) // 2
    return str(factorial - ydif

answer(3, 2)
