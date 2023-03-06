# Story mode description 




To choose a target, we're gonna look at a straightforward recursive Sudoku solver. 
To put all to the same page with the terminology, a [sudoku](https://en.wikipedia.org/wiki/Sudoku)
is a logical game where you have a 9x9 grid divided into 9 3x3 blocks:

<img src="./images/Sudoku.svg">


The rule of the game is to fill the grid with numbers 1-9 such that any row, column or block
contains each of the numbers 1-9 exactly once. The difficulty of the game depends on which 
cells have been pre-filled with which numbers. Estimating the difficulty of a sudoku is
a non-trivial task, though if you are given starting configuration that has only one solution then adding legal numbers always
makes it easier. (Removing them might not as multiple solutions might emerge by reducing
restrictions, and if the starting solution has multiple solutions then adding a number might rule out simpler solutions.)

For the system we'll handle data input and output as strings of numbers, i.e. a single
sudoku will be an string of length 81, with each character one of the numbers 0-9. Here
with a 0 we will mean that a cell is unfilled. The numbers in this string are taken to 
be in such an order that they fill the standard 9x9 grid one by one, starting from top left
and moving through the cells left to right, top to bottom.

Internally we'll handle the Sudoku as a 9x9 grid of *possibilities*. By this I mean
that the content of any given sudoku cell will be an array of booleans, where each index
is representing if a given number could be allowed in that cell. We do this instead of
just having a 9x9 grid of numbers 0-9 for two reasons:
- This base architecture makes it much easier to include some more complicated strategies.
- We don't want to make the algorithm and the underlying structure *too* simple. Benchmarking Python vs Numpy vs C with a for loop doesn't sound interesting enough.
Anyway, so the basic structure we'll look at will be something we call a *possibility grid*:
```
boolean p_grid[NUM_ROWS][NUM_COLS][NUM_POSSIBILITIES]
```
though all of the numbers here are actually just 9 and depending on the 
version, instead of booleans we might be using integers or chars.

Anyway, pseudocode for the main solver will look like this:
```python
def recursive_solver(sudoku : PossibilityGrid) -> bool:

    changed = True
    while(changed):
        changed = reduce_possibilities(sudoku) # Clever strategies

    if is_solved(sudoku):
        return True

    # Recursive brute forcing starts here:
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
So here the `reduce_possibilities` is responsible for clever strategies like "for this cell, the only number not yet appearing in its row, col and block is 5, so the only possibility for this cell is 5", where as the latter recursive part will just start brute forcing the solution after the clever stuff has failed. 

### (On) what?

I found a nice open source sudoku source on kaggle: LINK


## Results

The main idea is that I take turns improving my Python solvers and C solvers, with the aim of
alternatively trying to close the gap with the Python versions and then trying to expand the
gap with C versions. The benchmarks were run (at the time of writing) on an Azure VM B2ms (2 vcpus, 8 GiB memory) running Ubuntu 18.04.

### Round 1 - The baseline - Simple Python vs Simple C

I started by building a very straightforward implementation in Python 
(`./src/naive_sudoku_solver.py`).
It's called naive because it doesn't do anything fancy, though it aims to be as pythonic as possible
and not do too much obviously stupid things. On the benchmark machine  it solved
10k sudokus in just under 50 seconds.

To compete the naive Python version, I then made a simple C-version. I call it simple because simple
C is the best I can do, and it probably does some obviously stupid things as well because I don't 
have a good touch to C. But in any case it runs and using the same algorithm it solves the same 10k
sudokus in about 5 seconds - so an order of magnitude improvement right off the bat. 

|              | s/Sudoku | 10k Sudokus |
|--------------|----------|-------------|
| Naive Python | 5.1e-03  | 51s         |
| Naive C      | 5.4e-04  | 5.2s        |
|              |          |             |

So C 1, Python 0 at this point. Let's see how we could start improving the Python version a bit.


### Round 1.5 - OOP solution

Before we start to do anything fancy, I see that we're gonna be building Sudoku solvers that improve
or extend previous versions. Shouldn't we maybe do this in a more Object Oriented Programming way? 
It should surely make this nice in the long run, but doesn't OOP create extra baggage that will slow
everything down? Let's test this!

So in `./src/OOP_sudoku.py` we hate the very same solver as before, but in as a Sudoku Solving Object. We run the results again and what we see is:

|              | s/Sudoku | 10k Sudokus |
|--------------|----------|-------------|
| Naive Python | 5.1e-03  | 51s         |
| Naive C      | 5.4e-04  | 5.2s        |
| OOP Python   | 4.9e-03  | 49s         |

So no, the Object structure doesn't bring any extra baggage, we're even a bit faster than we were with the naive solution. If we find the energy, we'll later on try to understand why we were faster
here. (I wouldn't be surprised if the answer has something to do with "optimizing bytocode interpreter".)

### Round 2 - Improved Naive Python

Let's start small before even trying to bring out the big guns. 


#### Analysis

First of all let's look at where we actually spend time in our current OOP solver by 
running the benchmark for that solver under cProfile:

```python -m cProfile -o OOP_solver.prof benchmark.py```

The results are kinda long, but let's look at the top time spenders based both on *cumtime* which counts even when the given function has called another function
(and waiting for its results) and on *total time* which excludes time in sub-functions. The commands we run look like this:

```
$ python -m pstats OOP_solver.prof 
Welcome to the profile statistics browser.
OOP_solver.prof% strip
OOP_solver.prof% sort cumtime
OOP_solver.prof% stats 30
[...]
OOP_solver.prof% sort tottime
OOP_solver.prof% stats 30
```

And here are the results, first for cumulative time:
```
Mon Mar  6 10:11:01 2023    OOP_solver.prof

         252249901 function calls (252235248 primitive calls) in 114.974 seconds

   Ordered by: cumulative time
   List reduced from 696 to 30 due to restriction <30>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     44/1    0.000    0.000  115.336  115.336 {built-in method builtins.exec}
        1    0.000    0.000  115.336  115.336 benchmark.py:1(<module>)
        1    0.066    0.066  115.315  115.315 benchmark.py:15(run_benchmark)
    10000    0.038    0.000  114.444    0.011 OOP_sudoku.py:4(read_and_solve_sudoku_from_string)
24019/10000  0.170    0.000  112.645    0.011 OOP_sudoku.py:80(recursive_solver)
    84712    9.148    0.000   78.545    0.001 OOP_sudoku.py:171(reduce_possibilities)
  2135653    6.198    0.000   66.217    0.000 OOP_sudoku.py:197(get_simple_mask)
  6406959   21.542    0.000   44.162    0.000 OOP_sudoku.py:54(extract_exclusions)
    84712    1.542    0.000   29.708    0.000 OOP_sudoku.py:137(still_solvable)
  2287224   11.333    0.000   19.849    0.000 OOP_sudoku.py:44(collision_in_collection)
 88109228   17.485    0.000   17.639    0.000 {built-in method builtins.sum}
  2898061    9.392    0.000   11.871    0.000 OOP_sudoku.py:113(block)
 46275920    6.938    0.000    6.938    0.000 {method 'index' of 'list' objects}
 62948777    6.190    0.000    6.190    0.000 {method 'append' of 'list' objects}
  6406959    5.310    0.000    5.310    0.000 OOP_sudoku.py:56(<listcomp>)
  2898061    1.881    0.000    4.605    0.000 OOP_sudoku.py:110(col)
    84712    0.745    0.000    3.981    0.000 {built-in method builtins.all}
  6664729    1.971    0.000    3.238    0.000 OOP_sudoku.py:156(<genexpr>)
  2135653    3.202    0.000    3.202    0.000 OOP_sudoku.py:210(<listcomp>)
  6406959    2.807    0.000    2.807    0.000 OOP_sudoku.py:62(<listcomp>)
    24019    1.178    0.000    2.748    0.000 OOP_sudoku.py:241(__str__)
  2898061    2.724    0.000    2.724    0.000 OOP_sudoku.py:111(<listcomp>)
    14019    0.031    0.000    2.444    0.000 OOP_sudoku.py:231(copy)
  2824460    1.079    0.000    1.987    0.000 OOP_sudoku.py:19(p_array_to_num)
    24019    0.024    0.000    1.425    0.000 OOP_sudoku.py:76(__init__)
    24019    0.732    0.000    1.401    0.000 OOP_sudoku.py:28(convert_sudoku_string_to_p_grid)
    16974    0.292    0.000    0.937    0.000 OOP_sudoku.py:127(first_unsolved_cell_index)
     4295    0.814    0.000    0.814    0.000 OOP_sudoku.py:234(import_p_grid)
    10001    0.018    0.000    0.771    0.000 std.py:1174(__iter__)
      795    0.015    0.000    0.750    0.001 std.py:1212(update)
```
and then for total time:

```
Mon Mar  6 10:11:01 2023    OOP_solver.prof

         252249901 function calls (252235248 primitive calls) in 114.974 seconds

   Ordered by: internal time
   List reduced from 696 to 30 due to restriction <30>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  6406959   21.542    0.000   44.162    0.000 OOP_sudoku.py:54(extract_exclusions)
 88109228   17.485    0.000   17.639    0.000 {built-in method builtins.sum}
  2287224   11.333    0.000   19.849    0.000 OOP_sudoku.py:44(collision_in_collection)
  2898061    9.392    0.000   11.871    0.000 OOP_sudoku.py:113(block)
    84712    9.148    0.000   78.545    0.001 OOP_sudoku.py:171(reduce_possibilities)
 46275920    6.938    0.000    6.938    0.000 {method 'index' of 'list' objects}
  2135653    6.198    0.000   66.217    0.000 OOP_sudoku.py:197(get_simple_mask)
 62948777    6.190    0.000    6.190    0.000 {method 'append' of 'list' objects}
  6406959    5.310    0.000    5.310    0.000 OOP_sudoku.py:56(<listcomp>)
  2135653    3.202    0.000    3.202    0.000 OOP_sudoku.py:210(<listcomp>)
  6406959    2.807    0.000    2.807    0.000 OOP_sudoku.py:62(<listcomp>)
  2898061    2.724    0.000    2.724    0.000 OOP_sudoku.py:111(<listcomp>)
  6664729    1.971    0.000    3.238    0.000 OOP_sudoku.py:156(<genexpr>)
  2898061    1.881    0.000    4.605    0.000 OOP_sudoku.py:110(col)
    84712    1.542    0.000   29.708    0.000 OOP_sudoku.py:137(still_solvable)
    24019    1.178    0.000    2.748    0.000 OOP_sudoku.py:241(__str__)
  2824460    1.079    0.000    1.987    0.000 OOP_sudoku.py:19(p_array_to_num)
     4295    0.814    0.000    0.814    0.000 OOP_sudoku.py:234(import_p_grid)
    84712    0.745    0.000    3.981    0.000 {built-in method builtins.all}
    24019    0.732    0.000    1.401    0.000 OOP_sudoku.py:28(convert_sudoku_string_to_p_grid)
  2898061    0.513    0.000    0.513    0.000 OOP_sudoku.py:107(row)
4577538/4577451    0.494    0.000    0.494    0.000 {built-in method builtins.len}
      799    0.373    0.000    0.373    0.000 {method 'write' of '_io.TextIOWrapper' objects}
    16974    0.292    0.000    0.937    0.000 OOP_sudoku.py:127(first_unsolved_cell_index)
  1945539    0.200    0.000    0.200    0.000 {method 'copy' of 'list' objects}
24019/10000    0.170    0.000  112.645    0.011 OOP_sudoku.py:80(recursive_solver)
   464825    0.110    0.000    0.153    0.000 utils.py:330(<genexpr>)
    24019    0.108    0.000    0.670    0.000 OOP_sudoku.py:31(<listcomp>)
        1    0.066    0.066  115.315  115.315 benchmark.py:15(run_benchmark)
   462434    0.044    0.000    0.044    0.000 {built-in method unicodedata.east_asian_width}
```

For now I think the best place to focus on is the top of the total time, in particular these lines:
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  6406959   21.542    0.000   44.162    0.000 OOP_sudoku.py:54(extract_exclusions)
 88109228   17.485    0.000   17.639    0.000 {built-in method builtins.sum}
  2287224   11.333    0.000   19.849    0.000 OOP_sudoku.py:44(collision_in_collection)
  2898061    9.392    0.000   11.871    0.000 OOP_sudoku.py:113(block)
    84712    9.148    0.000   78.545    0.001 OOP_sudoku.py:171(reduce_possibilities)
 46275920    6.938    0.000    6.938    0.000 {method 'index' of 'list' objects}
  2135653    6.198    0.000   66.217    0.000 OOP_sudoku.py:197(get_simple_mask)
 62948777    6.190    0.000    6.190    0.000 {method 'append' of 'list' objects}
 ```

So here we see that the biggest time consumers consist of a few built-in methods -
`sum`, `list.index` and `append` - together with a few methods we've built, namely
`extract_exclusions`, `collisions_in_collection`, `block`, `reduce_possibilities` and `get_simple_mask`.

Looking at how these transgressors interact, we note that the appending to list only happens
in the methods `collisions_in_collection`, `block`, `reduce_possibilities` and the magic
method `__str__` which is used in the copying of a sudoku. 
The built-in `sum` method is also used only in methods listed above, together with another
static method called `p_array_to_num` which has also found its way to the top 30 of both lists.

So looking how these different subparts consume our CPU time, we note that there is actually a lot to improve. For example, looking at our `extract_exclusions` method which holds top rank in both total and cumulative times, we see that we are using the `sum` only to detect if a given 
possibility array is already completely determined. And in fact, most of the uses of `sum`
are only used to figure out if a given probability array has only a single '1' in it. This seeems
like an overkill.

So instead of sums, let's do a faster lookup. There are only 9 possibilities for 
an array of length 9 to have only one '1', so let's enumerate them and turn the check into
a dictionary lookup. To do this, though, we need something hashable, so we need to turn from 
lists to tuples. Let's go one step further: we'll change the whole Sudoku data format from 3-dimensional list to a 2-dimensional list of tuples!

So what we changed going from `OOP_sudoku.py` to `OOP_sudoku_improved.py` was:
1. Turned the whole "from possibility array to number and back" thing to rely on 
dictionary lookups of pre-stored tuples.
2. Changed the internal sudoku format to have all the possibility arrays to be tuples
instead of lists.
3. Reduced for loops by adding more early returns, plus other minor improvements.

And here are the results:

|              | s/Sudoku | 10k Sudokus |
|--------------|----------|-------------|
| Naive Python | 5.1e-03  | 51s         |
| Naive C      | 5.4e-04  | 5.2s        |
| OOP Python   | 4.9e-03  | 49s         |
| Improved OOP Python | 4.7e-03 | 47s |

So with all that work we shaved about four percents off our running time. cProfiler tells that for the total time the biggest time users are now:
```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
  6406959   20.422    0.000   33.407    0.000 OOP_sudoku_improved.py:47(extract_exclusions)
 81526820   16.343    0.000   16.343    0.000 OOP_sudoku_improved.py:35(p_array_to_num)
  2287224    9.319    0.000   15.190    0.000 OOP_sudoku_improved.py:73(collision_in_collection)
    84712    9.137    0.000   65.780    0.001 OOP_sudoku_improved.py:179(reduce_possibilities)
  2898061    8.713    0.000   10.813    0.000 OOP_sudoku_improved.py:124(block)
  2135653    5.703    0.000   53.776    0.000 OOP_sudoku_improved.py:205(get_simple_mask)
 62948777    5.046    0.000    5.046    0.000 {method 'append' of 'list' objects}
  2135653    3.099    0.000    3.099    0.000 OOP_sudoku_improved.py:218(<listcomp>)
  6406959    2.731    0.000    2.731    0.000 OOP_sudoku_improved.py:49(<listcomp>)
  2898061    2.562    0.000    2.562    0.000 OOP_sudoku_improved.py:122(<listcomp>)
  2898061    1.776    0.000    4.338    0.000 OOP_sudoku_improved.py:121(col)
```

So one of the big differences is that we pushed the 17 or so seconds used by `sum` to the
`p_array_to_num` function here.


### Round 3 - Numpy

So, Sudoku is pretty much a glorified matrix, and numpy is good with matrices.
This should be a no-brainer.

