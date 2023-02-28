import pytest
import src.sudoku_solver as sudoku_solver


from tests.joint_fixtures import *


@pytest.fixture
def hard_p_grid(hard_string):
    p_grid = sudoku_solver.convert_sudoku_string_to_p_grid(hard_string)
    return p_grid


def test_self():
    assert True


def test_produce_p_grid_from_sudoku_string(simple_sudoku_string, simple_sudoku_naive_p_grid):
    p_grid = sudoku_solver.convert_sudoku_string_to_p_grid(simple_sudoku_string)
    assert len(p_grid) == 9
    assert all(len(row) == 9 for row in p_grid)
    assert all(all(len(p) == 9 for p in row) for row in p_grid)
    assert not all(all(all(val == 1 for val in p) for p in row) for row in p_grid)

    assert p_grid == simple_sudoku_naive_p_grid

    p_grid = sudoku_solver.convert_sudoku_string_to_p_grid(81 * "0")
    assert len(p_grid) == 9
    assert all(len(row) == 9 for row in p_grid)
    assert all(all(len(p) == 9 for p in row) for row in p_grid)
    assert all(all(all(val == 1 for val in p) for p in row) for row in p_grid)


def test_print_sudoku(capfd, simple_sudoku_naive_p_grid):
    sudoku_solver.print_sudoku(simple_sudoku_naive_p_grid)
    out, err = capfd.readouterr()

    # If the formatting is changed, this should be removed.
    # The latter test is much more general.
    assert (
        out
        == "╔═══════╤═══════╤═══════╗\n║ 7 6 5 │ _ 8 2 │ _ 9 _ ║\n║ 9 1 3 │ _ _ 4 │ _ 8 _ ║\n║ 8 4 _ │ _ 3 _ │ 1 5 _ ║\n╟───────┼───────┼───────╢\n║ 2 _ 9 │ _ _ _ │ 5 4 6 ║\n║ _ 8 4 │ 3 6 9 │ 2 _ _ ║\n║ _ _ 6 │ 4 _ 5 │ _ _ _ ║\n╟───────┼───────┼───────╢\n║ _ _ _ │ _ 4 _ │ _ _ 9 ║\n║ _ 9 _ │ _ 5 1 │ _ 2 4 ║\n║ _ _ 1 │ 8 9 _ │ 7 6 5 ║\n╚═══════╧═══════╧═══════╝\n"
    )

    # The following tests if the printed output has the same content as the input string.
    pruned = []
    for char in out:
        if char in [str(val) for val in range(0, 10)]:
            pruned.append(char)
        if char == "_":
            pruned.append("0")
    pruned = "".join(pruned)

    assert sudoku_solver.convert_sudoku_string_to_p_grid(pruned) == simple_sudoku_naive_p_grid


def test_get_sudoku_row(simple_sudoku_naive_p_grid):
    row = sudoku_solver.get_sudoku_row(0, simple_sudoku_naive_p_grid)
    pruned_row = [p_grid_elt_translator(p) for p in row]
    assert pruned_row == [7, 6, 5, 0, 8, 2, 0, 9, 0]

    row = sudoku_solver.get_sudoku_row(8, simple_sudoku_naive_p_grid)
    pruned_row = [p_grid_elt_translator(p) for p in row]
    assert pruned_row == [0, 0, 1, 8, 9, 0, 7, 6, 5]


def test_get_sudoku_col(simple_sudoku_naive_p_grid):
    col = sudoku_solver.get_sudoku_col(0, simple_sudoku_naive_p_grid)
    pruned_col = [p_grid_elt_translator(p) for p in col]
    assert pruned_col == [7, 9, 8, 2, 0, 0, 0, 0, 0]

    col = sudoku_solver.get_sudoku_col(7, simple_sudoku_naive_p_grid)
    pruned_col = [p_grid_elt_translator(p) for p in col]
    assert pruned_col == [9, 8, 5, 4, 0, 0, 0, 2, 6]


