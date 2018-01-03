import math

def line(p1, p2):
    """Grab the... somethings."""
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

# The lines and their factors
CEILING = line((-1, -1), (0, -1))
WALL_L = line((-1, -1), (-1, 0))
WALL_R = None
FLOOR = None

def hitbox_set(your_x, your_y, guard_x, guard_y):
        global GUARD_L, GUARD_R, GUARD_U, GUARD_D

        GUARD_L = line((guard_x-0.5, guard_y-0.5), (guard_x-0.5, guard_y+0.5))
        GUARD_R = line((guard_x+0.5, guard_y-0.5), (guard_x+0.5, guard_y+0.5))
        GUARD_U = line((guard_x-0.5, guard_y-0.5), (guard_x+0.5, guard_y-0.5))
        GUARD_D = line((guard_x-0.5, guard_y+0.5), (guard_x+0.5, guard_y+0.5))

        global YOUR_L, YOUR_R, YOUR_U, YOUR_D

        YOUR_L = line((your_x-0.5, your_y-0.5), (your_x-0.5, your_y+0.5))
        YOUR_R = line((your_x+0.5, your_y-0.5), (your_x+0.5, your_y+0.5))
        YOUR_U = line((your_x-0.5, your_y-0.5), (your_x+0.5, your_y-0.5))
        YOUR_D = line((your_x-0.5, your_y+0.5), (your_x+0.5, your_y+0.5))


def answer(dimensions, your_position, guard_position, distance):
    """Begin combat protocol."""
    global WALL_R, FLOOR
    global YOU, GUARD

    WALL_R = line((dimensions[0]+1, -1), (dimensions[0]+1, 0))
    FLOOR = line((0, dimensions[1]+1), (-1, dimensions[1]+1))

    YOU = your_position
    GUARD = guard_position

    your_x = your_position[0]
    your_y = your_position[1]
    guard_x = guard_position[0]
    guard_y = guard_position[1]

    hitbox_set(your_x, your_y, guard_x, guard_y)

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
    answers.append((3, -2))
    while laser_y != your_y:
        laser_x += 1
        laser_y = your_y - int(missing_angle(laser_x, distance))  # Offset
        answers.append((laser_x, laser_y))


    # laser_x = your_x - distance
    # laser_y = your_y
    # while laser_x != your_x:
    #     laser_x += 1
    #     laser_y = your_y - int(missing_angle(laser_x, distance))  # Offset
    #     answers.append((laser_x, laser_y))


    for item in answers:
        print("My position:", your_position)
        print("Laser direction:", item)
        print("Target position:", guard_position)
        reflect(dimensions, your_position, item, distance)
        print("======================")
    return answers

def hit_check(laser, laser_line):
    print("PRINTING: UP, DOWN, LEFT, RIGHT")
    inter_U = intersection(laser_line, GUARD_U)
    print(inter_U)

    if inter_U and GUARD[0] - 0.5 <= inter_U[0] <= GUARD[0] + 0.5:
        print("* * * * * * * * * * * * * * * * * * * *")
        print("* * * * * REFLECT HIT(TOP) * * * * *")
        print("* * * * * * * * * * * * * * * * * * * *")
        return True

    inter_D = intersection(laser_line, GUARD_D)
    print(inter_D)

    if inter_D and GUARD[0] - 0.5 <= inter_D[0] <= GUARD[0] + 0.5:
        print("* * * * * * * * * * * * * * * * * * * *")
        print("* * * * * REFLECT HIT (BOTTOM) * * * * *")
        print("* * * * * * * * * * * * * * * * * * * *")
        return True

    inter_L = intersection(laser_line, GUARD_L)
    print(inter_L)

    if inter_L and GUARD[1] - 0.5 <= inter_L[1] <= GUARD[1] + 0.5:
        print("* * * * * * * * * * * * * * * * * * * *")
        print("* * * * * REFLECT HIT (LEFT) * * * * *")
        print("* * * * * * * * * * * * * * * * * * * *")
        return True

    inter_R = intersection(laser_line, GUARD_R)
    print(inter_R)
    if inter_L and GUARD[1] - 0.5 <= inter_R[1] <= GUARD[1] + 0.5:
        print("* * * * * * * * * * * * * * * * * * * *")
        print("* * * * * REFLECT HIT (RIGHT) * * * * *")
        print("* * * * * * * * * * * * * * * * * * * *")
        return True


def reflect(dim, origin, laser, dist):
    # Going toward ceiling
    laser_line = line(origin, laser)
    print("New set")
    if hit_check(laser, laser_line):
        print("WE'RE DONE HERE")
        return True

    if is_on(origin, laser, GUARD):
        print("* * * * * * * * * * * * * * * * * * * *")
        print("* * * * * Straight shot * * * * *")
        print("* * * * * * * * * * * * * * * * * * * *")

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
        elif vert_line == CEILING:
            print("Hitting that ceiling")

    # Horizontal; only hitting either wall
    elif not vert_line and wall_line:
        print("Only hitting walls")

    # You're going to end up hitting both eventually
    elif vert_line and wall_line:
        print("You're hitting both!")
        # Wall is further
        if vert_dist < wall_dist:
            if vert_line == FLOOR:
                print("... but you're hitting the ceiling first at", vert_hit)
                print("Angle", origin, vert_hit)
                print("Distance left, laser direction", dist - vert_dist, laser)
                reflect(dim, vert_hit, (vert_hit[0]+(vert_hit[0]-origin[0]), origin[1]), dist - vert_dist)

            elif vert_line == CEILING:
                print("... but you're hitting the ceiling first at", vert_hit)
                print("Angle", origin, vert_hit)
                print("Distance left, laser direction", dist - vert_dist, laser)
                reflect(dim, vert_hit, (vert_hit[0]+(vert_hit[0]-origin[0]), origin[1]), dist - vert_dist)
        # Floor/Ceiling is further
        elif vert_dist > wall_dist:
            if wall_line == WALL_L:
                print("... but you're hitting the left wall first at", wall_hit)
                print("Angle", origin, wall_hit)
                print("Distance left, laser direction", dist - wall_dist, laser)
                reflect(dim, wall_hit, (origin[0], wall_hit[1]+(wall_hit[1]-origin[1])), dist - wall_dist)
            elif wall_line == WALL_R:
                print("... but you're hitting the right wall first", wall_hit)
                print("Angle", origin, wall_hit)
                print("Distance left, laser direction", dist - wall_dist, laser)
                reflect(dim, wall_hit, (origin[0], wall_hit[1]+(wall_hit[1]-origin[1])), dist - wall_dist)





# INTERSECTIONS: I'll need to learn about this later
def intersection(laser_line, target_line):
    D  = laser_line[0] * target_line[1] - laser_line[1] * target_line[0]
    Dx = laser_line[2] * target_line[1] - laser_line[1] * target_line[2]
    Dy = laser_line[0] * target_line[2] - laser_line[2] * target_line[0]
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

# Checking to see if something is on a line
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
