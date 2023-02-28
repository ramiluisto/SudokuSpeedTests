from tqdm import tqdm
from src.sudoku_solver import read_and_solve_sudoku_from_string

with open('./data/10k_sudokus.csv', 'r') as fp:
    data = fp.readlines()

success_count = 0
for line in tqdm(data):
    puzzle, solved = line.strip('\n ').split(',')
    result = read_and_solve_sudoku_from_string(puzzle)
    if result == solved:
        success_count += 1

print(f"Success count: {success_count}/{len(data)}.")