def test_get_sudoku_blo(simple_sudoku_naive_p_grid):
    blo = sudoku_solver.get_sudoku_blo(0, simple_sudoku_naive_p_grid)
    pruned_blo = [p_grid_elt_translator(p) for p in blo]
    assert pruned_blo == [7, 6, 5, 9, 1, 3, 8, 4, 0]

    blo = sudoku_solver.get_sudoku_blo(31, simple_sudoku_naive_p_grid)
    pruned_blo = [p_grid_elt_translator(p) for p in blo]
    assert pruned_blo == [0, 0, 0, 3, 6, 9, 4, 0, 5]

    blo = sudoku_solver.get_sudoku_blo(41, simple_sudoku_naive_p_grid)
    pruned_blo = [p_grid_elt_translator(p) for p in blo]
    assert pruned_blo == [0, 0, 0, 3, 6, 9, 4, 0, 5]

    blo = sudoku_solver.get_sudoku_blo(48, simple_sudoku_naive_p_grid)
    pruned_blo = [p_grid_elt_translator(p) for p in blo]
    assert pruned_blo == [0, 0, 0, 3, 6, 9, 4, 0, 5]


def p_grid_elt_translator(element):
    if sum(element) == 1:
        return 1 + element.index(1)
    else:
        return 0


def test_p_grid_elt_translator():
    for j in range(9):
        data = [0] * 9
        data[j] = 1
        assert p_grid_elt_translator(data) == j + 1
    assert p_grid_elt_translator([0] * 9) == 0
    assert p_grid_elt_translator([0, 1, 0, 0, 0, 1, 0, 0, 0]) == 0


def test_extract_exclusions(simple_sudoku_naive_p_grid):
    possibility_grid = simple_sudoku_naive_p_grid[0]
    result = sudoku_solver.extract_exclusions(0, possibility_grid)
    assert result == [0, 1, 0, 0, 1, 1, 0, 1, 1]

    possibility_grid = simple_sudoku_naive_p_grid[3]
    result = sudoku_solver.extract_exclusions(8, possibility_grid)
    assert result == [0, 1, 0, 1, 1, 0, 0, 0, 1]


def test_get_simple_mask(simple_sudoku_naive_p_grid):
    total_mask = sudoku_solver.get_simple_mask(0, 0, simple_sudoku_naive_p_grid)
    assert total_mask == [1, 1, 1, 1, 1, 1, 0, 1, 1]

    total_mask = sudoku_solver.get_simple_mask(1, 1, simple_sudoku_naive_p_grid)
    assert total_mask == [0, 0, 1, 1, 1, 1, 1, 1, 1]

    total_mask = sudoku_solver.get_simple_mask(2, 2, simple_sudoku_naive_p_grid)
    assert total_mask == [1, 0, 1, 1, 1, 1, 1, 1, 1]


def test_reduce_possibilities(simple_sudoku_naive_p_grid):
    assert simple_sudoku_naive_p_grid[2][2] == [1] * 9
    one_change = sudoku_solver.reduce_possibilities(simple_sudoku_naive_p_grid)
    assert simple_sudoku_naive_p_grid[2][2] == [0, 1, 0, 0, 0, 0, 0, 0, 0]
    assert one_change

    second_change = sudoku_solver.reduce_possibilities(simple_sudoku_naive_p_grid)
    assert second_change

    third_change = sudoku_solver.reduce_possibilities(simple_sudoku_naive_p_grid)
    assert third_change

    fourth_change = sudoku_solver.reduce_possibilities(simple_sudoku_naive_p_grid)
    assert not fourth_change


def test_first_unsolved_cell_index(simple_sudoku_naive_p_grid, simple_sudoku_naive_p_grid_solved):
    assert sudoku_solver.first_unsolved_cell_index(simple_sudoku_naive_p_grid) == 3
    assert sudoku_solver.first_unsolved_cell_index(simple_sudoku_naive_p_grid_solved) == -1


def test_get_cell_possibilities(simple_sudoku_naive_p_grid):
    assert sudoku_solver.get_cell_possibilities(0, simple_sudoku_naive_p_grid) == [7]
    assert sudoku_solver.get_cell_possibilities(3, simple_sudoku_naive_p_grid) == list(
        range(1, 10)
    )
    one_change = sudoku_solver.reduce_possibilities(simple_sudoku_naive_p_grid)
    assert sudoku_solver.get_cell_possibilities(3, simple_sudoku_naive_p_grid) == [1]
    assert sudoku_solver.get_cell_possibilities(7, simple_sudoku_naive_p_grid) == [9]
    assert sudoku_solver.get_cell_possibilities(12, simple_sudoku_naive_p_grid) == [5, 6, 7]


