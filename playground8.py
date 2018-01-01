import math


def answer(dimensions, your_position, guard_position, distance):
    your_x = your_position[0]
    your_y = your_position[1]

    guard_x = guard_position[0]
    guard_y = guard_position[1]
    print(your_position, guard_position)
    distance_between = get_distance(your_position, guard_position)

    # Easiest cases; enough distance or not enough distance
    if distance_between > distance:
        return 0
    elif distance_between == distance:
        return 1

    # Let's get started
    answers = []

    # Angles where it should hit
    laser_x = your_x
    laser_y = your_y - distance
    answers.append((laser_x, laser_y))
    print("My position:", your_position)
    print("Laser direction:", (laser_x, laser_y))
    print("Target position:", guard_position)
    result = reflect(dimensions, your_position, (laser_x, laser_y), distance)
    print(is_on(your_position, (laser_x, laser_y), guard_position))
    print("======================")

    while laser_y != your_y:
        laser_x += 1
        laser_y = your_y - missing_angle(laser_x, distance)  # Offset
        # result = reflect(dimensions, (laser_x, laser_y), distance)

        print("My position:", your_position)
        print("Laser direction:", (laser_x, laser_y))
        print("Target position:", guard_position)
        result = reflect(dimensions, your_position, (laser_x, laser_y), distance)

        print(is_on(your_position, (laser_x, laser_y), guard_position))
        print("======================")
        answers.append((laser_x, laser_y))


    return answers

def reflect(dim, origin, laser, dist):
    # Going toward ceiling
    l1 = line(origin, laser)
    # Ceiling
    if origin[1] > laser[1]:
        print("Towards ceiling")
        # There's an offset of -1
        l2 = line((-1, -1), (0, -1))
        l3 = None
        if laser[0] == origin[0]:
            print("Straight up")
        if laser[0] > origin[0]:
            print("and to the right")
            l3 = line((dim[0]+1, -1), (dim[0]+1, 0))

        elif laser[0] < origin[0]:
            print("And to the left")
            l3 = line((0, 0), (0, dim[1]))

        if l3:
            wall_hit = intersection(l1, l3)
            print("Hits wall at", wall_hit, get_distance(origin, wall_hit))

        ceil_hit = intersection(l1, l2)
        print("Hits ceiling at", ceil_hit, get_distance(origin, ceil_hit))




    # Floor
    elif origin[1] < laser[1]:
        print("Towards floor")
    else:
        print("Straight right")


    # elif get_distance((x*dist)-0, (y*dist)-0) > dist:

# INTERSECTIONS: I'll need to learn about this later
def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False
# INTERSECTIONS OVER

def missing_angle(y, total):
    print(y, total)
    return math.sqrt((total**2) - (y**2))

def get_distance(pt1, pt2):
    # Pythagorean theorem
    x_dist = pt1[0] - pt2[0]
    y_dist = pt1[1] - pt2[1]
    return math.sqrt((x_dist**2) + (y_dist**2))

def is_on(a, b, c):
    """See if it's between a and b. x=[0], y=[1]"""
    # Use either the x or the y to see if within bounds
    if a[0] != b[0]:
        is_within = within(a[0], c[0], b[0])
    else:
        is_within = within(a[1], c[1], b[1])
    return collinear(a, b, c) and is_within

def collinear(a, b, c):
    "Return if on same line."
    return (b[0] - a[0]) * (c[1] - a[1]) == (c[0] - a[0]) * (b[1] - a[1])


def within(p, q, r):
    "Return true iff q is between p and r (inclusive)."
    return p <= q <= r or r <= q <= p




print(answer([3, 2], [1, 1], [2, 1], 4))
