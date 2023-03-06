from tqdm import tqdm
import re
import time
import cProfile

from src.naive_sudoku_solver import read_and_solve_sudoku_from_string as naive_solver
from src.OOP_sudoku import read_and_solve_sudoku_from_string as oop_solver
from src.CLI_C_caller import read_and_solve_sudoku_from_string as convoluted_C_solver
from src.CLI_C_caller import run_C_benchmark

with open("./data/10k_sudokus.csv", "r") as fp:
    benchmark_data_10k = fp.readlines()


def run_benchmark(algo_to_use, title, data = benchmark_data_10k):
    print(80*'*')
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
    print(f"Success count: {success_count:>8}/{len(data):>8} ({success_count/len(data):>3.1%})")
    print(f"Time: {tock-tick:>8.2} seconds for {len(data)} data. ({(tock-tick)/len(data):>1.1e} secs per sudoku)")

def run_C_benchmark_wrapper(title):
    test_data_filepath = './data/10k_sudokus.csv'    
    print(80*'*')
    print(f"Running benchmark for {title}: ")

    tick = time.time()    
    output = run_C_benchmark(test_data_filepath)
    tock = time.time()

    matches = re.search("[\s]+([\d]+)[\s]*\/[\s]*([\d]+)", output)
    success_count = int(matches[1])
    total =int(matches[2])

    print(f"{title} done!")
    print(f"Success count: {success_count:>8}/{total:>8} ({success_count/total:>3.1%})")
    print(f"Time: {tock-tick:>8.2} seconds for {total} data. ({(tock-tick)/total:>1.1e} secs per sudoku)")


if __name__ == "__main__":
    
    run_benchmark(naive_solver, "Naive solver")
    #run_benchmark(oop_solver, "OOP solver")
    #run_benchmark(convoluted_C_solver, "Convoluted C-solver")
    #run_C_benchmark_wrapper("Wrapped C-Benchmark tool")

