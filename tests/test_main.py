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
    
    assert fourth_row == expection_translator(expected)

   
def expection_translator(old_data):
    new_version = []
    for p_list in old_data:
        new_p = [0 for _ in range(9)]
        for val in p_list:
            new_p[val-1] = 1

        new_version.append(new_p)

    return new_version
 

def test_get_col():
    p_grid = sudoku.create_possibility_grid(TEST_SUDOKU)
    fifth_col = sudoku.get_col(4, p_grid)
    expected = [[4], [8], list(range(1,10)), [6], [2], [3], list(range(1,10)), [1], list(range(1,10))]
    assert fifth_col == expection_translator(expected)

def test_get_block():
    p_grid = sudoku.create_possibility_grid(TEST_SUDOKU)
    middle_block = sudoku.get_block(4, 4, p_grid)
    expected = [[1], [6], list(range(1,10)), [5], [2], list(range(1,10)), [7], [3], list(range(1,10))]
    assert middle_block == expection_translator(expected)

def dont_test_simple_possibility_pruner():
    p_grid = sudoku.create_possibility_grid(TEST_SUDOKU)

    sudoku.simple_possibility_pruner(p_grid)

    orig_grid = sudoku.create_possibility_grid(TEST_SUDOKU)
    assert p_grid != orig_grid

    for new, old in zip(p_grid, orig_grid):
        assert all( value in old for value in new)


def test_extract_and_combine_exclusions():
    p_grid = sudoku.create_possibility_grid(TEST_SUDOKU)
    result = sudoku.extract_and_combine_exclusions(0,0,p_grid)
    assert result == [0,0,0,1,0,1,1,0,1]

    result = sudoku.extract_and_combine_exclusions(5,4,p_grid)
    assert result == [1,1,1,1,1,1,1,0,1]


def test_simple_possibility_pruner():
    p_grid = sudoku.create_possibility_grid(TEST_SUDOKU)

    sudoku.simple_possibility_pruner(p_grid)

    orig_grid = sudoku.create_possibility_grid(TEST_SUDOKU)
    assert p_grid != orig_grid

    for new, old in zip(p_grid, orig_grid):
        assert all(val_new <= val_old for val_new, val_old in zip(new, old))


    print('\noriginal')
    print(orig_grid[0])

    print('\nnew')
    print(p_grid[0])
    assert False