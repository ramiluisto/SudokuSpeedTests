


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



