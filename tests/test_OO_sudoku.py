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


def test_first_unsolved_cell_index(
    simple_sudoku_object,
    simple_solved_sudoku_object
):
    assert (
        simple_sudoku_object.first_unsolved_cell_index == 3
    )
    assert (
        simple_solved_sudoku_object.first_unsolved_cell_index == -1
    )

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
        assert not simple_sudoku_object.collision_in_collection(simple_sudoku_object.row(j))

        

    bad_string = 72 * "0" + "10000001"
    sudoku = sudoku_solver.Sudoku(bad_string)  
    assert simple_sudoku_object.collision_in_collection(sudoku.row(8))
    assert not simple_sudoku_object.collision_in_collection(sudoku.row(5))



