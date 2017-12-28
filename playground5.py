from collections import deque

def answer(maze):
    dimensions = (len(maze), len(maze[0]))
    # Set of walls we can pass
    passable = wallcheck(dimensions, maze)
    # Actual pathfinding
    return pathfinding(dimensions, maze, passable)

# # # # # # # # # # # # # #
#  Wall check shenanigans #
# # # # # # # # # # # # # #

def wallcheck(dim, maze):
    """Makes a set of walls we can remove."""
    passable = set()
    for x in xrange(dim[0]):
        for y in xrange(dim[1]):
            if maze[x][y] == 1 and isremovable(dim, maze, x, y):
                # Success! We found a passable block
                passable.add((x, y))
    return passable

def isremovable(dim, maze, x, y):
    """Check if wall is removable."""
    # Need to make sure this is 2 or more
    adjacent = 0
    # Coordinate for original block
    coordinates = (x, y)

    # Learned that I can't do for x, y due to possibly only having one?
    # Checks to see all VALID adjacent blocks
    for coord in adjacent_blocks(dim, coordinates):
        if maze[coord[0]][coord[1]] == 0:
            adjacent += 1

    # We need 2 or more free blocks, otherwise it's pointless
    if adjacent > 1:
        return True
    else:
        return False


def adjacent_blocks(dim, point):
    """Set up valid adjacent blocks."""
    adjacent_blocks = (
        (point[0]+1, point[1]),     # Right block
        (point[0], point[1]-1),     # Bottom block
        (point[0]-1, point[1]),     # Left block
        (point[0], point[1]+1)      # Top block
        )

    # Check if it's within bounds of maze dimensions
    for block in adjacent_blocks:
        if 0 <= block[0] < dim[0] and 0 <= block[1] < dim[1]:
            yield block

# # # # # # # # #
#  Pathfinding  #
# # # # # # # # #
def pathfinding(dim, maze, passable):
    end = (dim[0]-1, dim[1]-1)
    best = 0

    mazemap = [[None] * dim[1] for _ in xrange(dim[0])]
    mazemap[end[0]][end[1]] = 0          # Starting and ending

    for wall in passable:
        temp_maze = maze
        if wall:
            temp_maze[wall[0]][wall[1]] = 0

        stat_mat = [['-'] * dim[1] for _ in xrange(dim[0])]
        #
        queue = deque()
        queue.append(end)
    while queue:
        current = queue.popleft()

        if current == (0, 0):
            break

        for next in adjacent_blocks(dim, current):
            if temp_maze[next[0]][next[1]] == 0:  # Not a wall
                temp = mazemap[current[0]][current[1]] + 1
                if temp < mazemap[next[0]][next[1]] or mazemap[next[0]][next[1]] == None:  # there is a shorter path to this cell
                    mazemap[next[0]][next[1]] = temp
                if stat_mat[next[0]][next[1]] != '+':  # Not visited yet
                    queue.append(next)
        print(queue)
        mazemap[current[0]][current[1]] = '+'

        # That's as fast as we can go
        if mazemap[0][0]+1 <= (dim[0] + dim[1] - 1):
            break
    if best == 0 or mazemap[0][0]+1 < best:
        best = mazemap[0][0]+1

    return best

maze = [
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0]
    ]

print(answer(maze))

# answer([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]])
