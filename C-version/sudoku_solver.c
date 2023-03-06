#include <stdio.h>
#include <stdbool.h> 
#include <stdlib.h>
#include <string.h>

// CLI parameter stuff
#define MAX_FILEPATH_LENGTH 511

// More descriptive dimension names.
#define SUDO_X 9
#define SUDO_Y 9
#define P_RANGE 9
#define SUDOKU_LIST_LENGTH SUDO_X*SUDO_Y
#define SUDOKU_STR_LENGTH 81

// The following are used for pretty printing sudokus.
#define TOP_ROW_FORMAT "╔═══════╤═══════╤═══════╗\n"
#define MID_ROW_FORMAT "╟───────┼───────┼───────╢\n"
#define BOT_ROW_FORMAT "╚═══════╧═══════╧═══════╝\n"
#define ROW_FORMAT "║ %c %c %c │ %c %c %c │ %c %c %c ║\n"


/* The following p_grid ('possibility grid') type defines the standard format
 * that we'll use to handle sudokus. For each cell in the 9x9 sudoku, we have 
 * a boolean array of length 9. We call this array the p_array
 * ('possibility array') and it represents which of the numbers 1-9
 * are still possible for the given cell. E.g. if for a sudoku of type
 * p_grid we have that on the cell at (2,4) only the numbers 1, 3 or 9 
 * are possible, then 
 * sudoku[2][4] = {1, 0, 1, 0, 0, 0, 0, 0, 1}.
 * Note that with standard indexing, number n corresponds to index position
 * n-1.
 */
typedef char p_grid[SUDO_X][SUDO_Y][P_RANGE];

/*The sub_component type will always point to a length 9 array of pointers. 
each such array represents either a row, column or a block. The pointers point
to the corresponding cells in the main p_grid type sudoku array.*/
typedef char** sub_component; 

typedef char sudoku_string[SUDOKU_STR_LENGTH];

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

    // The cell index of the cell in the top left corner of the block.
    topleft = 27*B_row + 3*B_col;
    // Indeces of the block will be "topleft + shift_array".
    static char block_shift_array[] = { 0, 1, 2, 9, 10, 11, 18, 19, 20 };
    
    for(int i=0; i<9; i++){
        block_index = topleft+block_shift_array[i];
        block[i] = sudoku[block_index/9][block_index%9];
    }


    return block;
}

