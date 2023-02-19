#include <stdio.h>
#define SUDOKU_LIST_SIZE 81
#define SUDOKU_NUM_COUNT 9


char TEST_SUDOKU_STRING[] = "765082090913004080840030150209000546084369200006405000000040009090051024001890765";
char sudoku_possibility_array[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT] = {0};


int print_sudoku_string(char []);

void convert_sudoku_string_to_p_array(char *, char[SUDOKU_LIST_SIZE][SUDOKU_NUM_COUNT]);

int main() {
    printf("Sudoku starting\n");
    print_sudoku_string(TEST_SUDOKU_STRING);



    convert_sudoku_string_to_p_array(TEST_SUDOKU_STRING, sudoku_possibility_array);

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


        printf("%d|", *raw - '0');
        for(int j=0; j<9; j++){
            printf("%d ", p_grid[i][j]);
        }
        printf("\n");
        i++;
    }
    printf("\n");

    return;
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