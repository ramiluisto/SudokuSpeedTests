# My personal speed analysis repo

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Test coverage: full](https://img.shields.io/badge/coverage-100%25-green)



The goal of this repo is to study the speed increases that can be achived
from going first from 'naive Python' to 'numpy Python', and then to either
building specific crucial parts as C-libraries, or to building the whole system
in C. The differences are benchmarked with a simple recursive Sudoku solver.

## Introduction

Here I'm describing some general ideas. If you just wanna get started, 
jump to the next section ('Getting Started').

### Why?

C is faster than Python. There is very little question about that. But
there is a much smaller difference between a Python program correctly using 
e.g. numpy, pandas or one of the other fast libraries with a C back-end.
In particular, in many cases (including mine) the important question is whether *I* 
the Python programmer could write C-code that runs faster than the implementations that rely
on the Python libraries whose C backends have been written by professional
C developers.

### How?

To choose a target, we're gonna look at a straightforward recursive Sudoku solver. 
To put all to the same page with the terminology, a [sudoku](https://en.wikipedia.org/wiki/Sudoku)
is a logical game where you have a 9x9 grid divided into 9 3x3 blocks:

<img src="./images/Sudoku.svg">


The rule of the game is to fill the grid with numbers 1-9 such that any row, column or block
contains each of the numbers 1-9 exactly once. The difficulty of the game depends on which 
cells have been pre-filled with which numbers. Estimating the difficulty of a sudoku is
a non-trivial task, though given starting configuration adding legal numbers always
makes it easier. (Removing them might not as multiple solutions might emerge by reducing
restrictions.)

For the system we'll handle data input and output as strings of numbers, i.e. a single
sudoku will be an string of length 81, with each character one of the numbers 0-9. Here
with a 0 we will mean that a cell is unfilled. The numbers in this string are taken to 
be in such an order that they fill the standard 9x9 grid one by one, starting from top left
and moving through the cells left to right, top to bottom.


Pseudocode for the solver.
```python
def recursive_solver(sudoku : ThreeDimensionalArray) -> bool:

    changed = True
    while(changed):
        changed = reduce_possibilities(sudoku)

    if is_solved(sudoku):
        return True

    cell_idx = first_unsolved_cell_index(sudoku)
    possibilities = get_cell_possibilities(cell_idx, sudoku)
    for p in possibilities:
        local_sudoku = sudoku.copy()
        set_cell_of_sudoku(cell_idx, local_sudoku, p)

        result = recursive_solver(local_sudoku)
        if result:
            return True

    return False
```

### (On) what?

I found a nice open source sudoku source on kaggle: LINK


## Results

The main idea is that I take turns improving my Python solvers and C solvers, with the aim of
alternatively trying to close the gap with the Python versions and then trying to expand the
gap with C versions.

### The baseline - Simple Python vs Simple C

I started by building a very straightforward implementation in Python (`./src/naive_sudoku_solver.py`).
It's called naive because it doesn't do anything fancy, though it aims to be as pythonic as possible
and not do too much obviously stupid things. On the benchmark machine (Azure VM of style XXX) it solved
10k sudokus in just under 50 seconds.

To compete the naive Python version, I then made a simple C-version. I call it simple because simple
C is the best I can do, and it probably does some obviously stupid things as well because I don't 
have a good touch to C. But in any case it runs and using the same algorithm it solves the same 10k
sudokus in about 5 seconds - so an order of magnitude improvement right off the bat. 

So C 1, Python 0 at this point. Let's see how we could start improving the Python version a bit.


### 


## Getting started


### Fast start:
```
conda create --name SudokuSpeedBenchmark python=3.10
conda activate SudokuSpeedBenchmark
pip install requirements.txt
python benchmark.py
```

### Exploratory start:

```
conda create --name SudokuSpeedExploratory python=3.10
conda activate SudokuSpeedExploratory
pip install requirements.txt
```
Then open the `Exploration.ipynb` -notebook and read on.


# Todo / Ideas

Create a dict with precalculated block indeces?
- How about a dict that contains the "array_to_num" (and num_to_array) conversions?

Run better diagnostics on what takes most time

Check if OOP affects speed -- recurse the whole object.

