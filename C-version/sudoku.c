#include <stdio.h>
#define SUDOKU_LIST_SIZE 81
#define SUDOKU_NUM_COUNT 9



char TEST_SUDOKU_STRING[] = "765082090913004080840030150209000546084369200006405000000040009090051024001890765";
char sudoku_possibility_array[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT] = {0};


int print_sudoku_string(char []);
int print_p_grid(char[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT]);

void convert_sudoku_string_to_p_array(char *, char[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT]);

int get_row_by_index(int, char[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT], char[SUDOKU_NUM_COUNT][SUDOKU_NUM_COUNT]);
int get_col_by_index(int, char[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT], char[SUDOKU_NUM_COUNT][SUDOKU_NUM_COUNT]);
int get_block_by_index(int, char[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT], char[SUDOKU_NUM_COUNT][SUDOKU_NUM_COUNT]);


int main() {
    printf("Sudoku starting\n");
    print_sudoku_string(TEST_SUDOKU_STRING);

    convert_sudoku_string_to_p_array(TEST_SUDOKU_STRING, sudoku_possibility_array);
    print_p_grid(sudoku_possibility_array);

    char test_row[SUDOKU_NUM_COUNT][SUDOKU_NUM_COUNT] = {0};

    get_block_by_index(16, sudoku_possibility_array, test_row);

    /*
    printf("\n");
    for(int i=0; i<9; i++) {
        for(int j=0; j<9; j++){
            printf("%d ", test_row[i][j]);
        }
        printf("\n");
       
    }*/
}

void convert_sudoku_string_to_p_array(char *raw, char p_grid[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT]){

    for(int i = 0 ; *raw != '\0' ; raw++){
        if (*raw != '0') {
            p_grid[i][*raw - '0' -1] = 1;
        }
        else {
            for(int j=0; j<9; j++) {
                p_grid[i][j] = 1;
            }
        }
        i++;
    }
}

int print_p_grid(char p_grid[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT]) {

    for(int square=0; square < SUDOKU_LIST_SIZE; square++) {
        int index=0, sum=0;
        for(int i=0; i < SUDOKU_NUM_COUNT; i++) {
            if (p_grid[square][i] == 1) {
                index = i+1;
                sum++;
            }
        }
        if (sum > 1) {
            index = 0;
        }

        printf("%d | ", index);
        for(int i=0; i < SUDOKU_NUM_COUNT; i++) {
            printf("%d ", p_grid[square][i]);
        }
        printf("\n");
    }

}

int print_sudoku_string(char sudoku[]) {

    for(int i = 0; i < SUDOKU_LIST_SIZE; i++) {
        if (i%9 == 0) {
            printf("\n");
            if ((i%27 == 0) && (i > 0))  printf("\n");
        }
        if (i%3 == 0) printf(" ");
        
        printf("%c ", sudoku[i]);
    }

    printf("\n\n");
}

int get_row_by_index(int index, char p_grid[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT], char row[SUDOKU_NUM_COUNT][SUDOKU_NUM_COUNT]) {
    int row_index;

    for(int i=0; i<9; i++){
        row_index = (index/9)*9 + i;
        for(int j=0; j < 9; j++) {
            row[i][j] = p_grid[row_index][j];
        }
    }
    return index/9;
}

int get_col_by_index(int index, char p_grid[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT], char col[SUDOKU_NUM_COUNT][SUDOKU_NUM_COUNT]) {
    int col_index;

    for(int i=0; i<9; i++){
        col_index = (index % 9)+ 9*i; 


        for(int j=0; j < 9; j++) {
            col[i][j] = p_grid[col_index][j];
        }
    }
    return index%9;
}

int get_block_by_index(int index, char p_grid[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT], char block[SUDOKU_NUM_COUNT][SUDOKU_NUM_COUNT]) {

    int block_index;
    int B_row, B_col, topleft;

    B_col = (index/3)%3;
    B_row = index/27;
    topleft = 27*B_row + 3*B_col;

    printf("We have B_col: %d, B_row: %d and topleft: %d", B_col, B_row, topleft);

    char shift_array[] = {0, 1, 2, 9, 10, 11, 18, 19, 20};

    for(int i=0; i<9; i++){
        block_index = topleft + shift_array[i];
        for(int j=0; j < 9; j++) {
            block[i][j] = p_grid[block_index][j];
        }
    }
    return 3*B_col + B_row;
}

void mask_p_grid_by_data(
    char current_index,
    char p[], 
    char row[SUDOKU_NUM_COUNT][SUDOKU_NUM_COUNT], 
    char col[SUDOKU_NUM_COUNT][SUDOKU_NUM_COUNT], 
    char block[SUDOKU_NUM_COUNT][SUDOKU_NUM_COUNT]){

    for(int i=0; i<9; i++){

        int col_idx, row_idx, block_idx;
        col_idx = row_idx = block_idx = -2;

        for(int j=0; j<9; j++){
            if (j == current_index) continue;

            if (row[i][j] == 1) row_idx = (row_idx == -2) ? j : -1; // put if inside the ternary?
            if (col[i][j] == 1) col_idx = (col_idx == -2) ? j : -1;
            if (block[i][j] == 1) block_idx = (block_idx == -2) ? j : -1;  
        }

        char mask_indeces[] = {row_idx, col_idx, block_idx};
        for(int k=0; k<3; k++) {
            if (mask_indeces[k] >= 0) {
                p[i] = 0;
            }
        }


    }

        return;
    }