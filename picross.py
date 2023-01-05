global FIRST_LINE
global GRID
global NUM_ROW
global NUM_COL
global ROW_CLUES
global COL_CLUES


def create_grid(file):
    global FIRST_LINE
    global GRID
    global NUM_ROW
    global NUM_COL
    global ROW_CLUES
    global COL_CLUES
    try:
        with open(file) as f:
            FIRST_LINE = f.readline()
            NUM_ROW = int(FIRST_LINE[0])
            NUM_COL = int(FIRST_LINE[2])
            GRID = [["-" for index in range(NUM_ROW)] for index in range(NUM_COL)]
            ROW_CLUES = f.readline()
            ROW_CLUES = (ROW_CLUES.split("*"))
            # print(ROW_CLUES)
            COL_CLUES = f.readline()
            COL_CLUES = (COL_CLUES.split("*"))
            # print(COL_CLUES)
            return GRID
    except IOError:
        print("File does not exist")
        exit()


def print_grid():
    print("\n".join("".join(row) for row in GRID))


def find_empty_square(grid):
    global NUM_COL
    global NUM_ROW
    for row in range(NUM_ROW):
        for col in range(NUM_COL):
            if grid[row][col] == "-":
                return row, col
    return None, None


def is_valid(grid, row, col):
    # check first against row clue
    row_clue = int(get_row_clue(row))
    while row_clue > -1:
        grid[row][col] = "*"
        row = row+1
        row_clue = row_clue-1
    col_clue = int(get_col_clue(row))
    while col_clue > -1:
        grid[row][col] = "*"
        col = col+1
        col_clue = col_clue-1


def get_row_clue(row):
    return ROW_CLUES[row]


def get_col_clue(col):
    return COL_CLUES[col]


def solve_picross(grid):
    row, col = find_empty_square(grid)
    if row or col is None:
        return True

    if is_valid(grid, row, col):
        if solve_picross(grid):
            return True


def main():
    grid = create_grid("test1")
    print("BEFORE")
    print_grid()
    solve_picross(grid)
    print("\nAFTER")
    print_grid()

if __name__ == '__main__':
    main()
