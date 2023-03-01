from tqdm import tqdm
import time
from src.naive_sudoku_solver import read_and_solve_sudoku_from_string as naive_solver
from src.OOP_sudoku import read_and_solve_sudoku_from_string as oop_solver


with open("./data/10k_sudokus.csv", "r") as fp:
    benchmark_data_10k = fp.readlines()


def run_benchmark(algo_to_use, title, data=benchmark_data_10k):
    print(80 * "*")
    print(f"Running benchmark for {title}: ")

    tick = time.time()
    success_count = 0
    for line in tqdm(data):
        puzzle, solved = line.strip("\n ").split(",")
        result = algo_to_use(puzzle)
        if result == solved:
            success_count += 1
    tock = time.time()

    print(f"{title} done!")
    print(
        f"Success count: {success_count:>8}/{len(data):>8} ({success_count/len(data):>3.1%})"
    )
    print(
        f"Time: {tock-tick:>8.2} seconds for {len(data)} data. ({(tock-tick)/len(data):>1.1e} secs per sudoku)"
    )


if __name__ == "__main__":
    run_benchmark(naive_solver, "Naive solver")
    run_benchmark(oop_solver, "OOP solver")
