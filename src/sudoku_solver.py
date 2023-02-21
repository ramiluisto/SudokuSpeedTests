


def produce_p_grid_from_sudoku_string(input_sudoku : str):
    base_p = 9*[1]
    p_grid = [[base_p.copy() for _ in range(9)] for j in range(9)]


    for idx, char in enumerate(input_sudoku):
        row = idx//9
        col = idx%9
        value = int(char)

        if value != 0:
            p_grid[row][col] = 9*[0]
            p_grid[row][col][value-1] = 1

    return p_grid


def print_sudoku(sudoku):
    TOP_ROW_FORMAT = "╔═══════╤═══════╤═══════╗"
    MID_ROW_FORMAT = "╟───────┼───────┼───────╢"
    BOT_ROW_FORMAT = "╚═══════╧═══════╧═══════╝"
    ROW_FORMAT =     "║ {} {} {} │ {} {} {} │ {} {} {} ║"

    sudoku_nums = []
    for idx in range(81):
        row = idx//9
        col = idx%9
        if sum(sudoku[row][col]) != 1:
            value = "_"
        else:
            value = str(sudoku[row][col].index(1) + 1)

        sudoku_nums.append(value)

    print(TOP_ROW_FORMAT)
    for j in [0,9,18]:
        print(ROW_FORMAT.format(*sudoku_nums[j:j+9]))
    print(MID_ROW_FORMAT)
    for j in [27, 36, 45]:
        print(ROW_FORMAT.format(*sudoku_nums[j:j+9]))
    print(MID_ROW_FORMAT)
    for j in [54,63,72]:
        print(ROW_FORMAT.format(*sudoku_nums[j:j+9]))
    print(BOT_ROW_FORMAT)


def recursive_solver(sudoku) -> bool:

    changed = True
    while(changed):
        changed = reduce_possibilities(sudoku)

    if is_solved(sudoku):
        return True

    cell_idx = first_unsolved_cell_index(sudoku)
    possibilities = get_cell_possibilities(cell_idx, sudoku)
    for p in possibilities:
        local_sudoku = sudoku.copy()
        set_cell_of_sudoku(cell_idx, local_sudoku, p)

        result = recursive_solver(local_sudoku)
        if result:
            return True

    return False


def reduce_possibilities(sudoku):

    for idx in range(81):
        row_idx = idx//9
        col_idx = idx%9

        if sum(sudoku[row][col]) == 1:
            continue






def get_sudoku_row(row_idx, sudoku):
    return sudoku[row_idx]

def get_sudoku_col(col_idx, sudoku):
    return [sudoku[j][col_idx] for j in range(9)]

def get_sudoku_blo(idx, sudoku):

    blo_row = idx//27
    blo_col = (idx//3)%3
    top_left = 27*blo_row + 3*blo_col

    shifts = [*range(3), *range(9, 12), *range(18, 21)]
    block = []
    for shift in shifts:
        internal_idx = top_left + shift
        row = internal_idx//9
        col = internal_idx%9
        block.append(sudoku[row][col])

    return block

def combine_exclusions(row_idx, col_idx, possibility_grid):

    row = get_sudoku_row(row_idx, sudoku)
    col = get_sudoku_col(col_idx, sudoku)
    blo = get_sudoku_blo(9*row_idx + col_idx, sudoku)

    row_mask = extract_exclusions(row_idx, possibility_grid)
    col_mask = extract_exclusions(col_idx, possibility_grid)

    block_idx = 3*(row_idx%3) + (col_idx%3)
    block_mask = extract_exclusions(block_idx, blo)

    total_mask = [ int(rb or cb or bb) for rb, cb, bb in zip(row_mask, col_mask, block_mask)]

    return total_mask
        
def extract_exclusions(current_idx, possibilities):
    non_current = [possibility for idx, possibility in enumerate(possibilities) if idx != current_idx]

    exclusion_mask = [0 for _ in range(9)]
    for possibility in non_current:
        if sum(possibility) != 1:
            continue
        else:
            idx = possibility.index(1)
            exclusion_mask[idx] = 1

    return exclusion_mask


if __name__ == "__main__":
    sudoku_str = "765082090913004080840030150209000546084369200006405000000040009090051024001890765"
    sudoku = produce_p_grid_from_sudoku_string(sudoku_str)
    print_sudoku(sudoku)
    print("\n")
    print(sudoku)