import math

def answer(pellets):
    number = int(pellets)
    accumulator = 0
    # I really wish I had case
    while number != 1:
        # If even, we can just cut it
        if number % 2 == 0:
            number = number / 2
        # If subtracting 1 allows multicut, probably beats adding
        elif number % 4 == 1:
            number = number - 1
        # 3, why are you so weird
        elif number == 3:
            number = number - 1
        # Otherwise, just add?
        else:
            number += 1
        accumulator += 1

    return(accumulator)

print(answer("96"))
