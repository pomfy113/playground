def answer(x, y):
    return summation(x, y)

def summation(x, y):
    # Need the difference
    ydif = y - 1
    xtotal = x + ydif
    # Initial factorial
    factorial = xtotal * (xtotal + 1) // 2
    return factorial - ydif