char p_array_interpreter(char p_array[9]) {
    /* This function will take in a p_array and return
    either the unique possible number 1-9 that it can be or
    0 if there are more or less than 1 possibilities.*/
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



bool check_collisions(sub_component sub) {
    char hits[10] = {0};

    for(int idx=0; idx<9; idx++) {
        char cell_number = p_array_interpreter(sub[idx]);
        hits[cell_number] += 1;
    }

    for(int i=1; i<10; i++) if (hits[i] > 1) return true;

    return false;
}

bool still_solvable(p_grid sudoku) {
    static char top_left_indeces_of_blocks[9] = {0, 3, 6, 27, 30, 33, 54, 57, 60};

    // Check rows for collisions.
    for(int row_idx=0; row_idx<SUDO_Y; row_idx++){
        sub_component row = get_row(row_idx, sudoku);
        if (check_collisions(row)) return false;
    }

    // Check cols for collisions.
    for(int col_idx=0; col_idx<SUDO_X; col_idx++){
        sub_component row = get_col(col_idx, sudoku);
        if (check_collisions(row)) return false;
    }

    // Check blocks for collisions.
    for(int idx=0; idx<9; idx++){
        char block_idx = top_left_indeces_of_blocks[idx];
        sub_component block = get_block(block_idx, sudoku);
        if (check_collisions(block)) return false;
    }

    // Check if any cell has no possibilities left.
    for(int idx=0; idx<SUDOKU_LIST_LENGTH; idx++) {
        int sum = 0;
        for(int i=0; i<P_RANGE; i++) sum += sudoku[idx/9][idx%9][i];
        if (sum == 0) return false;
    }

    return true;
}

void get_single_exclusion_data(char exclusion_counts[9], char ignore_idx, sub_component sub){
    for(int i=0; i<P_RANGE; i++) {
        if (i == ignore_idx) continue;
        char value = p_array_interpreter(sub[i]);
        if (value != 0) exclusion_counts[value-1] += 1;
    }
}

void get_total_exclusions(char values_to_exclude[9], char cell_idx, p_grid sudoku){
    char exclusion_counts[9] = {0};
    //printf("Getting total exclusions for cell_idx %2d.\n", cell_idx);
    //printf("Exclusion mask at start:  ");
    //for(int j=0; j<P_RANGE; j++) printf("%d%s", exclusion_counts[j], (j==8) ? "\n" : " ");
    
    sub_component sub;

    sub = get_row(cell_idx/9, sudoku);
    char row_exclusion_index = cell_idx%9;
    get_single_exclusion_data(exclusion_counts, row_exclusion_index, sub);
    //printf("Exclusion mask after row: ");
    //for(int j=0; j<P_RANGE; j++) printf("%d%s", exclusion_counts[j], (j==8) ? "\n" : " ");

    sub = get_col(cell_idx%9, sudoku);
    char col_exclusion_index = cell_idx/9;
    get_single_exclusion_data(exclusion_counts, col_exclusion_index, sub);
    //printf("Exclusion mask after col: ");
    //for(int j=0; j<P_RANGE; j++) printf("%d%s", exclusion_counts[j], (j==8) ? "\n" : " ");

    sub = get_block(cell_idx, sudoku);
    // The following index gets the "relative index" of the cell in the block
    // it belongs to. E.g. cell 17 is at coordinates (2, 8) in the total sudoku,
    // belonging to the rightmost block in the first row of blocks. Inside that 
    // block it is the rightmost one of the middle row, and it's index there is 
    // thus 5.
    char block_exclusion_index =  3*((cell_idx/9) % 3) + ((cell_idx%9) % 3);
    get_single_exclusion_data(exclusion_counts, cell_idx%9, sub);
    //printf("Exclusion mask after blo: ");
    //for(int j=0; j<P_RANGE; j++) printf("%d%s", exclusion_counts[j], (j==8) ? "\n" : " ");


    for(int i=0; i<P_RANGE; i++) {
        values_to_exclude[i] = (exclusion_counts[i] > 0) ? 1 : 0;
    }
    //printf("Exclusion return is:      ");
    //for(int j=0; j<P_RANGE; j++) printf("%d%s", values_to_exclude[j], (j==8) ? "\n" : " ");

    
}


bool reduce_possibilities(p_grid sudoku) {
    bool changes = false;

    for(int cell_idx=0; cell_idx<SUDOKU_LIST_LENGTH; cell_idx++){
        // If the cell value is already known, i.e. >0, it will not change.
        if (p_array_interpreter(sudoku[cell_idx/9][cell_idx%9])) continue;

        //printf("Reducer working on cell_idx %2d.\n", cell_idx);       
        char values_to_exclude[9] = {0};
        get_total_exclusions(values_to_exclude, cell_idx, sudoku);
        //printf("Exclusion array is: ");
        //for(int j=0; j<P_RANGE; j++) printf("%d%s", values_to_exclude[j], (j==8) ? "\n" : " ");
        for(int i=0; i<P_RANGE; i++){
            bool current_possibility = sudoku[cell_idx/9][cell_idx%9][i];
            bool exclude_possibility = values_to_exclude[i];
            char new_p = (current_possibility && !exclude_possibility) ? 1 : 0;
            sudoku[cell_idx/9][cell_idx%9][i] = new_p;
            changes = changes || (current_possibility != new_p);
        }
    }

    return changes;
}

char first_unsolved_cell_index(p_grid sudoku) {
    for(int cell_idx=0; cell_idx<SUDOKU_LIST_LENGTH; cell_idx++) {
        char num_value = p_array_interpreter(sudoku[cell_idx/9][cell_idx%9]);
        if (num_value==0) return cell_idx;
    }
    return -1;
}

void get_cell_possibilities(char cell_index, p_grid sudoku, char possibilities[P_RANGE]) {
    for(int i=0; i<P_RANGE; i++){
        char p = sudoku[cell_index/9][cell_index%9][i];
        possibilities[i] = (p > 0) ? i+1 : 0;
    }
}

void copy_first_sudoku_contents_to_second(p_grid sudoku_in, p_grid sudoku_out) {
    for(int cell_index=0; cell_index<SUDOKU_LIST_LENGTH; cell_index++){
        for(int j=0; j<P_RANGE; j++) {
            sudoku_out[cell_index/9][cell_index%9][j] = sudoku_in[cell_index/9][cell_index%9][j];
        }
    }
}

void set_cell_of_sudoku(char cell_index, p_grid sudoku, char new_value) {
    for(int i=0; i<P_RANGE; i++) {
        sudoku[cell_index/9][cell_index%9][i] = (new_value == 0) ? 1 : 0;
    }
    if (new_value != 0) sudoku[cell_index/9][cell_index%9][new_value-1] = 1;    
}

int recursion_depth = 0;
bool recursive_solver(p_grid sudoku){
    recursion_depth++;
    //printf("Recursing at depth %3d.", recursion_depth);
    // This is the main recursive loop.
    do
    {
        if (! still_solvable(sudoku)) return false;
    } while (reduce_possibilities(sudoku));

    char cell_idx = first_unsolved_cell_index(sudoku);
    if (cell_idx == -1) {
        recursion_depth--;
        return true;
    }

    char possibilities[P_RANGE] = {0};
    get_cell_possibilities(cell_idx, sudoku, possibilities);
    for(int index = 0; index < P_RANGE; index++) {
        char fixed_number = possibilities[index];
        if (!fixed_number) continue;

        char local_sudoku[SUDO_X][SUDO_Y][P_RANGE] = {0};
        copy_first_sudoku_contents_to_second(sudoku, local_sudoku);
        set_cell_of_sudoku(cell_idx, local_sudoku, fixed_number);
        bool result = recursive_solver(local_sudoku);
        if (result) {
            copy_first_sudoku_contents_to_second(local_sudoku, sudoku);
            recursion_depth--;
            return true;
        }
    }
    recursion_depth--;
    return false;

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

void convert_p_grid_to_sudoku_string(p_grid sudoku, char* input_sudoku_string) {
    char c;
    for(int cell_index = 0; cell_index < SUDOKU_LIST_LENGTH; cell_index++){
        c = '0' + p_array_interpreter(sudoku[cell_index/9][cell_index%9]);
        input_sudoku_string[cell_index] = c;
    }
}


void solve_from_string(sudoku_string sudoku_input, sudoku_string sudoku_result) {
    p_grid sudoku = {0};
    convert_sudoku_string_to_p_grid(sudoku_input, sudoku);
    recursive_solver(sudoku);
    char result[82] = {0}; //Sudoku string has 81 num chars and then '\0'.
    convert_p_grid_to_sudoku_string(sudoku, result);
    strcpy(sudoku_result, result);
}

void extract_data_from_line(char line[], char s_in[82], char s_out[82]){
    for(int i=0; i<81; i++) s_in[i] = line[i];
    for(int j=82; j<163; j++) s_out[j-82] = line[j];
    s_in[81] = '\0';
    s_out[81] = '\0';
}

void run_csv(int limit, char* filepath, bool output_filepath_flag, char* output_filepath) {
    char s_in[82];
    char s_out[82];
    char in_buffer[255];
    FILE *fp, *fp_out;
    fp = fopen(filepath, "r");

    if (output_filepath_flag) fp_out = fopen(output_filepath, "w");

    int line_no = 0;
    int correct_count = 0;
    char result[82];
    while((fscanf(fp, "%s", in_buffer) != EOF) && (--limit >= 0)) {
        extract_data_from_line(in_buffer, s_in, s_out);

        line_no++;
        solve_from_string(s_in, result);
        if (!strcmp(result, s_out)) correct_count++;
        else printf("\n\nDiscrepancy. Below is in, out, excpected.\n%s\n%s\n%s\n\n", s_in, result, s_out);

        if (output_filepath_flag) fprintf(fp_out, "%s,%s\n", s_in, result);

    }


    fclose(fp);
    if (output_filepath_flag) fclose(fp_out);

    printf("We got %8d / %8d correct!", correct_count, line_no);
}


//////////////////////////////////
// Tests
/////////////////////////////////


void run_generation_and_sub_access_tests() {
    char TEST_SUDOKU_STRING[] = "765082090913004080840030150209000546084369200006405000000040009090051024001890765";
    char NULL_SUDOKU_STRING[] = "000000000000000000000000000000000000000000000000000000000000000000000000000000000";
    p_grid sudoku = {0};

    printf("%s\n", TEST_SUDOKU_STRING);
    convert_sudoku_string_to_p_grid(TEST_SUDOKU_STRING, sudoku);
    print_sudoku(sudoku);

    //printf("%s\n", TEST_SUDOKU_STRING);
    //convert_sudoku_string_to_p_grid(NULL_SUDOKU_STRING, sudoku);
    //print_sudoku(sudoku);

    printf("Row 4 contents:        ");
    sub_component test_row = get_row(4, sudoku);
    p_array_pretty_print(test_row);

    printf("Col 5 contents:        ");
    sub_component test_col = get_col(5, sudoku);
    p_array_pretty_print(test_col);
    /*for(int i=0; i<9; i++){
        printf("%d| ", i+1);
        for(int j=0; j<9; j++) printf("%d ", test_col[i][j]);
        printf("\n");
    }
    printf("\n");*/

    printf("Block 8 contents:      ");
    sub_component test_block = get_block(80, sudoku);
    p_array_pretty_print(test_block);

}

void run_solvability_and_access_tests() {
    char TEST_SUDOKU_STRING[] = "765082090913004080840030150209000546084369200006405000000040009090051024001890765";
    char NULL_SUDOKU_STRING[] = "000000000000000000000000000000000000000000000000000000000000000000000000000000000";
    p_grid sudoku = {0};

    printf("%s\n", TEST_SUDOKU_STRING);
    convert_sudoku_string_to_p_grid(TEST_SUDOKU_STRING, sudoku);
    print_sudoku(sudoku);

    // Test positive solvability
    if (still_solvable(sudoku)) printf("This is solvable.\n\n");

    // Test row collision detection
    set_cell_of_sudoku(6, sudoku, 7);
    print_sudoku(sudoku);
    if (still_solvable(sudoku)) printf("This is solvable.\n\n");
    else printf("This is NOT solvable.\n\n");

    // Test col collision detection
    convert_sudoku_string_to_p_grid(NULL_SUDOKU_STRING, sudoku);
    set_cell_of_sudoku(6, sudoku, 5);
    set_cell_of_sudoku(33, sudoku, 5);
    print_sudoku(sudoku);
    if (still_solvable(sudoku)) printf("This is solvable.\n\n");
    else printf("This is NOT solvable.\n\n");

    // Test block collision detection
    convert_sudoku_string_to_p_grid(NULL_SUDOKU_STRING, sudoku);
    set_cell_of_sudoku(60, sudoku, 8);
    set_cell_of_sudoku(80, sudoku, 8);
    print_sudoku(sudoku);
    if (still_solvable(sudoku)) printf("This is solvable.\n\n");
    else printf("This is NOT solvable.\n\n");

    // Test zero possibility detection
    convert_sudoku_string_to_p_grid(TEST_SUDOKU_STRING, sudoku);
    for(int i=0; i<9; i++) sudoku[0][0][i] = 0;
    print_sudoku(sudoku);
    if (still_solvable(sudoku)) printf("This is solvable.\n\n");
    else printf("This is NOT solvable.\n\n");
}

void run_possibility_reduction_tests(){
    printf("\n<<<< Possibility Reduction Tests >>>>\n");
    char TEST_SUDOKU_STRING[] = "765082090913004080840030150209000546084369200006405000000040009090051024001890765";
    char NULL_SUDOKU_STRING[] = "000000000000000000000000000000000000000000000000000000000000000000000000000000000";
    p_grid sudoku = {0};
    convert_sudoku_string_to_p_grid(TEST_SUDOKU_STRING, sudoku);

    print_sudoku(sudoku);
    // Test row exclusion retrieval
    
    sub_component sub;
    int cell_idx = 27;

    char row_exclusion_counts[9] = {0};
    sub = get_row(cell_idx/9, sudoku);
    get_single_exclusion_data(row_exclusion_counts, cell_idx%9, sub);
    printf("For cell_idx %2d ROW exclusion array is: ", cell_idx);
    for(int j=0; j<P_RANGE; j++) printf("%d%s", row_exclusion_counts[j], (j==8) ? "\n" : " ");
    printf("Extracted from sub values of:           ");
    for(int j=0; j<P_RANGE; j++) printf("%d%s", p_array_interpreter(sub[j]), (j==8) ? "\n" : " ");
    printf("\n");

    char col_exclusion_counts[9] = {0};
    sub = get_col(cell_idx%9, sudoku);
    get_single_exclusion_data(col_exclusion_counts, cell_idx/9, sub);
    printf("For cell_idx %2d COL exclusion array is: ", cell_idx);
    for(int j=0; j<P_RANGE; j++) printf("%d%s", col_exclusion_counts[j], (j==8) ? "\n" : " ");
    printf("Extracted from sub values of:           ");
    for(int j=0; j<P_RANGE; j++) printf("%d%s", p_array_interpreter(sub[j]), (j==8) ? "\n" : " ");
    printf("\n");

    char blo_exclusion_counts[9] = {0};
    sub = get_block(cell_idx, sudoku);
    char block_exclusion_index =  3*((cell_idx/9) % 3) + ((cell_idx%9) % 3);
    get_single_exclusion_data(blo_exclusion_counts, block_exclusion_index, sub);
    printf("For cell_idx %2d BLO exclusion array is: ", cell_idx);
    for(int j=0; j<P_RANGE; j++) printf("%d%s", blo_exclusion_counts[j], (j==8) ? "\n" : " ");
    printf("Extracted from sub values of:           ");
    for(int j=0; j<P_RANGE; j++) printf("%d%s", p_array_interpreter(sub[j]), (j==8) ? "\n" : " ");
    printf("\n");

    char values_to_exclude[9] = {0};
    get_total_exclusions(values_to_exclude, cell_idx, sudoku);
    printf("Total exclusion array is:               ");
    for(int j=0; j<P_RANGE; j++) printf("%d%s", values_to_exclude[j], (j==8) ? "\n" : " ");
    

    convert_sudoku_string_to_p_grid(TEST_SUDOKU_STRING, sudoku);
    print_sudoku(sudoku);
    bool changes = false;
    while(changes = reduce_possibilities(sudoku)) {
        print_sudoku(sudoku);
        printf("Changes: %s\n", changes ? "Yes" : "No");
    }
    
}

void run_recursion_tools_tests(){
    printf("\n<<<< Recursion tools Tests >>>>\n");
    char TEST_SUDOKU_STRING[] = "765082090913004080840030150209000546084369200006405000000040009090051024001890765";
    p_grid sudoku = {0};
    convert_sudoku_string_to_p_grid(TEST_SUDOKU_STRING, sudoku);

    char first = first_unsolved_cell_index(sudoku);
    print_sudoku(sudoku);
    printf("First unsolved idx: %d.\n", first_unsolved_cell_index(sudoku));

    reduce_possibilities(sudoku);
    print_sudoku(sudoku);
    printf("First unsolved idx: %d.\n", first_unsolved_cell_index(sudoku));

    while(reduce_possibilities(sudoku));
    print_sudoku(sudoku);
    printf("First unsolved idx: %d.\n", first_unsolved_cell_index(sudoku));

    printf("\n");
    convert_sudoku_string_to_p_grid(TEST_SUDOKU_STRING, sudoku);
    reduce_possibilities(sudoku);
    print_sudoku(sudoku);
    char cell_index = 43;
    char ps[9] = {0};
    get_cell_possibilities(cell_index, sudoku, ps);
    printf("\nPossibilities at cell index %2d are: ", cell_index);
    for(int j=0; j<9; j++) printf("%d%s", ps[j], (j==8) ? "\n" : " ");

    printf("\n");
    p_grid sudoku_1 = {0};
    p_grid sudoku_2 = {0};
    convert_sudoku_string_to_p_grid(TEST_SUDOKU_STRING, sudoku_2);
    copy_first_sudoku_contents_to_second(sudoku_2, sudoku_1);
    print_sudoku(sudoku_1);
    print_sudoku(sudoku_2);

    set_cell_of_sudoku(0, sudoku_1, 8);
    set_cell_of_sudoku(1, sudoku_2, 8);

    print_sudoku(sudoku_1);
    print_sudoku(sudoku_2);

}



void run_csv_sudokus_tests(int limit) {
    p_grid sudoku = {0};
    char s_in[82];
    char s_out[82];
    FILE *fp;
    char in_buffer[255];
    fp = fopen("../data/10k_sudokus.csv", "r");
    int line_no = 0;
    int correct_count = 0;
    char result[82];
    while((fscanf(fp, "%s", in_buffer) != EOF) && (--limit >= 0)) {
        extract_data_from_line(in_buffer, s_in, s_out);

        line_no++;
        //convert_sudoku_string_to_p_grid(s_in, sudoku);
        //recursive_solver(sudoku);
        solve_from_string(s_in, result);
        if (!strcmp(result, s_out)) correct_count++;
        else printf("\n\nDiscrepancy. Below is in, out, excpected.\n%s\n%s\n%s\n\n", s_in, result, s_out);
    }
    fclose(fp);

    printf("We got %8d / %8d correct!", correct_count, line_no);
}


void run_full_solver_tests() {
    char HARD_SUDOKU_STRING[] = "536000000000703000100800059002000571600070008457010030061390705708620413300187600";
    p_grid sudoku = {0};
    convert_sudoku_string_to_p_grid(HARD_SUDOKU_STRING, sudoku);
    print_sudoku(sudoku);
    recursive_solver(sudoku);
    print_sudoku(sudoku);

    char str_input[] = "408309001290050873007600000619005248870400009503090706081920460900006300060803090";
    char excpected_str_output[] = "458379621296154873137682954619735248872461539543298716381927465924516387765843192";
    char result[82];
    solve_from_string(str_input, result);

    printf("\nFull solver received: %s", str_input);
    printf("\nFull solver expected: %s", excpected_str_output);
    printf("\nFull solver got:      %s", result);
    printf("\nDoes it match? %s\n\n", (!strcmp(excpected_str_output, result)) ? "Yes!" : "No.");

    char bad_str_input[] = "448309001290050873007600000619005248870400009503090706081920460900006300060803090";
    char good_excpected_str_output[] = "458379621296154873137682954619735248872461539543298716381927465924516387765843192";
    solve_from_string(bad_str_input, result);

    printf("\nFull solver received: %s", bad_str_input);
    printf("\nFull solver expected: %s", good_excpected_str_output);
    printf("\nFull solver got:      %s", result);
    printf("\nDoes it match? %s\n\n", (!strcmp(excpected_str_output, result)) ? "Yes!" : "No.");
}

void run_filereader_tests(){
    FILE *fp;
    char buff[255];
    fp = fopen("../data/10k_sudokus.csv", "r");

    for(int j=0; j<10;j++){
        fscanf(fp, "%s", buff);
        printf("%d : %s\n", j, buff );

    }
   
    int line_count=0;
    while(fscanf(fp, "%s", buff) != EOF) {
        line_count++;
    }
    printf("Line count: %5d.\n", line_count);
    fclose(fp);



}

void run_csv_separation_tests(){
    FILE *fp;
    char buff[255];
    fp = fopen("../data/10k_sudokus.csv", "r");

    char start[81];
    char result[81];
    for(int j=0; j<10;j++){
        fscanf(fp, "%s", buff);
        extract_data_from_line(buff, start, result);
        printf("%d : %s | %s\n", j, start, result );
    }
    fclose(fp);
}



void run_tests() {
    run_generation_and_sub_access_tests();
    run_solvability_and_access_tests();
    run_possibility_reduction_tests();
    run_recursion_tools_tests();
    run_full_solver_tests();
    run_filereader_tests();
    run_csv_separation_tests();
    run_csv_sudokus_tests(200);
    printf("\nI Finished tests without crashing.\n");
}


int main(int argc, char *argv[]) {
    /* Main function handles CLI. Options are:
     * -r : raw - interprets the given string as a a sudoku to solve.
     * -t : testing - runs the basic tests
     * -B : Benchmarking - runs the sudokus in the specified csv file.
     * -o : output for the benchmarking results
     * -S : Silent
     * */

    bool run_single_sudoku_flag = false;
    bool run_troubleshoot_tests = false;
    bool run_csv_test_file_flag = false;
    bool write_next_benchmark_output = false;
    bool benchmark_output_file_given_flag = false;
    bool silent_flag = false;

    char test_data_filepath[MAX_FILEPATH_LENGTH];
    char benchmark_result_filepath[MAX_FILEPATH_LENGTH];
    char raw_sudoku_string[SUDOKU_LIST_LENGTH];

    // Parse incoming args.
    char *argument;
    bool write_next_raw_sudoku = false;
    bool write_next_csv_filepath = false;
    while(--argc > 0) {
        argument = *++argv;
        if (argument[0] == '-') {
            switch (argument[1]) {
                case 'r':
                    run_single_sudoku_flag = true;
                    write_next_raw_sudoku = true;
                    break;
                case 't':
                    run_troubleshoot_tests = true;
                    break;
                case 'B':
                    run_csv_test_file_flag = true;
                    write_next_csv_filepath = true;
                    break;
                case 'o':
                    write_next_benchmark_output = true;
                    benchmark_output_file_given_flag = true;
                case 'S':
                    silent_flag = true;
                    break;
                default:
                    printf("Illegal option %c\n", argument[1]);
                    argc = 0;
                    break;
            }
        }
        else {
            if (write_next_csv_filepath) { 
                strcpy(test_data_filepath, argument); 
                write_next_csv_filepath = false;
            }

            if (write_next_raw_sudoku) { 
                strcpy(raw_sudoku_string, argument); 
                write_next_raw_sudoku = false;
            }

            if (write_next_benchmark_output) {
                strcpy(benchmark_result_filepath, argument);
                write_next_benchmark_output = false;
            }
            
        }

    }


    if (run_troubleshoot_tests) {
        printf("Running ts tests.\n");
        run_tests();
        printf("\nRunning ts tests complete.\n");
    }

    if (run_csv_test_file_flag) {
        printf("Running csv tests from file %s.\n", test_data_filepath );
        run_csv(10000000, test_data_filepath, benchmark_output_file_given_flag, benchmark_result_filepath);

        printf("\nRunning csv tests done.\n");
    }

    if (run_single_sudoku_flag) {
        char result[82] = {0};
        printf("%s", (silent_flag) ? "" : "Processing single Sudoku.\n");
        if (!silent_flag) printf("Input:  %s\n", raw_sudoku_string);
        if (!silent_flag) printf("Output: ");
        solve_from_string(raw_sudoku_string, result);
        printf("%s\n", result);
        printf("%s", (silent_flag) ? "" : "Processing done.\n");
    }

}