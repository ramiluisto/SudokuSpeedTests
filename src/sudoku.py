from itertools import product

SUDOKU_CONTENT_LEN = 81

sudoku_base = [0 for j in range(SUDOKU_CONTENT_LEN)]


def solve_sudoku(sudoku_list):

    p_grid = create_possibility_grid(sudoku_list)
    success_flag, res = recursive_solver(p_grid)

    if not success_flag:
        print('FAILURE')

    sudoku_list = reduce_from_p_grid(res)


    return sudoku_list


def reduce_from_p_grid(p_grid):
    sudoku_list = []
    for p in p_grid:
        
        if 1 in p:
            sudoku_list.append(p.index(1)+1)
        else:
            sudoku_list.append('X')

    return sudoku_list



def recursive_solver(loc_grid):
    simple_possibility_pruner(loc_grid)
    if not check_viability(loc_grid):
        return False, loc_grid

    first_unsolved_idx, iter_values = find_first_unsolved(loc_grid)

    if first_unsolved_idx == -1:
        return True, loc_grid

    for iter_val in iter_values:
        fixed_possibilities = [0 for _ in range(9)]
        fixed_possibilities[iter_val] = 1

        sub_grid = copy_possibility_grid(loc_grid)
        sub_grid[first_unsolved_idx] = fixed_possibilities
        
        success, iterated_grid = recursive_solver(sub_grid)

        if success:
            return True, iterated_grid

    return False, loc_grid
    
def find_first_unsolved(p_grid):
    unsolved_idx = -1
    for idx, possibilities in enumerate(p_grid):
        if sum(possibilities) >= 2:
            unsolved_idx = idx
            break
    
    if unsolved_idx != -1:
        lowest_possible_values = [idx for idx, value in enumerate(p_grid[unsolved_idx]) if value == 1]
    else:
        lowest_possible_values = []  
    

    return unsolved_idx, lowest_possible_values

def check_viability(p_grid):
    return all(sum(possibilities) >= 1 for possibilities in p_grid)


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


def copy_possibility_grid(p_grid):
    new_grid = [possibilities.copy() for possibilities in p_grid]
    return new_grid




###########################################

def pprint_sudoku(sudoku_list):
    res = sudoku_list

    row = 0
    col_block = 0
    row_block = 0
    for thing in res:
        print(thing if thing != 0 else '_', end=' ')
        row += 1
        col_block += 1

        if col_block >= 3:
            print(' ', end='')
            col_block = 0
        if row >= 9:
            print('')
            row = 0
            col_block = 0
            row_block += 1

        if row_block >= 3:
            print('')
            row_block = 0


if __name__ == '__main__':
    TEST_SUDOKU = [
    0,9,0, 0,4,0, 0,0,0,
    0,0,0, 0,8,6, 0,4,7,
    6,0,0, 0,0,1, 5,0,3,
    #
    7,0,4, 1,6,0, 3,8,2,
    9,3,6, 5,2,0, 0,1,4,
    0,8,0, 7,3,0, 0,0,0,
    #
    0,0,0, 0,0,3, 0,5,0,
    4,0,5, 0,1,0, 0,0,0,
    0,1,9, 0,0,0, 4,0,8,
    ]

 
    print('In:\n')
    pprint_sudoku(TEST_SUDOKU)
    res = solve_sudoku(TEST_SUDOKU)
    print('Out:\n')
    pprint_sudoku(res)
    print(res)

    sudo_in = [0 for _ in range(81)]
    print('In:\n')
    pprint_sudoku(sudo_in)
    res = solve_sudoku(sudo_in)
    print('Out:\n')
    pprint_sudoku(res)

    print(res)

    sudo_in = [0 for _ in range(81)]
    sudo_in[0] = 5
    sudo_in[8] = 5
    print('In:\n')
    pprint_sudoku(sudo_in)
    res = solve_sudoku(sudo_in)
    print('Out:\n')
    pprint_sudoku(res)

    print(res)

    from tqdm import tqdm

    with open('./data/minimal_lines.csv', 'r') as fp:
        datalines = fp.readlines()

    tally = 0
    for line in tqdm(datalines):
        unsolved, solved = line.split(',')
        unsolved = unsolved.strip(' \n')
        solved = solved.strip(' \n')

        in_sudoku = [int(val) for val in unsolved]
        result_sudoku = [int(val) for val in solved]

        result = solve_sudoku(in_sudoku)
        if result == result_sudoku:
            tally += 1

    print('\n\n')
    print('Yht:', tally)
    print('\n\n')