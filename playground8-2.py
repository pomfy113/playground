import math
from decimal import Decimal

def line(p1, p2):
    """Grab the... somethings."""
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

# The lines and their factors
# Testing something out with boundaries
# CEILING = line((-1, -1), (0, -1))
# WALL_L = line((-1, -1), (-1, 0))
# WALL_R = None
# FLOOR = None

CEILING = line((0,0), (1,0))
WALL_L = line((0,0), (0, 1))
WALL_R = None
FLOOR = None


def answer(dimensions, your_position, guard_position, distance):
    """Begin combat protocol."""
    global YOUR, GUARD
    global WALL_R, FLOOR
    WALL_R = line((dimensions[0], 0.0), (dimensions[0], 10.0))
    FLOOR = line((0.0, dimensions[1]), (10.0, dimensions[1]))
    global DIST

    DIST = distance

    YOUR = tuple(your_position)
    GUARD = tuple(guard_position)

    your_x = your_position[0]
    your_y = your_position[1]
    guard_x = guard_position[0]
    guard_y = guard_position[1]

    distance_between = get_distance(your_position, guard_position)

    # Easiest cases; enough distance or not enough distance
    if distance_between > distance:
        return 0
    elif distance_between == distance:
        return 1

    # Let's get started
    test_set = set()
    quadrant = set()
    slopes = set()
    quadrant.add((0,1))
    quadrant.add((1,0))

    row = (dimensions[0] / 2) + 3
    col = (dimensions[1] / 2) + 3

    # One quadrant
    for x in xrange(1, row):
        for y in xrange(1, col):
            # print("Initial", x, y)
            if x % 2 == 0 and y % 2 == 0:
                if Decimal(y)/x not in slopes:
                    slopes.add(Decimal(y)/x)
                    quadrant.add((x / 2, x / 2))
            elif Decimal(y)/x not in slopes:
                slopes.add(Decimal(y)/x)
                quadrant.add((x, y))

    # Other three
    for item in quadrant:
        test_set.add(item)
        test_set.add((-item[0], item[1]))
        test_set.add((item[0], -item[1]))
        test_set.add((-item[0], -item[1]))



    print("")
    print(test_set)

    # test_set = [(21, -30), (35, -50), (53, 60), (49, -70), (-67, -50), (7, -10), (53, -50), (-67, 60), (7, -50), (63, -90)]


    answers = set()
    for item in test_set:
        answers.add((float(your_position[0]+item[0]), float(your_position[1]+item[1])))


    # test_set = ((35,-250), (0,0))
    # test_set = ((7,60), (0,0))

    final = []
    for item in test_set:
        print("My position:", YOUR)
        print("Laser direction:", item)
        print("Target position:", GUARD)

        result = reflect(dimensions, YOUR, (float(item[0]+your_position[0]), float(item[1]+your_position[1])), distance)
        print(result)
        if result:
            final.append(item)
        print("==============================================================")
    print(len(final))
    print("Answers should have [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]")
    print("TESTING", collinear((164.583, 275), (196.666, 0), (179.166, 150)))
    return final

