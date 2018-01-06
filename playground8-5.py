import math

def answer(dimensions, you, guard, distance):
    """Begin combat protocol."""
    distance_between = get_distance(you, guard)
    # Easiest cases; enough distance or not enough distance
    if distance_between > distance:
        return 0
    elif distance_between == distance:
        return 1

    your_x = you[0]
    your_y = you[1]
    guard_x = guard[0]
    guard_y = guard[1]

    diff = [guard_x - your_x, guard_y - your_y]
    vectors = dict()

    # How big we want the sample to be
    row = 2 * (distance / dimensions[0])
    col = 2 * (distance / dimensions[1])
    # Rows
    for x in xrange(-row, row):
        for y in xrange(-col, col):
            mirror_vector = get_mirror(dimensions, x, y, you)


def get_distance(pt1, pt2):
    # Pythagorean theorem
    x_dist = pt1[0] - pt2[0]
    y_dist = pt1[1] - pt2[1]
    return math.sqrt((x_dist**2) + (y_dist**2))

def get_mirror(dim, x, y, you):
    
