import src.OOP_sudoku as sudoku_solver
import pytest

from tests.joint_fixtures import *


@pytest.fixture
def simple_sudoku_object(simple_sudoku_string):
    Sudoku = sudoku_solver.Sudoku(simple_sudoku_string)
    return Sudoku


@pytest.fixture
def simple_solved_sudoku_object(simple_sudoku_string_solved):
    Sudoku = sudoku_solver.Sudoku(simple_sudoku_string_solved)
    return Sudoku


@pytest.fixture
def hard_sudoku_object(hard_string):
    Sudoku = sudoku_solver.Sudoku(hard_string)
    return Sudoku


def test_self():
    assert True


def test_initialization(simple_sudoku_string):
    Sudoku = sudoku_solver.Sudoku(simple_sudoku_string)


def test_stringification(simple_sudoku_string, simple_sudoku_object):
    assert str(simple_sudoku_object) == simple_sudoku_string


def test_get_sudoku_row(simple_sudoku_object):
    row = simple_sudoku_object.row(0)
    pruned_row = [p_grid_elt_translator(p) for p in row]
    assert pruned_row == [7, 6, 5, 0, 8, 2, 0, 9, 0]

    row = simple_sudoku_object.row(8)
    pruned_row = [p_grid_elt_translator(p) for p in row]
    assert pruned_row == [0, 0, 1, 8, 9, 0, 7, 6, 5]


def test_get_sudoku_col(simple_sudoku_object):
    col = simple_sudoku_object.col(0)
    pruned_col = [p_grid_elt_translator(p) for p in col]
    assert pruned_col == [7, 9, 8, 2, 0, 0, 0, 0, 0]

    col = simple_sudoku_object.col(7)
    pruned_col = [p_grid_elt_translator(p) for p in col]
    assert pruned_col == [9, 8, 5, 4, 0, 0, 0, 2, 6]


def test_get_sudoku_blo(simple_sudoku_object):
    blo = simple_sudoku_object.block(0)
    pruned_blo = [p_grid_elt_translator(p) for p in blo]
    assert pruned_blo == [7, 6, 5, 9, 1, 3, 8, 4, 0]

    blo = simple_sudoku_object.block(31)
    pruned_blo = [p_grid_elt_translator(p) for p in blo]
    assert pruned_blo == [0, 0, 0, 3, 6, 9, 4, 0, 5]

    blo = simple_sudoku_object.block(41)
    pruned_blo = [p_grid_elt_translator(p) for p in blo]
    assert pruned_blo == [0, 0, 0, 3, 6, 9, 4, 0, 5]

    blo = simple_sudoku_object.block(48)
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


def test_first_unsolved_cell_index(simple_sudoku_object, simple_solved_sudoku_object):
    assert simple_sudoku_object.first_unsolved_cell_index == 3
    assert simple_solved_sudoku_object.first_unsolved_cell_index == -1


def test_still_solvable(simple_sudoku_object, simple_solved_sudoku_object):
    assert simple_sudoku_object.still_solvable

    simple_sudoku_object.sudoku[7][7] = [0] * 9
    assert not simple_sudoku_object.still_solvable

    bad_row = 72 * "0" + "10000001"
    sudoku = sudoku_solver.Sudoku(bad_row)
    assert not sudoku.still_solvable

    bad_col = 4 * "0" + "1" + 4 * "0" + 63 * "0" + 4 * "0" + "1" + 4 * "0"
    sudoku = sudoku_solver.Sudoku(bad_col)
    assert not sudoku.still_solvable

    bad_block = 71 * "0" + "100000001"
    sudoku = sudoku_solver.Sudoku(bad_block)
    assert not sudoku.still_solvable

    assert simple_solved_sudoku_object.still_solvable


def test_collision_in_collection(simple_sudoku_object):
    for j in range(9):
        assert not simple_sudoku_object.collision_in_collection(
            simple_sudoku_object.row(j)
        )

    bad_string = 72 * "0" + "10000001"
    sudoku = sudoku_solver.Sudoku(bad_string)
    assert simple_sudoku_object.collision_in_collection(sudoku.row(8))
    assert not simple_sudoku_object.collision_in_collection(sudoku.row(5))


