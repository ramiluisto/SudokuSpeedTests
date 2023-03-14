from distutils.core import setup, Extension


def main():
    setup(
        name="RamiSudoku",
        version="1.0.0",
        description="Rami's Python interface to RamiSudoku.",
        author="Rami Luisto",
        author_email="rami.luisto@gmail.com",
        ext_modules=[Extension("RamiSudoku", ["sudoku_solver_module.c"])],
    )


if __name__ == "__main__":
    main()