def test_create_copy_of_sudoku(simple_sudoku_naive_p_grid):
    copy_grid = sudoku_solver.create_copy_of_sudoku(simple_sudoku_naive_p_grid)

    assert copy_grid == simple_sudoku_naive_p_grid
    assert id(copy_grid) != id(simple_sudoku_naive_p_grid)

    simple_sudoku_naive_p_grid[0][0][0] = -1
    assert copy_grid[0][0][0] != -1


def test_set_cell_of_sudoku(simple_sudoku_naive_p_grid):
    for j in range(1, 10):
        sudoku_solver.set_cell_of_sudoku(0, simple_sudoku_naive_p_grid, j)
        for val in range(9):
            if val == j - 1:
                assert simple_sudoku_naive_p_grid[0][0][val] == 1
            else:
                assert simple_sudoku_naive_p_grid[0][0][val] == 0

    for j in range(1, 10):
        sudoku_solver.set_cell_of_sudoku(77, simple_sudoku_naive_p_grid, j)
        for val in range(9):
            if val == j - 1:
                assert simple_sudoku_naive_p_grid[8][5][val] == 1
            else:
                assert simple_sudoku_naive_p_grid[8][5][val] == 0


def test_recursive_solver(simple_sudoku_naive_p_grid, hard_p_grid):
    assert sudoku_solver.recursive_solver(simple_sudoku_naive_p_grid)
    assert sudoku_solver.first_unsolved_cell_index(simple_sudoku_naive_p_grid) == -1

    assert sudoku_solver.recursive_solver(hard_p_grid)


def test_p_grid_to_sudoku_string(simple_sudoku_string, simple_sudoku_naive_p_grid):
    assert simple_sudoku_string == sudoku_solver.convert_p_grid_to_sudoku_string(
        simple_sudoku_naive_p_grid
    )


def test_collision_in_collection(simple_sudoku_naive_p_grid):
    for j in range(9):
        assert not sudoku_solver.collision_in_collection(simple_sudoku_naive_p_grid[j])

    bad_string = 72 * "0" + "10000001"
    sudoku = sudoku_solver.convert_sudoku_string_to_p_grid(bad_string)
    assert sudoku_solver.collision_in_collection(sudoku[8])
    assert not sudoku_solver.collision_in_collection(sudoku[5])


def test_still_solvable(simple_sudoku_naive_p_grid):
    assert sudoku_solver.still_solvable(simple_sudoku_naive_p_grid)

    simple_sudoku_naive_p_grid[7][7] = [0] * 9
    assert not sudoku_solver.still_solvable(simple_sudoku_naive_p_grid)

    bad_row = 72 * "0" + "10000001"
    sudoku = sudoku_solver.convert_sudoku_string_to_p_grid(bad_row)
    assert not sudoku_solver.still_solvable(sudoku)

    bad_col = 4 * "0" + "1" + 4 * "0" + 63 * "0" + 4 * "0" + "1" + 4 * "0"
    sudoku = sudoku_solver.convert_sudoku_string_to_p_grid(bad_col)
    assert not sudoku_solver.still_solvable(sudoku)

    bad_block = 71 * "0" + "100000001"
    sudoku = sudoku_solver.convert_sudoku_string_to_p_grid(bad_block)
    print("\n\nLooking at bad blocks")
    assert not sudoku_solver.still_solvable(sudoku)


def test_read_and_solve_sudoku_from_string(
    simple_sudoku_string, simple_sudoku_string_solved, sudoku_string_test_pairs
):
    result = sudoku_solver.read_and_solve_sudoku_from_string(simple_sudoku_string)
    assert result == simple_sudoku_string_solved

    for pair in sudoku_string_test_pairs:
        sudoku, solution = pair
        result = sudoku_solver.read_and_solve_sudoku_from_string(sudoku)
        assert result == solution


def test_solver_with_25_sudokus():
    with open('./tests/test_data/25_sudokus.csv', 'r') as fp:
        data = fp.readlines()

    for line in data[:24]:
        line = line.strip("\n ")
        orig, solved = line.split(",")
        result = sudoku_solver.read_and_solve_sudoku_from_string(orig)
        assert result == solved
