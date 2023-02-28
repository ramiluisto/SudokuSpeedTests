import pytest
import src.utils as utils
import src.naive_sudoku_solver as naive_sudoku_solver

from tests.joint_fixtures import *


def test_print_sudoku(capfd, simple_sudoku_naive_p_grid):
    utils.print_sudoku(simple_sudoku_naive_p_grid)
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

    assert (
        naive_sudoku_solver.convert_sudoku_string_to_p_grid(pruned)
        == simple_sudoku_naive_p_grid
    )
