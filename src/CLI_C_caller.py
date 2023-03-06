import shutil
import os
import time


def read_and_solve_sudoku_from_string(input_sudoku: str) -> str:
    stream = os.popen(f"./C-version/a.out -r {input_sudoku} -S")
    output = stream.read()
    return output.strip("\n")


def run_C_benchmark(test_data) -> str:
    stream = os.popen(f'./C-version/a.out -B "{test_data}"')
    output = stream.read()

    return output
