#include <stdio.h>

#define SUDO_X 9
#define SUDO_Y 9
#define P_RANGE 9
#define SUDOKU_LIST_LENGTH SUDO_X*SUDO_Y

#define TOP_ROW_FORMAT "╔═══════╤═══════╤═══════╗\n"
#define MID_ROW_FORMAT "╟───────┼───────┼───────╢\n"
#define BOT_ROW_FORMAT "╚═══════╧═══════╧═══════╝\n"
#define ROW_FORMAT "║ %c %c %c │ %c %c %c │ %c %c %c ║\n"

char TEST_SUDOKU_STRING[] = "765082090913004080840030150209000546084369200006405000000040009090051024001890765";




void convert_sudoku_string_to_p_array(char *raw, char sudoku[SUDO_X][SUDO_Y][P_RANGE]){
    /*This function is essentially defining the standard format
    that we'll use to handle sudokus. For each cell in the sudoku, we have 
    an array of numbers 0 or 1.*/
    for(int i = 0 ; *raw != '\0' ; raw++){
        if (*raw != '0') {
            sudoku[i/9][i%9][*raw - '0' -1] = 1;
        }
        else {
            for(int j=0; j<9; j++) {
                sudoku[i/9][i%9][j] = 1;
            }
        }
        i++;
    }
}

/*
bool recursive_solver(char sudoku[SUDO_X][SUDO_Y][P_RANGE]){
    // This is the main recursive loop.
    do
    {
        if (! still_solvable(sudoku)) return False;
    } while (reduce_possibilities(sudoku));

    int cell_idx = first_unsolved_cell_index(sudoku);
    if (cell_idx == -1) return True;

    char possibilities[P_RANGE] = get_cell_possibilities(cell_idx, sudoku);
    for(int index = 0; index < P_RANGE; index++) {
        char fixed_number = possibilities[index];
        if (!fixed_number) continue;

        char local_sudoku[SUDO_X][SUDO_Y][P_RANGE] = {0};
        copy_first_sudoku_contents_to_second(sudoku, local_sudoku);
        set_cell_of_sudoku(cell_idx, local_sudoku, fixed_number);
        result = recursive_solver(local_sudoku);
        if result {
            copy_first_sudoku_contents_to_second(local_sudoku, sudoku);
            return True
        }
    }

    return False

}*/


void print_sudoku(char sudoku[SUDO_X][SUDO_Y][P_RANGE]) {
    char sns[SUDOKU_LIST_LENGTH] = {0};

    for(int i=0; i<SUDOKU_LIST_LENGTH; i++) {
        char p_sum = 0;
        char p_index = 0;

        char value;
        for(char p_idx=0; p_idx<P_RANGE; p_idx++){
            value = sudoku[i/9][i%9][p_idx];
            p_sum += value;
            p_index = (value == 0) ? p_index : p_idx;
        }

        sns[i] = (p_sum==1) ? '1'+p_index : '_';
    }


    printf(TOP_ROW_FORMAT);
    for(int j = 0; j < 3; j++) {
        int i = 9*j;
        printf(ROW_FORMAT, sns[i+0], sns[i+1], sns[i+2], sns[i+3], sns[i+4], sns[i+5], sns[i+6], sns[i+7], sns[i+8] );
    }
    printf(MID_ROW_FORMAT);
    for(int j = 3; j < 6; j++) {
        int i = 9*j;
        printf(ROW_FORMAT, sns[i+0], sns[i+1], sns[i+2], sns[i+3], sns[i+4], sns[i+5], sns[i+6], sns[i+7], sns[i+8] );
    }
    printf(MID_ROW_FORMAT);
    for(int j = 6; j < 9; j++) {
        int i = 9*j;
        printf(ROW_FORMAT, sns[i+0], sns[i+1], sns[i+2], sns[i+3], sns[i+4], sns[i+5], sns[i+6], sns[i+7], sns[i+8] );
    }
    printf(BOT_ROW_FORMAT);

}

int main() {
    printf("%s\n", TEST_SUDOKU_STRING);
    char sudoku[SUDO_X][SUDO_Y][P_RANGE] = {0};
    convert_sudoku_string_to_p_array(TEST_SUDOKU_STRING, sudoku);
    print_sudoku(sudoku);

}