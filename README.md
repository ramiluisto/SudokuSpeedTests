# My personal speed analysis repo

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [Test coverage: full](https://img.shields.io/badge/coverage-100%25-green)


The goal of this repo is to study the speed increases that **I as a particular 
Python dev** can achieve by going from 'naive Python' to using either more
pythonic tools, using C-powered libraries like numpy, or by at the extreme
using straight up C-code. The differences are benchmarked with a simple recursive Sudoku solver.

## Introduction

Here I'm describing some general ideas. If you just wanna get started and see
the various benchmarks jump to the section ('Getting Started').

### Why?

C is faster than Python. There is very little question about that. But
there is a much smaller difference between a Python program correctly using 
e.g. numpy, pandas or one of the other fast libraries with a C back-end.
In particular, in many cases (including mine) the important question is whether *I* 
the Python programmer could write C-code that runs faster than the implementations that rely
on the Python libraries whose C backends have been written by professional
C developers.

### How?

We're gonna look at a Sudoku solver.
- Custom made
- Recursive
- Too easy for numpy?


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

Make a separate blog.md