def reflect(dim, origin, laser, dist):
    # Going toward ceiling
    laser_line = line(origin, laser)
    print(" ")
    print("New distances, max", dist, DIST)
    print("Origin, laser, guard", origin, laser, GUARD)
    guard_hit = collinear(origin, laser, GUARD)
    you_hit = collinear(origin, laser, YOUR)
    if origin == laser:
        print("Suicide is not the answer")
        return False

    # The only way you get it on first hit is if already aligned
    if dist == DIST:
        if guard_hit:
            if laser[0] < origin[0] < GUARD[0] or laser[0] > origin[0] > GUARD[0] or\
               laser[1] < origin[1] < GUARD[1] or laser[1] > origin[1] > GUARD[1]:
                print("It's on the opposite end!")
            else:
                print("First shot!")
                return True
    # Otherwise, play normally
    else:
        if you_hit and guard_hit:
            print("Both got hit!")
            # Guard is closer
            if get_distance(origin, YOUR) > get_distance(origin, GUARD):
                # Make sure we have enough space to hit the guy
                if get_distance(origin, GUARD) <= dist:
                    print("* * * * * * * WE GOT THE OTHER GUY FIRST * * * * * * * * *")
                    return True
                else:
                    print("Too far.")
                    return False
            # You're closer
            else:
                print("Uh oh")
                return False
        elif guard_hit:
            if get_distance(origin, GUARD) <= dist:
                print("* * * * * * * WE GOT IT * * * * * * * * *")
                return True
            else:
                print("Way too far")
                return False
        elif you_hit:
            print("YOU GOT SHOT")
            return False




    if dist <= 0:
        print("Out of distance")
        return


    # See if floor or ceiling
    if origin[1] == laser[1]:
        vert_line = None
    elif origin[1] > laser[1]:
        vert_line = CEILING
        vert_hit = intersection(laser_line, vert_line)
        vert_dist = get_distance(origin, vert_hit)
    elif origin[1] < laser[1]:
        vert_line = FLOOR
        vert_hit = intersection(laser_line, vert_line)
        print("INTERSECTION", vert_hit)
        vert_dist = get_distance(origin, vert_hit)

    # See if it goes left or right
    if laser[0] == origin[0]:
        wall_line = None
    elif laser[0] > origin[0]:
        wall_line = WALL_R
        wall_hit = intersection(laser_line, wall_line)
        wall_dist = get_distance(origin, wall_hit)
    elif laser[0] < origin[0]:
        wall_line = WALL_L
        wall_hit = intersection(laser_line, wall_line)
        wall_dist = get_distance(origin, wall_hit)

    # Where do we hit?
    # Vertical; Only floor/ceiling
    if vert_line and not wall_line:
        if vert_line == FLOOR:
            print("Hitting that floor")
            return reflect(dim, vert_hit, (vert_hit[0]+(vert_hit[0]-origin[0]), origin[1]), dist - vert_dist)

        elif vert_line == CEILING:
            print("Hitting that ceiling")
            return reflect(dim, vert_hit, (vert_hit[0]+(vert_hit[0]-origin[0]), origin[1]), dist - vert_dist)


    # Horizontal; only hitting either wall
    elif not vert_line and wall_line:
        print("Only hitting walls")
        return reflect(dim, wall_hit, (origin[0], wall_hit[1]+(wall_hit[1]-origin[1])), dist - wall_dist)

    # You're going to end up hitting both eventually
    elif vert_line and wall_line:
        print("You're hitting both!")
        # Wall is further
        if vert_dist < wall_dist:
            if vert_line == FLOOR:
                print("... but you're hitting the floor first at", vert_hit)
                print("Angle", origin, vert_hit)
                print("Distance left, laser direction", dist - vert_dist, laser)
                return reflect(dim, vert_hit, (vert_hit[0]+(vert_hit[0]-origin[0]), origin[1]), dist - vert_dist)

            elif vert_line == CEILING:
                print("... but you're hitting the ceiling first at", vert_hit)
                print("Angle", origin, vert_hit)
                print("Distance left, laser direction", dist - vert_dist, laser)
                return reflect(dim, vert_hit, (vert_hit[0]+(vert_hit[0]-origin[0]), origin[1]), dist - vert_dist)
        # Floor/Ceiling is further
        elif vert_dist > wall_dist:
            if wall_line == WALL_L:
                print("... but you're hitting the left wall first at", wall_hit)
                print("Angle", origin, wall_hit)
                print("Distance left, laser direction", dist - wall_dist, laser)
                return reflect(dim, wall_hit, (origin[0], wall_hit[1]+(wall_hit[1]-origin[1])), dist - wall_dist)
            elif wall_line == WALL_R:
                print("... but you're hitting the right wall first", wall_hit)
                print("Angle", origin, wall_hit)
                print("Distance left, laser direction", dist - wall_dist, laser)
                return reflect(dim, wall_hit, (origin[0], wall_hit[1]+(wall_hit[1]-origin[1])), dist - wall_dist)
        else:
            print("Uhhhhhh, that's a corner")
            return reflect(dim, wall_hit, origin, dist - wall_dist)






# INTERSECTIONS: I'll need to learn about this later
def intersection(laser_line, target_line):
    D  = laser_line[0] * target_line[1] - laser_line[1] * target_line[0]
    Dx = laser_line[2] * target_line[1] - laser_line[1] * target_line[2]
    Dy = laser_line[0] * target_line[2] - laser_line[2] * target_line[0]
    if D != 0:
        print(D, Dx, Dy)
        x = round(Dx, 6) / round(D, 6)
        y = round(Dy, 6) / round(D, 6)
        print("X AND Y", x, y)
        return round(x, 6), round(y, 6)
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

# Checking to see if something is on a line
def is_on(a, b, c):
    """See if it's between a and b. x=[0], y=[1]"""
    # Use either the x or the y to see if within bounds
    a = list(map(lambda x: round(x, 5), a))
    b = list(map(lambda x: round(x, 5), b))
    c = list(map(lambda x: round(x, 5), c))
    print("CHECKING IS_ON")
    print(a, b, c)


    if a[0] != b[0]:
        is_within = within(a[0], c[0], b[0])
    else:
        is_within = within(a[1], c[1], b[1])
    return collinear(a, b, c) and is_within

def collinear(a, b, c):
    "Return if on same line, but let's give SOME leeway"
    print("COLLINEAR CHECK")
    return round((b[0] - a[0])*(c[1] - a[1]), 2) == round((c[0] - a[0]) * (b[1] - a[1]), 2)


def within(p, q, r):
    "Return true iff q is between p and r (inclusive)."
    return p <= q <= r or r <= q <= p



# [300,275], [150,150], [185, 100], 500
print(answer([300,275], [150,150], [185, 100], 500))

# print(answer([3, 2], [1, 1], [2, 1], 4))
