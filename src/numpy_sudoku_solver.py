import numpy as np


def print_sudoku(sudoku):
    TOP_ROW_FORMAT = "╔═══════╤═══════╤═══════╗"
    MID_ROW_FORMAT = "╟───────┼───────┼───────╢"
    BOT_ROW_FORMAT = "╚═══════╧═══════╧═══════╝"
    ROW_FORMAT = "║ {} {} {} │ {} {} {} │ {} {} {} ║"

    sudoku_nums = []
    for idx in range(81):
        row = idx // 9
        col = idx % 9

        array_sum = 0
        for i, p in enumerate(sudoku[row][col]):
            array_sum += p
            if p == 1:
                value = str(i + 1)

        if array_sum != 1:
            value = "_"

        sudoku_nums.append(value)

    print(TOP_ROW_FORMAT)
    for j in [0, 9, 18]:
        print(ROW_FORMAT.format(*sudoku_nums[j : j + 9]))
    print(MID_ROW_FORMAT)
    for j in [27, 36, 45]:
        print(ROW_FORMAT.format(*sudoku_nums[j : j + 9]))
    print(MID_ROW_FORMAT)
    for j in [54, 63, 72]:
        print(ROW_FORMAT.format(*sudoku_nums[j : j + 9]))
    print(BOT_ROW_FORMAT)



def string_to_p_grid(sudoku_string: str) -> np.array:
    separated_string = " ".join(list(sudoku_string))
    num_sudoku = np.fromstring(separated_string, dtype=np.int8, sep=" ")
    sudoku = np.zeros((9, 9, 9), dtype=np.int8)
    for idx, num in enumerate(num_sudoku):
        sudoku[idx // 9][idx % 9] = num_to_p_array(num)

    return sudoku


def num_to_p_array(num: int) -> np.array:
    if num == 0:
        p_array = np.ones(9, dtype=np.int8)
    else:
        p_array = np.zeros(9, dtype=np.int8)
        p_array[num - 1] = 1

    return p_array


def p_array_to_num(p_array: np.array) -> int:
    if p_array.sum() == 1:
        return 1 + np.where(p_array == 1)[0][0]
    else:
        return 0


def recursive_solver(sudoku) -> bool:
    changed = True
    while changed:
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


def reduce_possibilities(sudoku: np.array) -> bool:
    changes = False


def get_sudoku_row(row_idx: int, sudoku: np.array):
    return sudoku[row_idx, :, :]


def get_sudoku_col(col_idx: int, sudoku: np.array):
    return sudoku[:, col_idx, :]


def get_sudoku_block(cell_idx: int, sudoku: np.array):
    b_row = 3 * (idx // 27)
    b_col = 3 * ((idx // 3) % 3)
    block_selection_x = np.array([*3 * [b_row], *3 * [b_row + 1], *3 * [b_row + 2]])
    block_selection_y = np.array(3 * [b_col, b_col + 1, b_col + 2])


sudoku_string = (
    "536000000000703000100800059002000571600070008457010030061390705708620413300187600"
)
sudoku = string_to_p_grid(sudoku_string)
print_sudoku(sudoku)
print("Rows: ")
for j in range(9):
    row = get_sudoku_row(j, sudoku)
    print(f"{j}| ", end="")
    for i in range(9):
        print(p_array_to_num(row[i]), end=" ")
    print()

print_sudoku(sudoku)
print("Cols: ")
for j in range(9):
    row = get_sudoku_col(j, sudoku)
    print(f"{j}| ", end="")
    for i in range(9):
        print(p_array_to_num(row[i]), end=" ")
    print()

idx = 44
b_row = 3 * (idx // 27)
b_col = 3 * ((idx // 3) % 3)
print(f"\nSelecting block from index {idx}, topleft coords ({b_row}, {b_col})")
block_selection_x = np.array([*3 * [b_row], *3 * [b_row + 1], *3 * [b_row + 2]])
block_selection_y = np.array(3 * [b_col, b_col + 1, b_col + 2])
print(block_selection_x)
print(block_selection_y)
print_sudoku(sudoku)
print("Block: ")
block = sudoku[block_selection_x, block_selection_y, :]



row = sudoku[2]
print('Second row')
print(row)
summed_row = np.sum(row, axis = -1)
fixed_elts = np.where(summed_row ==1)[0]
fixed_rows = np.take(row, fixed_elts, axis = 0)
collisions = np.sum(fixed_rows, axis = 0)
print(f"Summed: {summed_row}")
print(f"Fixed elts: {fixed_elts}")
print(f"Fixed rows {fixed_rows}")
print(f"Collisions: {collisions}")

print(np.all(collisions <= 1))
collisions[2] = 4
print(collisions)
print(np.all(collisions <= 1))

print('\n\n')
print(row)
print(row.shape)
omitted = np.delete(row, [2], axis = 0)
print(omitted)
print(row.shape)


