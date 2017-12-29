from collections import deque

def memoize(f):
    """Memoize! God, it's so fast."""
    class memodict(dict):
        def __getitem__(self, *key):
            return dict.__getitem__(self, key)
        def __missing__(self, key):
            ret = self[key] = f(*key)
            return ret
    return memodict().__getitem__

def answer(maze):
    if not maze:
        return
    dimensions = (len(maze), len(maze[0]))
    # Set of walls we can pass
    passable = wallcheck(dimensions, maze)
    print(passable)
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
            if adjacent:
                return True
            adjacent += 1
    # We need 2 or more free blocks, otherwise it's pointless
    return False


@memoize
def adjacent_blocks(dim, point):
    """Set up valid adjacent blocks."""
    adjacent_blocks = []
    if point[0] > 0:
        adjacent_blocks.append((point[0]+1, point[1]))
    if point[0] < dim[0]:
        adjacent_blocks.append((point[0]-1, point[1]))
    if point[1] > 0:
        adjacent_blocks.append((point[0], point[1]-1))
    if point[1] < dim[1]:
        adjacent_blocks.append((point[0], point[1]+1))

    # Check if it's within bounds of maze dimensions
    return [block for block in adjacent_blocks if 0 <= block[0] < dim[0] and 0 <= block[1] < dim[1]]



# # # # # # # # #
#  Pathfinding  #
# # # # # # # # #
def pathfinding(dims, maze, passable):
    """Actual pathfinding function."""
    end = (dims[0]-1, dims[1]-1)
    best = 0

    mazemap = [[None] * dims[1] for _ in xrange(dims[0])]
    # Starting at the end, then working our way back!
    mazemap[dims[0]-1][dims[1]-1] = 0

    # Check the passable walls
    for wall in passable:
        temp_maze = maze
        # If we can break it, let's!
        # We checked to make sure ALL passable walls are valid
        if wall:
            temp_maze[wall[0]][wall[1]] = 0

        # For checking visited/non-visited
        stat_mat = [['-'] * dims[1] for _ in xrange(dims[0])]

        # Queue for where to go next
        # Originally list, but deques have O(n) queue/dequeue
        queue = deque()
        queue.append(end)

        while queue:
            # Dequeue; where we go next
            current = queue.popleft()
            curr_x = current[0]
            curr_y = current[1]

            # We hit the beginning point
            if current == (0, 0):
                break

            # Check where the next block would take us
            for nextblock in adjacent_blocks(dims, current):
                next_x = nextblock[0]
                next_y = nextblock[1]
                # Check if not a wall
                if temp_maze[next_x][next_y] == 0:
                    # If so, that's our next move! Add 1 to move
                    moves = mazemap[curr_x][curr_y] + 1
                    # If there's a shorter path...
                    if best != 0 and moves > best:
                        break
                    if moves < mazemap[next_x][next_y] or mazemap[next_x][next_y] is None:
                        mazemap[next_x][next_y] = moves
                    # Not visited yet
                    if stat_mat[next_x][next_y] != '~':
                        queue.append(nextblock)
            stat_mat[curr_x][curr_y] = '~'

        if mazemap[0][0]+1 <= (dims[0] + dims[1] - 1):
            break
        print(best)

    for i in xrange(len(mazemap)):
        print(mazemap[i])

    if best == 0 or mazemap[0][0]+1 < best:
        best = mazemap[0][0]+1

        return best


maze = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

print(answer(maze))

# answer([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]])
