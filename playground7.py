from fractions import Fraction

def answer(fuel):
    # prob = [[] for _ in xrange(len(fuel) + 1)]
    prob = {}
    terminal = map(lambda x: True if sum(x) == 0 else False, fuel)
    print(terminal)
    prob["denom"] = 0

    for state in fuel:
        total = sum(state)
        if total != 0:
            for index, chance in enumerate(state):
                travel(fuel, chance, index, prob, total)
    print(prob)


def travel(fuel, chance, index, prob, total):
    if index in prob:
        prob_as_float = float(chance)/total
        prob_as_fraction = Fraction(prob_as_float).limit_denominator()

        total = prob[index] + prob_as_fraction
        prob[index] = total
        prob["denom"] += 1

        return
    elif chance:
        prob_as_float = float(chance)/total
        prob_as_fraction = Fraction(prob_as_float).limit_denominator()

        prob[index] = prob_as_fraction
        prob["denom"] += 1
        travel(fuel, chance, index, prob, total)






fuel = [
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]

# fuel = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

answer(fuel)
