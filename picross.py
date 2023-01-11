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
            COL_CLUES = f.readline()
            COL_CLUES = (COL_CLUES.split("*"))
            for element in COL_CLUES:
                position = COL_CLUES.index(element)
                if len(element) > 1:
                    sub_clue = element.split(" ")
                    # sub_clue = list(element)
                    COL_CLUES[position] = sub_clue
            print(COL_CLUES)
            ROW_CLUES = f.readline()
            ROW_CLUES = (ROW_CLUES.split("*"))
            for element in ROW_CLUES:
                position = ROW_CLUES.index(element)
                if len(element) > 1:
                    sub_clue = element.split(" ")
                    # sub_clue = list(element)
                    ROW_CLUES[position] = sub_clue
            print(ROW_CLUES)
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
    r = row
    c = col
    # print("~                ~")
    # print_grid()
    # check first against row clue
    if check_row_filled(row) or check_col_filled(col):
        return False
    row_clue = get_row_clue(row)
    if check_row_filled(row):
        clue = ROW_CLUES[row]
        if type(clue) == list:
            clue.pop(0)
            if len(clue) == 1:
                ROW_CLUES[row] = clue[0]
    else:
        while row_clue > 0:
            grid[r][c] = "*"
            grid[r][c+1] = "."
            grid[r+1][c] = "."
            r = r+1
            row_clue = row_clue-1
    col_clue = get_col_clue(row)
    if check_col_filled(col):
        clue = COL_CLUES[col]
        if type(clue) == list:
            clue.pop(0)
            if len(clue) == 1:
                COL_CLUES[col] = clue[0]
    else:
        while col_clue > 0:
            grid[r][c] = "*"
            grid[r+1][c] = "."
            c = c+1
            col_clue = col_clue-1
    # if this is an empty spot but the row or column is already filled
    # then this space is not valid
    return True


def check_col_filled(col):
    count = 0
    for x in range(NUM_COL):
        if GRID[x][col] == "*":
            count = count+1
    if type(COL_CLUES[col] == list):
        if count == int(COL_CLUES[col][0]):
            return True
    else:
        if count == int(COL_CLUES[col]):
            return True
    return False


def check_row_filled(row):
    count = 0
    for x in range(NUM_ROW):
        if GRID[row][x] == "*":
            count = count+1
    if type(ROW_CLUES[row] == list):
        if count == int(ROW_CLUES[row][0]):
            return True
    else:
        if count == int(ROW_CLUES[row]):
            return True
    return False


def get_row_clue(row):
    clue = ROW_CLUES[row]
    if type(clue) == list:
        value = int(clue[0])
    #     clue.pop(0)
    #     if len(clue) == 1:
    #         ROW_CLUES[row] = clue[0]
        return value
    return int(clue)


def get_col_clue(col):
    clue = COL_CLUES[col]
    if type(clue) == list:
        value = int(clue[0])
    #     clue.pop(0)
    #     if len(clue) == 1:
    #         COL_CLUES[col] = clue[0]
        return value
    return int(clue)


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
