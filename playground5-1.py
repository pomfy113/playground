from collections import deque

def memodict(f):
     """ Memoization decorator for a function taking a single argument """
     class memodict(dict):

        def __missing__(self, key):
           ret = self[key] = f(key)
           return ret
     return memodict().__getitem__


@memodict
def adjacent_to((maze_dim, point)):
     neighbors = (
         (point[0] - 1, point[1]),
         (point[0], point[1] - 1),
         (point[0], point[1] + 1),
         (point[0] + 1, point[1]))

     return [p for p in neighbors if 0 <= p[0] < maze_dim[0] and 0 <= p[1] < maze_dim[1]]




def removable(maz, ii, jj):
     counter = 0
     for p in adjacent_to(((len(maz), len(maz[0])), (ii, jj))):
         if not maz[p[0]][p[1]]:
             if counter:
                 return True
             counter += 1
     return False


def answer(maze):

     path_length = 0

     if not maze:
         return

     dims = (len(maze), len(maze[0]))
     end_point = (dims[0]-1, dims[1]-1)

     # list of walls that can be removed
     passable_walls = set()
     for i in xrange(dims[0]):
         for j in xrange(dims[1]):
             if maze[i][j] == 1 and removable(maze, i, j):
                 passable_walls.add((i, j))

     shortest_path = 0
     print(passable_walls)
     best_possible = dims[0] + dims[1] - 1

     path_mat = [[None] * dims[1] for _ in xrange(dims[0])]  # tracker      matrix for shortest path
     path_mat[dims[0]-1][dims[1]-1] = 0  # set the starting point to destination (lower right corner)

     for wall in passable_walls:
         temp_maze = maze
         if wall:
             temp_maze[wall[0]][wall[1]] = 0

         stat_mat = [['-'] * dims[1] for _ in xrange(dims[0])]  # status of visited and non visited cells

         q = deque()
         q.append(end_point)

         while q:
             curr = q.popleft()

             if curr == (0,0):
                 break

             for next in adjacent_to((dims, curr)):
                 if temp_maze[next[0]][next[1]] == 0:  # Not a wall
                     temp = path_mat[curr[0]][curr[1]] + 1
                     if temp < path_mat[next[0]][next[1]] or path_mat[next[0]][next[1]] == None:  # there is a shorter path to this cell
                         path_mat[next[0]][next[1]] = temp
                     if stat_mat[next[0]][next[1]] != '+':  # Not visited yet
                         q.append(next)

             stat_mat[curr[0]][curr[1]] = '+'  # mark it as visited

         if path_mat[0][0]+1 <= best_possible:
             break
     for i in range(len(path_mat[0])):
         print(path_mat[i])
     if shortest_path == 0 or path_mat[0][0]+1 < shortest_path:
         shortest_path = path_mat[0][0]+1

     return shortest_path

maze = [
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0]
    ]
print(answer(maze))
