import src.sudoku as sudoku

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

def test_self():
    assert True

def test_get_xy():
    x,y = sudoku.get_xy(5)
    assert x == 5
    assert y == 0

def test_create_possibility_grid():
    p_grid = sudoku.create_possibility_grid(TEST_SUDOKU)
    assert len(p_grid) == len(TEST_SUDOKU)
    assert all( type(possibilities) == list for possibilities in p_grid)

def test_get_row():
    p_grid = sudoku.create_possibility_grid(TEST_SUDOKU)
    fourth_row = sudoku.get_row(3, p_grid)
    expected = [[7], list(range(1,10)), [4], [1], [6], list(range(1,10)), [3], [8], [2]]
    assert fourth_row == expected

def test_get_col():
    p_grid = sudoku.create_possibility_grid(TEST_SUDOKU)
    fifth_col = sudoku.get_col(4, p_grid)
    expected = [[4], [8], list(range(1,10)), [6], [2], [3], list(range(1,10)), [1], list(range(1,10))]
    assert fifth_col == expected

def test_get_block():
    p_grid = sudoku.create_possibility_grid(TEST_SUDOKU)
    middle_block = sudoku.get_block(4, 4, p_grid)
    expected = [[1], [6], list(range(1,10)), [5], [2], list(range(1,10)), [7], [3], list(range(1,10))]
    assert middle_block == expected

def test_simple_possibility_pruner():
    p_grid = sudoku.create_possibility_grid(TEST_SUDOKU)

    sudoku.simple_possibility_pruner(p_grid)

    orig_grid = sudoku.create_possibility_grid(TEST_SUDOKU)
    assert p_grid != orig_grid

    for new, old in zip(p_grid, orig_grid):
        assert all( value in old for value in new)


def test_extract_and_combine_exclusions():
    p_grid = sudoku.create_possibility_grid(TEST_SUDOKU)
    result = sudoku.extract_and_combine_exclusions(0,0,p_grid)
    assert result == [4,6,7,9]

    result = sudoku.extract_and_combine_exclusions(5,4,p_grid)
    assert result == [1,2,3,4,5,6,7,9]

    