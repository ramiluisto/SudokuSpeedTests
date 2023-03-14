# My personal C vs Python speed analysis repo

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


The goal of this repo is to study the speed increases that **I as a particular 
Python dev** can achieve by going from 'naive Python' to using either more
pythonic tools, using C-powered libraries like numpy, or by at the extreme
using straight up C-code. The differences are benchmarked with a simple recursive Sudoku solver.

If you want to read of my (mis)adventures in this in a more verbose form, 
turn to reading [`ProgressDescription.md`](ProgressDescription.md) which is
a more diary-like description of what I've been doing.

### Why?

C is faster than Python. There is very little question about that. But
there is a much smaller difference between a Python program correctly using 
e.g. numpy, pandas or one of the other fast libraries with a C back-end.
In particular, in many cases (including mine) the important question is whether *I* 
the Python programmer could write C-code that runs faster than the implementations that rely
on the Python libraries whose C backends have been written by professional
C developers.

### How?

We're gonna look at a Sudoku solver. Right now there are the following Python versions (in the `./src`-folder):
- Simple naive solver (`naive_sudoku_solver.py`)
- OOP version of the naive solver (`OOP_sudoku.py`)
- Improved/optimized OOP version of the OOP solver (`OOP_sudoku_improved.py`)
- Numpy-based version of the solver (`numpy_sudoku.py`)

Besides these, we have a C-implementation (`./C-version/sudoku_solver.c`) which accepts sudokus either via .csv file addressess or cli input strings. Currently the only way to call this from Python
is via the naive version of using Python to run bash commands, see `./src/CLI_C_caller.py`. 


**Still in progress** 
- Version of the C-solver which allows us to call it as a total
or some of its subparts as Python packages.
- Cython implementation of the OOP solver.


## Getting started

To run the more naive C-approaches, you'll probably have to run this on Linux as the 
simplest Python C-utilization just runs bash commands of the type `"./C-version/a.out -r {input_sudoku} -S"`. For these to work, run `gcc sudoku_solver.c` in the folder `./C-version`. (I am very far from a C-developer, so caveats with all my advice in this.)

To get the Python C-extension moduler running, **after activating your virtual environment**,
run `python setup.py install` in the folder `./C-version`.

### Fast start:
```
conda create --name SudokuSpeedBenchmark python=3.10
conda activate SudokuSpeedBenchmark
pip install requirements.txt
cd C-version
python setup.py install
cd ..
python benchmark.py
```

### Testing

For Python:
```
coverage run -m pytest
coverage report -m
```
Currently all python tests have 100% coverage.

For C-code, go to folder `./C-version`, (compile) and run the result with
option `-t`, e.g.:
``` 
gcc sudoku_solver.c
./a.out -t
```
If this doesn't crash, then probably tests are okay. The tests here are 
more troubleshoot-tests than TDD-tests, and can be turned on or off
by commenting lines in the C source code.

# Todo / Ideas

Create a dict with precalculated block indeces?
- How about a dict that contains the "array_to_num" (and num_to_array) conversions?

Run better diagnostics on what takes most time

Check if OOP affects speed -- recurse the whole object.

Make a separate blog.md