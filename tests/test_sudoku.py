import pytest
import src.sudoku_solver as sudoku_solver


@pytest.fixture
def simple_sudoku_string():
    sudoku = "765082090913004080840030150209000546084369200006405000000040009090051024001890765"
    return sudoku


def test_self():
    assert True


def test_produce_p_grid_from_sudoku_string(simple_sudoku_string):

    p_grid = sudoku_solver.produce_p_grid_from_sudoku_string(simple_sudoku_string)
    assert len(p_grid) == 9
    assert all(len(row) == 9 for row in p_grid)
    assert all( all(len(p) == 9 for p in row) for row in p_grid)
    assert not all( all( all(val == 1 for val in p) for p in row) for row in p_grid)

    p_grid = sudoku_solver.produce_p_grid_from_sudoku_string(81*"0")
    assert len(p_grid) == 9
    assert all(len(row) == 9 for row in p_grid)
    assert all( all(len(p) == 9 for p in row) for row in p_grid)
    assert all( all( all(val == 1 for val in p) for p in row) for row in p_grid)
