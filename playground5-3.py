"""
I don't feel proud about this.

I came into it not knowing too much about pathfinding and made
quite a few attempts.

Many of them went into seconds. I learned about memoization, but I kept
having iterate through to find the best. This takes way too much time and was
rather naive. Plus side, I learned about memoization and the basics.

I looked back through StackOverflow for inspiration and found an interesting
one that involved dictionaries for unique tiles. I thought 'wait, how do I
put nodes into dictiona- wait, I can make my OWN hash',

But then it basically ended up looking like theirs code.

I put in comments to show that I did understand the code +
I will hopefully look back into it and study things further for optimizing,
but I didn't feel too great about it.
"""
from collections import deque   # Better this than a deque (O(1) everything!)
# ASIDE: You know, they always did make fun of deques. Now who's laughing?


class Tile:
    """Individual tile data."""

    def __init__(self, x, y, breakable, maze):
        """Initialize with coordinates, amt breakable, and maze."""
        # Coordinates
        self.x = x
        self.y = y
        # Amount of breakable
        self.breakable = breakable
        # Passed in maze
        self.maze = maze

    def __hash__(self):
        """Needed for hashing to dictionary."""
        return (self.x ** self.y) + (self.x * self.y)

    def __eq__(self, other):
        """Can't double up on coordinates and breakable stat!"""
        if self.x == other.x and self.y == other.y and self.breakable == other.breakable:
            return True
        return False

    def get_neighbors(self):
        """Grab neighbors."""
        # For each wall broken, append a neighbor + lower neighbor's break by 1
        # After we break one, it should be 0 now
        breakable = self.breakable
        # List of VALID neighbors
        neighbors = []
        # Current coordinates
        x = self.x
        y = self.y
        # Grid system for figuring out coordinates + neighbors
        maze = self.maze
        rows = len(maze)
        cols = len(maze[0])

        # If it's not on leftmost, we can check left
        if x > 0:
            # If left is wall and we can break it, it's valid
            if maze[y][x - 1] == 1:
                if breakable > 0:
                    neighbors.append(Tile(x - 1, y, breakable - 1, maze))
            else:
                neighbors.append(Tile(x - 1, y, breakable, maze))

        # If not rightmost, right blocks are available
        if x < cols - 1:
            # Right is wall + can break it?
            if maze[y][x+1] == 1:
                if breakable > 0:
                    neighbors.append(Tile(x + 1, y, breakable - 1, maze))
            # Normal tile
            else:
                neighbors.append(Tile(x + 1, y, breakable, maze))

        # If under top row, tile under is available
        if y > 0:
            # Below is wall + can break?
            if maze[y - 1][x] == 1:
                if breakable > 0:
                    neighbors.append(Tile(x, y - 1, breakable - 1, maze))
            # Normal tile
            else:
                neighbors.append(Tile(x, y - 1, breakable, maze))

        # If above bottom row, tile above is available
        if y < rows - 1:
            # Above is wall + can break?
            if maze[y + 1][x] == 1:
                if breakable > 0:
                    neighbors.append(Tile(x, y + 1, breakable - 1, maze))
            # Normal tile
            else:
                neighbors.append(Tile(x, y + 1, breakable, maze))

        # Return all valid neighbors
        return neighbors


class Mapper:
    """For designing the map and the escape plan!"""

    def __init__(self, maze):
        """Initialize with map of maze and dimensions."""
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

    def escape_route(self):
        """Create the actual escape route."""
        # Make entrance node
        entrance = Tile(0, 0, 1, self.maze)
        # Dictionary for distances
        distance_map = {entrance: 1}
        # Deque for call stack, because lists are a no-no
        queue = deque([entrance])

        # As long as our queue is available, we can keep searching
        while queue:
            # Dequeue queue; next node up!
            current_node = queue.popleft()
            # If we hit the end, return the distance
            if current_node.x == self.cols - 1 and current_node.y == self.rows - 1:
                return distance_map[current_node]
            # Else, get plausible neighbors we can move to (0s)
            for neighbor in current_node.get_neighbors():
                # IMPORTANT! We only add UNIQUE nodes! D-R-Y.
                if neighbor not in distance_map.keys():
                    distance_map[neighbor] = distance_map[current_node] + 1
                    queue.append(neighbor)

        # [YOU CANNOT ESCAPE]
        return False


def answer(maze):
    """We must find the way out."""
    escape = Mapper(maze)

    if escape is False:
        raise ValueError("You cannot escape this maze! Game over, man!")
    else:
        return escape.escape_route()


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
