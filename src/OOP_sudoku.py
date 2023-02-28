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
    
    @staticmethod
    def extract_exclusions(exclusion_idx, possibilities):
        non_current = [
            possibility
            for idx, possibility in enumerate(possibilities)
            if idx != exclusion_idx
        ]

        exclusion_mask = [0 for _ in range(9)]
        for possibility in non_current:
            if sum(possibility) != 1:
                continue
            else:
                idx = possibility.index(1)
                exclusion_mask[idx] = 1

        return exclusion_mask

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

    # More complex methods

    def reduce_possibilities(self) -> bool:
        changes = False

        for idx in range(81):
            row_idx = idx // 9
            col_idx = idx % 9

            if sum(self.sudoku[row_idx][col_idx]) == 1:
                continue

            exclusion_mask = self.get_simple_mask(row_idx, col_idx)
            new_possibilities = []
            for current, mask in zip(self.sudoku[row_idx][col_idx], exclusion_mask):
                if current and not mask:
                    new_value = 1
                else:
                    new_value = 0

                if current != new_value:
                    changes = True
                new_possibilities.append(new_value)

            self.sudoku[row_idx][col_idx] = new_possibilities

        return changes
    
    def get_simple_mask(self, row_idx, col_idx):
        row = self.row(row_idx)
        col = self.col(col_idx)
        blo = self.block(9 * row_idx + col_idx)

        # Note that here e.g. the within the row_mask the index of the current cell is given
        # by col_idx, and vice versa.
        row_mask = self.extract_exclusions(col_idx, row)
        col_mask = self.extract_exclusions(row_idx, col)

        block_idx = 3 * (row_idx % 3) + (col_idx % 3)
        block_mask = self.extract_exclusions(block_idx, blo)

        total_mask = [
            int(rb or cb or bb) for rb, cb, bb in zip(row_mask, col_mask, block_mask)
        ]

        return total_mask




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
