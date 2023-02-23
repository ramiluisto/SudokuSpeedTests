#include <stdio.h>

// More descriptive dimension names.
#define SUDO_X 9
#define SUDO_Y 9
#define P_RANGE 9
#define SUDOKU_LIST_LENGTH SUDO_X*SUDO_Y

// The following are used for pretty printing sudokus.
#define TOP_ROW_FORMAT "╔═══════╤═══════╤═══════╗\n"
#define MID_ROW_FORMAT "╟───────┼───────┼───────╢\n"
#define BOT_ROW_FORMAT "╚═══════╧═══════╧═══════╝\n"
#define ROW_FORMAT "║ %c %c %c │ %c %c %c │ %c %c %c ║\n"


/*This p_grid type defines the standard format
that we'll use to handle sudokus. For each cell in the sudoku, we have 
an array of 9 numbers of either 0 or 1. These should be thought
as booleans that represent if a given number 1-9 is a possible value
for that cell.*/
typedef char p_grid[SUDO_X][SUDO_Y][P_RANGE];

/*The sub_component type will always point to a length 9 array of pointers. 
each such array represents either a row, column or a block. The pointers point
to the corresponding cells in the main p_grid type sudoku array.*/
typedef char** sub_component; 


void convert_sudoku_string_to_p_grid(char *raw, p_grid sudoku){
    /*This function is essentially defining the standard format
    that we'll use to handle sudokus. For each cell in the sudoku, we have 
    an array of numbers 0 or 1.*/

    for(int i = 0 ; *raw != '\0' ; raw++){
        for(int j=0; j<P_RANGE; j++) sudoku[i/9][i%9][j] = 0; // Initialize so that nothing is possible.
        if (*raw != '0') sudoku[i/9][i%9][*raw - '0' -1] = 1; // Non-empty cells have just one possibility.
        else for(int j=0; j<9; j++) sudoku[i/9][i%9][j] = 1;  // For empty cells everything is possible.
        i++;
    }
}

sub_component get_row(char row_idx, p_grid sudoku) {
    static char* row[9];
    for(int i=0; i<9; i++) row[i] = sudoku[row_idx][i];
    return row;
}

sub_component get_col(char col_idx, p_grid sudoku) {
    static char* col[9];
    for(int i=0; i<9; i++) col[i] = sudoku[i][col_idx];
    return col;
}

sub_component get_block(char total_idx, p_grid sudoku) {
    static char* block[9];
    int B_row, B_col, topleft, block_index;

    B_row = total_idx/27;        
    B_col = (total_idx/3)%3;      
    topleft = 27*B_row + 3*B_col; // The cell index of the cell in the top left corner of the block.
    static char shift_array[] = { 0, 1, 2, 9, 10, 11, 18, 19, 20 };
    // Indeces of the block will be "topleft + shift_array".
    
    for(int i=0; i<9; i++){
        block_index = topleft+shift_array[i];
        block[i] = sudoku[block_index/9][block_index%9];
    }


    return block;
}

char p_array_interpreter(char p_array[9]) {
    int num_idx=0, sum=0;
    char value;
    for(int p_idx=0; p_idx < P_RANGE; p_idx++) {
        value = p_array[p_idx];
        sum += value;
        num_idx = (value==0) ? num_idx : p_idx;

    }
    num_idx = (sum == 1) ? num_idx+1 : 0;

    return num_idx;
}

int check_collisions(sub_component sub) {
    char hits[9] = {0};

    for(int idx=0; idx<9; idx++) {

        //sub[idx]
    }


    for(int i=0; i<9; i++) if (hits[i] > 1) return 0;

    return 1;
}

int still_solvable(p_grid sudoku) {

    // Check rows for collisions.
    for(int row_idx=0; row_idx<SUDO_Y; row_idx++){
        sub_component row = get_row(row_idx, sudoku);

    }

    // Check if any cell has no possibilities left.
    for(int idx=0; idx<SUDOKU_LIST_LENGTH; idx++) {
        int sum = 0;
        for(int i=0; i<P_RANGE; i++) sum += sudoku[i/9][i%9][i];
        if (sum == 0) return 0;
    }


    return 0;
}

