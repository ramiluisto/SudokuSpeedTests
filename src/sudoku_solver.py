
from itertools import product

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

def p_grid_to_sudoku_string(sudoku) -> str:
    sudoku_list = []

    for idx in range(81):
        row_idx = idx//9
        col_idx = idx%9    
        if sum(sudoku[row_idx][col_idx]) == 1:
            num = 1+sudoku[row_idx][col_idx].index(1)
        else:
            num = 0
        sudoku_list.append(str(num))

    sudoku_str = ''.join(sudoku_list)
    
    return sudoku_str



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


################################################################
# The main recurser
################################################################

def recursive_solver(sudoku) -> bool:
    changed = True
    while(changed):
        changed = reduce_possibilities(sudoku)
        if not still_solvable(sudoku):
            return False

    cell_idx = first_unsolved_cell_index(sudoku)
    if cell_idx == -1:
        # If there is no unsolved cell, then the sudoku is complete.
        return True

    possibilities = get_cell_possibilities(cell_idx, sudoku)
    for fixed_number in possibilities:
        local_sudoku = create_copy_of_sudoku(sudoku)
        set_cell_of_sudoku(cell_idx, local_sudoku, fixed_number)
        result = recursive_solver(local_sudoku)
        if result:
            paste_local_sudoku_to_original(local_sudoku, sudoku)
            return True
  
    return False


################################################################
# Possibility reductions
################################################################

def reduce_possibilities(sudoku) -> bool:
    changes = False

    for idx in range(81):
        row_idx = idx//9
        col_idx = idx%9

        if sum(sudoku[row_idx][col_idx]) == 1:
            continue
        
        exclusion_mask = get_simple_mask(row_idx, col_idx, sudoku)
        new_possibilities = []
        for current, mask in zip(sudoku[row_idx][col_idx], exclusion_mask):
            if (current and not mask):
                new_value = 1
            else:
                new_value = 0
            
            if current != new_value:
                changes = True
            new_possibilities.append(new_value)

        sudoku[row_idx][col_idx] = new_possibilities

    return changes

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

def get_simple_mask(row_idx, col_idx, sudoku):

    row = get_sudoku_row(row_idx, sudoku)
    col = get_sudoku_col(col_idx, sudoku)
    blo = get_sudoku_blo(9*row_idx + col_idx, sudoku)

    # Note that here e.g. the within the row_mask the index of the current cell is given
    # by col_idx, and vice versa.
    row_mask = extract_exclusions(col_idx, row)
    col_mask = extract_exclusions(row_idx, col)

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


def still_solvable(sudoku):

    for j in range(9):
        row = get_sudoku_row(j, sudoku)
        collision = collision_in_collection(row)
        if collision:
            return False

        col = get_sudoku_col(j, sudoku)
        collision = collision_in_collection(col)
        if collision:
            return False

    for j in [0,3,6,27,30,33,54,57,60]:
        blo = get_sudoku_blo(j, sudoku)
        collision = collision_in_collection(blo)
        if collision:
            return False

    return all(sum(sudoku[i//9][i%9]) >= 1 for i in range(81))

def collision_in_collection(collection):
    numbers_in_collection = []
    for possibilities in collection:
        if sum(possibilities) == 1:
            num = 1+possibilities.index(1)
            numbers_in_collection.append(num)

    return len(set(numbers_in_collection)) < len(numbers_in_collection)

################################################################
# Recursive loop
################################################################

def first_unsolved_cell_index(sudoku):
    for idx in range(81):
        row_idx = idx//9
        col_idx = idx%9
        if sum(sudoku[row_idx][col_idx]) > 1:
            return idx

    return -1

def get_cell_possibilities(cell_idx, sudoku):
    row_idx = cell_idx//9
    col_idx = cell_idx%9

    possibility_mask = sudoku[row_idx][col_idx]
    possibilities = [idx + 1 for idx, value in enumerate(possibility_mask) if value == 1]

    return possibilities


def create_copy_of_sudoku(sudoku):
    base_p = 9*[1]
    p_grid = [[base_p.copy() for _ in range(9)] for j in range(9)]
    for idx in range(81):
        row_idx = idx//9
        col_idx = idx%9
        p_grid[row_idx][col_idx] = [value for value in sudoku[row_idx][col_idx]]

    return p_grid

def paste_local_sudoku_to_original(local_sudoku, sudoku):
    for idx in range(81):
        sudoku[idx//9][idx%9] = [ local_sudoku[idx//9][idx%9][j] for j in range(9)]


def set_cell_of_sudoku(cell_idx, sudoku, fixed_number):
    row_idx = cell_idx//9
    col_idx = cell_idx%9

    new_possibilities = [0]*9
    new_possibilities[fixed_number - 1] = 1

    sudoku[row_idx][col_idx] = new_possibilities

def read_and_solve_sudoku_from_string(sudoku_string):
    sudoku = produce_p_grid_from_sudoku_string(sudoku_string)
    success = recursive_solver(sudoku)
    result_string = p_grid_to_sudoku_string(sudoku)

    return result_string

if __name__ == "__main__":
    sudoku_str = "765082090913004080840030150209000546084369200006405000000040009090051024001890765"
    sudoku = produce_p_grid_from_sudoku_string(sudoku_str)
    print_sudoku(sudoku)  