import src.utils as utils


class Sudoku:
    block_shifts = (*range(3), *range(9, 12), *range(18, 21))

    ################################
    # Static methods
    ################################

    @staticmethod
    def p_array_to_num(p_array) -> int:
        if sum(p_array) == 1:
            num = 1 + p_array.index(1)
        else:
            num = 0

        return num

    @staticmethod
    def convert_sudoku_string_to_p_grid(input_sudoku: str):
        base_p = 9 * [1]
        p_grid = [[base_p.copy() for _ in range(9)] for j in range(9)]

        for idx, char in enumerate(input_sudoku):
            row = idx // 9
            col = idx % 9
            value = int(char)

            if value != 0:
                p_grid[row][col] = 9 * [0]
                p_grid[row][col][value - 1] = 1

        return p_grid

    @staticmethod
    def convert_p_grid_to_sudoku_string(sudoku) -> str:
        sudoku_list = []

        for idx in range(81):
            row_idx = idx // 9
            col_idx = idx % 9
            num = p_array_to_num(sudoku[row_idx][col_idx])
            sudoku_list.append(str(num))

        sudoku_str = "".join(sudoku_list)

        return sudoku_str
    
    @staticmethod
    def collision_in_collection(collection):
        numbers_in_collection = []
        for possibilities in collection:
            if sum(possibilities) == 1:
                num = 1 + possibilities.index(1)
                numbers_in_collection.append(num)

        return len(set(numbers_in_collection)) < len(numbers_in_collection)


    ################################
    # Object level stuff
    ################################


    def __init__(self, sudoku_string):
        self.sudoku = self.convert_sudoku_string_to_p_grid(sudoku_string)

    ################################
    # Accessors and whatnot
    ################################

    def row(self, row_idx):
        return self.sudoku[row_idx]

    def col(self, col_idx):
        return [self.sudoku[j][col_idx] for j in range(9)]

    def block(self, cell_idx):
        blo_row = cell_idx // 27
        blo_col = (cell_idx // 3) % 3
        top_left = 27 * blo_row + 3 * blo_col

        block = []
        for shift in self.block_shifts:
            internal_idx = top_left + shift
            row = internal_idx // 9
            col = internal_idx % 9
            block.append(self.sudoku[row][col])

        return block
    


    @property
    def first_unsolved_cell_index(self):
        for idx in range(81):
            row_idx = idx // 9
            col_idx = idx % 9
            if self.p_array_to_num(self.sudoku[row_idx][col_idx]) == 0:
                return idx

        return -1   
         
    @property
    def still_solvable(self):
        for j in range(9):
            row = self.row(j)
            collision = self.collision_in_collection(row)
            if collision:
                return False

            col = self.col(j)
            collision = self.collision_in_collection(col)
            if collision:
                return False

        for j in [0, 3, 6, 27, 30, 33, 54, 57, 60]:
            blo = self.block(j)
            collision = self.collision_in_collection(blo)
            if collision:
                return False

        return all(sum(self.sudoku[i // 9][i % 9]) >= 1 for i in range(81))


    ################################
    # Special magic methods
    ################################

    def __str__(self) -> str:
        sudoku_list = []

        for idx in range(81):
            row_idx = idx // 9
            col_idx = idx % 9
            num = self.p_array_to_num(self.sudoku[row_idx][col_idx])
            sudoku_list.append(str(num))

        sudoku_str = "".join(sudoku_list)

        return sudoku_str