int reduce_possibilities(p_grid sudoku) {
    return 0;
}

char first_unsolved_cell_index(p_grid sudoku) {

}

void get_cell_possibilities(char cell_index, p_grid sudoku, char possibilities[P_RANGE]) {

}

void copy_first_sudoku_contents_to_second(p_grid sudoku_in, p_grid sudoku_out) {

}

void set_cell_of_sudoku(char cell_index, p_grid sudoku, char new_value) {

}


int recursive_solver(p_grid sudoku){
    // This is the main recursive loop.
    do
    {
        if (! still_solvable(sudoku)) return 0;
    } while (reduce_possibilities(sudoku));

    char cell_idx = first_unsolved_cell_index(sudoku);
    if (cell_idx == -1) return 1;

    char possibilities[P_RANGE];
    get_cell_possibilities(cell_idx, sudoku, possibilities);
    for(int index = 0; index < P_RANGE; index++) {
        char fixed_number = possibilities[index];
        if (!fixed_number) continue;

        char local_sudoku[SUDO_X][SUDO_Y][P_RANGE] = {0};
        copy_first_sudoku_contents_to_second(sudoku, local_sudoku);
        set_cell_of_sudoku(cell_idx, local_sudoku, fixed_number);
        int result = recursive_solver(local_sudoku);
        if (result) {
            copy_first_sudoku_contents_to_second(local_sudoku, sudoku);
            return 1;
        }
    }

    return 0;

}



//////////////////////////////////
// Printers etc
/////////////////////////////////


void print_sudoku(p_grid sudoku) {
    char sns[SUDOKU_LIST_LENGTH] = {0};

    for(int i=0; i<SUDOKU_LIST_LENGTH; i++) {
        int num_index =  p_array_interpreter(sudoku[i/9][i%9]);
        sns[i] = (num_index>0) ? '0'+num_index : '_';
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


void p_array_pretty_print(sub_component sub){
    for(int i=0; i<9; i++){
        int index =  p_array_interpreter(sub[i]);
        printf("%d ", index);

    }
    printf("\n");
}

void run_tests() {

    char TEST_SUDOKU_STRING[] = "765082090913004080840030150209000546084369200006405000000040009090051024001890765";
    char NULL_SUDOKU_STRING[] = "000000000000000000000000000000000000000000000000000000000000000000000000000000000";
    p_grid sudoku = {0};

    printf("%s\n", TEST_SUDOKU_STRING);
    convert_sudoku_string_to_p_grid(TEST_SUDOKU_STRING, sudoku);
    print_sudoku(sudoku);

    //printf("%s\n", TEST_SUDOKU_STRING);
    //convert_sudoku_string_to_p_grid(NULL_SUDOKU_STRING, sudoku);
    //print_sudoku(sudoku);

    printf("Row 4 contents:");
    sub_component test_row = get_row(4, sudoku);
    p_array_pretty_print(test_row);
    for(int i=0; i<9; i++){
        printf("%d| ", i+1);
        for(int j=0; j<9; j++) printf("%d ", test_row[i][j]);
        printf("\n");
    }
    printf("\n");

    printf("Col 5 contents:");
    sub_component test_col = get_col(5, sudoku);
    p_array_pretty_print(test_col);
    for(int i=0; i<9; i++){
        printf("%d| ", i+1);
        for(int j=0; j<9; j++) printf("%d ", test_col[i][j]);
        printf("\n");
    }
    printf("\n");

    printf("Block 8 contents:");
    sub_component test_block = get_block(80, sudoku);
    p_array_pretty_print(test_block);
    for(int i=0; i<9; i++){
        printf("%d| ", i+1);
        for(int j=0; j<9; j++) printf("%d ", test_block[i][j]);
        printf("\n");
    }
    printf("\n");
}

int main() {
    run_tests();

}