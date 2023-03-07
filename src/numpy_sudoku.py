import numpy as np
import src.utils as utils


def read_and_solve_sudoku_from_string(sudoku_string):
    sudoku = Sudoku(sudoku_string)
    success = sudoku.recursive_solver()
    result_string = str(sudoku)

    return result_string


class Sudoku:
    block_shifts = (*range(3), *range(9, 12), *range(18, 21))

    ################################
    # Static methods
    ################################

    @staticmethod
    def p_array_to_num(p_array: np.array) -> int:
        if p_array.sum() == 1:
            return 1 + np.where(p_array == 1)[0][0]
        else:
            return 0
        
    @staticmethod
    def num_to_p_array(num: int) -> np.array:
        if num == 0:
            p_array = np.ones(9, dtype=np.int8)
        else:
            p_array = np.zeros(9, dtype=np.int8)
            p_array[num - 1] = 1

        return p_array        

    @classmethod
    def convert_sudoku_string_to_p_grid(cls, sudoku_string: str) -> np.array:
        separated_string = " ".join(list(sudoku_string))
        num_sudoku = np.fromstring(separated_string, dtype=np.int8, sep=" ")
        sudoku = np.zeros((9, 9, 9), dtype=np.int8)
        for idx, num in enumerate(num_sudoku):
            sudoku[idx // 9][idx % 9] = cls.num_to_p_array(num)

        return sudoku

    @classmethod
    def collision_in_collection(cls, collection : np.array) -> bool:
        collisions = cls.get_fixed_projection_array(collection)

        return np.any(collisions > 1)

    @classmethod
    def extract_exclusions(cls, exclusion_idx, possibilities):
        collection = np.delete(possibilities, [exclusion_idx], axis = 0)
        exclusion_mask = cls.get_fixed_projection_array(collection)

        return exclusion_mask

    @staticmethod
    def get_fixed_projection_array(collection : np.array) -> np.array:
        summed_collection = np.sum(collection, axis = -1)
        fixed_elts = np.where(summed_collection == 1)[0]
        fixed_p_arrays = np.take(collection, fixed_elts, axis = 0)
        projection_array = np.sum(fixed_p_arrays, axis = 0)

        return projection_array

    ################################
    # Object level stuff
    ################################

    def __init__(self, sudoku_string):
        self.sudoku = self.convert_sudoku_string_to_p_grid(sudoku_string)

    # The main recurser
    def recursive_solver(self) -> bool:
        changed = True
        while changed:
            changed = self.reduce_possibilities()
            if not self.still_solvable:
                return False

        cell_idx = self.first_unsolved_cell_index
        if cell_idx == -1:
            # If there is no unsolved cell, then the sudoku is complete.
            return True

        possibilities = self.get_cell_possibilities(cell_idx)
        for fixed_number in possibilities:
            local_sudoku = self.copy()
            local_sudoku.set_cell_of_sudoku(cell_idx, fixed_number)
            result = local_sudoku.recursive_solver()
            if result:
                self.import_p_grid(local_sudoku)
                return True

        return False

    ################################
    # Accessors and whatnot
    ################################

    def row(self, row_idx):
        return self.sudoku[row_idx, :, :]

    def col(self, col_idx):
        return self.sudoku[:, col_idx, :]

    def block(self, cell_idx):
        b_row = 3 * (cell_idx // 27)
        b_col = 3 * ((cell_idx // 3) % 3)
        block_selection_x = np.array([*3 * [b_row], *3 * [b_row + 1], *3 * [b_row + 2]])
        block_selection_y = np.array(3 * [b_col, b_col + 1, b_col + 2])
        return self.sudoku[block_selection_x, block_selection_y, :]

    @property
    def first_unsolved_cell_index(self):
        y, x = np.where( np.sum(self.sudoku, axis=2) > 1 )
        if len(x) == 0:
            return -1
        return 9*y[0] + x[0]

    @property
    def still_solvable(self):
        # Should these be made non-for-loopy?
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

        return np.all( np.sum(self.sudoku, axis=2) >= 1 )

    def set_cell_of_sudoku(self, cell_idx, fixed_number):
        row_idx = cell_idx // 9
        col_idx = cell_idx % 9

        new_possibilities = np.zeros(9)
        new_possibilities[fixed_number - 1] = 1

        self.sudoku[row_idx][col_idx] = new_possibilities

    ################################
    # More complex methods
    ################################

    def reduce_possibilities(self) -> bool:
        changes = False

        for idx in range(81):
            row_idx = idx // 9
            col_idx = idx % 9

            if self.p_array_to_num(self.sudoku[row_idx][col_idx]) != 0:
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

            self.sudoku[row_idx][col_idx] = tuple(new_possibilities)

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

    def get_cell_possibilities(self, cell_idx):
        row_idx = cell_idx // 9
        col_idx = cell_idx % 9

        possibility_mask = self.sudoku[row_idx][col_idx]
        possibilities = [
            idx + 1 for idx, value in enumerate(possibility_mask) if value == 1
        ]

        return possibilities

    ################################
    # Special methods
    ################################

    def copy(self):  # Copies the Sudoku OBJECT
        return Sudoku(str(self))

    def import_p_grid(self, source_sudoku_object):
        for cell_idx in range(81):
            for p_idx in range(9):
                self.sudoku[cell_idx // 9][cell_idx % 9][
                    p_idx
                ] = source_sudoku_object.sudoku[cell_idx // 9][cell_idx % 9][p_idx]

    def __str__(self) -> str:
        sudoku_list = []

        for idx in range(81):
            row_idx = idx // 9
            col_idx = idx % 9
            num = self.p_array_to_num(self.sudoku[row_idx][col_idx])
            sudoku_list.append(str(num))

        sudoku_str = "".join(sudoku_list)

        return sudoku_str