def test_extract_exclusions(simple_sudoku_object):
    possibility_grid = simple_sudoku_object.sudoku[0]
    result = simple_sudoku_object.extract_exclusions(0, possibility_grid)
    assert result == [0, 1, 0, 0, 1, 1, 0, 1, 1]

    possibility_grid = simple_sudoku_object.sudoku[3]
    result = simple_sudoku_object.extract_exclusions(8, possibility_grid)
    assert result == [0, 1, 0, 1, 1, 0, 0, 0, 1]


def test_get_simple_mask(simple_sudoku_object):
    total_mask = simple_sudoku_object.get_simple_mask(0, 0)
    assert total_mask == [1, 1, 1, 1, 1, 1, 0, 1, 1]

    total_mask = simple_sudoku_object.get_simple_mask(1, 1)
    assert total_mask == [0, 0, 1, 1, 1, 1, 1, 1, 1]

    total_mask = simple_sudoku_object.get_simple_mask(2, 2)
    assert total_mask == [1, 0, 1, 1, 1, 1, 1, 1, 1]


def test_reduce_possibilities(simple_sudoku_object):
    assert simple_sudoku_object.sudoku[2][2] == [1] * 9
    one_change = simple_sudoku_object.reduce_possibilities()
    assert simple_sudoku_object.sudoku[2][2] == [0, 1, 0, 0, 0, 0, 0, 0, 0]
    assert one_change

    second_change = simple_sudoku_object.reduce_possibilities()
    assert second_change

    third_change = simple_sudoku_object.reduce_possibilities()
    assert third_change

    fourth_change = simple_sudoku_object.reduce_possibilities()
    assert not fourth_change


def test_set_cell_of_sudoku(simple_sudoku_object):
    for j in range(1, 10):
        simple_sudoku_object.set_cell_of_sudoku(0, j)
        for val in range(9):
            if val == j - 1:
                assert simple_sudoku_object.sudoku[0][0][val] == 1
            else:
                assert simple_sudoku_object.sudoku[0][0][val] == 0

    for j in range(1, 10):
        simple_sudoku_object.set_cell_of_sudoku(77, j)
        for val in range(9):
            if val == j - 1:
                assert simple_sudoku_object.sudoku[8][5][val] == 1
            else:
                assert simple_sudoku_object.sudoku[8][5][val] == 0


def test_create_copy_of_sudoku(simple_sudoku_object):
    copied_sudoku = simple_sudoku_object.copy()

    for cell_idx in range(81):
        for p_idx in range(9):
            copied_sudoku.sudoku[cell_idx // 9][cell_idx % 9][
                p_idx
            ] == simple_sudoku_object.sudoku[cell_idx // 9][cell_idx % 9][p_idx]

    assert id(copied_sudoku) != id(simple_sudoku_object)

    simple_sudoku_object.sudoku[0][0][0] = -1
    assert copied_sudoku.sudoku[0][0][0] != -1


def test_import_p_grid(simple_sudoku_object):
    copied_sudoku = simple_sudoku_object.copy()
    copied_sudoku.sudoku[0][0][0] = 5

    id_before = id(simple_sudoku_object)
    simple_sudoku_object.import_p_grid(copied_sudoku)
    assert id(simple_sudoku_object) == id_before
    assert id(copied_sudoku) != id_before
    assert id(copied_sudoku) != id(simple_sudoku_object)
    assert simple_sudoku_object.sudoku[0][0][0] == 5


def test_recursive_solver(simple_sudoku_object, hard_sudoku_object):
    assert simple_sudoku_object.recursive_solver()
    assert simple_sudoku_object.first_unsolved_cell_index == -1

    assert hard_sudoku_object.recursive_solver()


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
    with open("./tests/test_data/25_sudokus.csv", "r") as fp:
        data = fp.readlines()

    for line in data[:24]:
        line = line.strip("\n ")
        orig, solved = line.split(",")
        result = sudoku_solver.read_and_solve_sudoku_from_string(orig)
        assert result == solved
