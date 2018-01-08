"""
Bringing a gun to a guard fight.

I struggled with this.
I originally had each shot reflect and went for a Hail Mary approach;
simulate every individual shot and see if it hits. Had a lot of
problems with precision, was using hitboxes at one point, had
to deal with decimals, floating point junk, etc. I kept at the same
approach, optimizing each piece and learning something new along the way,
but it just wasn't meant to be. I still kept hitting time-outs. I was
fairly discouraged before realizing I needed to approach this differently.

After crawling through some other code, I hit a "duh" moment:
Just create all possible locations of the guard on an extended graph, then
just see if I'm in the way. That or a corner, corners are special (perfect
reflects and all).
"""

import itertools
from fractions import gcd
from math import hypot
# Initializing room dimensions
DIM_X = 0
DIM_Y = 0


def reflections(unit, reflects):
    """Create reflections of coordinates."""
    # All possible reflections of what you pass in
    mirrored_x = [unit[0]]
    mirrored_y = [unit[1]]
    # The original coordinates of who we're trying to mirror
    unit_x = unit[0]
    unit_y = unit[1]
    # Four temporary variables
    pos_x = unit_x
    neg_x = unit_x
    pos_y = unit_y
    neg_y = unit_y

    for passes in range(1, reflects+1):
        # Mirrors alternate; odds and evens:
        if passes % 2 == 1:
            # Possible x-coordinates
            pos_x += 2 * (DIM_X - unit_x)
            neg_x -= 2 * unit_x
            mirrored_x.append(pos_x)
            mirrored_x.append(neg_x)
            # Possible y-coordinates
            pos_y += 2 * (DIM_Y - unit_y)
            neg_y -= 2 * unit_y
            mirrored_y.append(pos_y)
            mirrored_y.append(neg_y)
        else:
            # Possible x-coordinates
            pos_x += 2 * unit_x
            neg_x -= 2 * (DIM_X - unit_x)
            mirrored_x.append(pos_x)
            mirrored_x.append(neg_x)
            # Possible y-coordinates
            pos_y += 2 * unit_y
            neg_y -= 2 * (DIM_Y - unit_y)
            mirrored_y.append(pos_y)
            mirrored_y.append(neg_y)

    return (mirrored_x, mirrored_y)


def get_corners(reflects):
    """Grab all available corners."""
    corners_x = []
    corners_y = []
    for reflect in range(reflects+1):
        # All possible x coordinate corners
        corners_x.append(-reflect * DIM_X)
        corners_x.append((reflect+1) * DIM_X)
        # All possible y coordinate corners
        corners_y.append(-reflect * DIM_Y)
        corners_y.append((reflect+1) * DIM_Y)
    return (corners_x, corners_y)


def simplify(diff_x, diff_y):
    """Simplify directions (ie 10, 20 is just 1, 2)."""
    divisor = abs(gcd(diff_x, diff_y))
    rel_x = int(diff_x/divisor)
    rel_y = int(diff_y/divisor)
    return (rel_x, rel_y)


def get_copies(mirrors, target):
    """Make dictionary of relative direction and distances of objects."""
    # Key is direction, value is distance
    copies = {}
    # Getting all combinations of the mirror x's and y's
    for coord in itertools.product(mirrors[0], mirrors[1]):

        # Grab the relative location from absolutes
        if coord == target:
            (rel_x, rel_y) = (0, 0)  # If it's on you, it's (0, 0), dist = 0
            distance = 0
        # Else we simplify
        else:
            diff_x = coord[0] - target[0]
            diff_y = coord[1] - target[1]
            (rel_x, rel_y) = simplify(diff_x, diff_y)
            distance = hypot(diff_x, diff_y)  # Pythagorean for distance

        # See if it's in copies and update if the distance is shorter
        if (rel_x, rel_y) not in copies:
            copies[(rel_x, rel_y)] = distance
        else:
            if copies[(rel_x, rel_y)] > distance:
                copies[(rel_x, rel_y)] = distance

    return copies


def combat_protocol(you, guard, corners, dist):
    """Simulate all plausible shots."""
    hits = 0

    for loc in guard:  # Every shot we CAN take
        if guard[loc] <= dist:  # Can we reach it?
            if loc in you:  # Share direction w/ yourself?
                if you[loc] < guard[loc]:  # You are closer; you get shot
                    continue
            if loc in corners:  # Share direction w/ corner?
                if corners[loc] < guard[loc]:  # Corner is closer; back we go
                    continue
            # If all is well, you're good.
            hits += 1
    return hits


def answer(dims, you, guard, distance):
    """Activating combat protocol."""
    # Global constant; this isn't going to change any.
    global DIM_X, DIM_Y
    DIM_X = dims[0]
    DIM_Y = dims[1]

    # Check if we can even reach it in the first place
    enemy_dist = hypot(you[0]-guard[0], you[1]-guard[1])
    if enemy_dist > distance:
        return 0
    elif enemy_dist == distance:
        return 1

    # Tuples for ease of use; they'll remain static
    you = tuple(you)
    guard = tuple(guard)

    # I was thinking distance from you to wall, but better safe than sorry
    reflects = 1 + int(distance / min(DIM_X, DIM_Y))

    # All mirrored coordinates
    your_mirrors = reflections(you, reflects)
    guard_mirrors = reflections(guard, reflects)
    corner_mirrors = get_corners(reflects)

    # Now, the relative coordinates
    your_coords = get_copies(your_mirrors, you)
    guard_coords = get_copies(guard_mirrors, you)
    corner_coords = get_copies(corner_mirrors, you)

    return combat_protocol(your_coords, guard_coords, corner_coords, distance)
