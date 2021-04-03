# Standing on the top cornet of n x m grid with coordinate (0,0)
# simulate a walk where the destination in right hand bottom corner
# at coordinate (n - 1, m - 1)
# In this walk, allowed moves are - moving down or side way movement
# to the right

def grid_walk(rows, cols):
    row = [0 for _ in range(cols)]
    grid = [row[0:] for _ in range(rows)]
    for j in range(1, cols):
        grid[0][j] = 1
    for i in range(1, rows):
        grid[i][0] = 1
    for i in range(1, rows):
        for j in range(1, cols):
            grid[i][j] = grid[i - 1][j] + grid[i][j - 1]
    return grid[rows -1][cols - 1]

# There ia another way to calculate numer of paths.
# To reach the bottom on (4,3) grid, we need to go
# down 2 steps and move to right 3 times. These movements
# can happen any order. Total number of such distinct arrangements
# will give total count of different path.
# identify downward movement by D and move to right as R
# This problem is equivalent of distinct arrangements for 5 character word
# formed using 2 D's and 3 R's. That count will be 5!/3!2! = 10
if __name__ == '__main__':
    print(grid_walk(4, 3))