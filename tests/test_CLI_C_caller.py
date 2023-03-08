import re
import src.CLI_C_caller as C_solver


def test_self():
    assert True

def test_read_and_solve_sudoku_from_string():
    sudo_in = "000809745589000000000000982700065000860000324010400060400006871070908450658104009"
    sudo_out = C_solver.read_and_solve_sudoku_from_string(sudo_in)

def test_run_C_benchmark():
    output = C_solver.run_C_benchmark('./data/100_sudokus.csv')
    matches = re.search("[\s]+([\d]+)[\s]*\/[\s]*([\d]+)", output)
    success_count = int(matches[1])
    total = int(matches[2])
    success_count == total