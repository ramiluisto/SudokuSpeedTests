from itertools import product

SUDOKU_CONTENT_LEN = 81

sudoku_base = [0 for j in range(SUDOKU_CONTENT_LEN)]




def create_possibility_grid(sudoku_list):
    possibility_grid = []
    for value in sudoku_list:
        assert value in range(0,10)

        if value == 0:
            possibilities = [1 for _ in range(9)]

        else:
            possibilities = [0 for _ in range(9)]
            possibilities[value-1] = 1

        possibility_grid.append(possibilities)

    return possibility_grid


def simple_possibility_pruner(possibility_grid):
    for sudoku_index, possibilities in enumerate(possibility_grid):
        x,y = get_xy(sudoku_index)
        exclusion_mask = extract_and_combine_exclusions(x,y, possibility_grid)

        new_possibilities = [int(current and not new) for current, new in zip(possibilities, exclusion_mask)]
        possibility_grid[sudoku_index] = new_possibilities


def extract_and_combine_exclusions(x, y, possibility_grid):
    row = get_row(y, possibility_grid)
    col = get_col(x, possibility_grid)
    block = get_block(x, y, possibility_grid)

    row_mask = extract_exclusions(x, row)
    col_mask = extract_exclusions(y, col)

    block_idx = (y%3)*3 + (x%3)
    block_mask = extract_exclusions(block_idx, block)

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





def get_xy(sudoku_index):
    x = sudoku_index % 9
    y = sudoku_index // 9

    return x, y

def get_row(y, p_grid):
    row_data = p_grid[9*y : 9*(y+1) : 1]
    return row_data

def get_col(x, p_grid):
    col_data = p_grid[x : 81 : 9]
    return col_data

def get_block(x, y, p_grid):
    block_x = x//3
    block_y = y//3

    top_left = 27*block_y + 3*block_x
    indeces = [top_left + x_shift + y_shift for x_shift, y_shift in product(range(3), range(0,27,9))]
    indeces.sort()

    block_possibilities = [p_grid[idx] for idx in indeces]

    return block_possibilities
