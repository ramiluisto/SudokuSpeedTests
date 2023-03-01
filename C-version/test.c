#include <stdio.h>

typedef char mygrid[3][3][2];
typedef char** subthing;

typedef char* row[3];

row* subfinder(mygrid p_grid, int indeces[3][2]) {
    static row result_array;
    int x, y;

    for(int i=0; i<3; i++) {
        x = indeces[i][0];
        y = indeces[i][1];

        char* new = p_grid[x][y];
        result_array[i] = new;
    }

    return &result_array;
}

int main() {
    mygrid example_grid = {
            { {1, 1}, {1, 2}, {1, 3} }, 
            { {2, 1}, {2, 2}, {2, 3} }, 
            { {3, 1}, {3, 2}, {3, 3} }
        }; 
    printf("Original center is (%d, %d).\n", example_grid[1][1][0], example_grid[1][1][1]);

    int diag_indeces[3][2] = {{0,0}, {1,1}, {2,2}};
    void* diagonal = subfinder(example_grid, diag_indeces);
    printf("Diagonal is        (%d, %d).\n", diagonal[1][0], diagonal[1][1]);

    example_grid[1][1][0] = 7;
    example_grid[1][1][1] = 8;
    printf("Original center is (%d, %d).\n", example_grid[1][1][0], example_grid[1][1][1]);
    printf("Diagonal is        (%d, %d).\n", diagonal[1][0], diagonal[1][1]);

    diagonal[1][0] = 0;
    printf("Original center is (%d, %d).\n", example_grid[1][1][0], example_grid[1][1][1]);
    printf("Diagonal is        (%d, %d).\n", diagonal[1][0], diagonal[1][1]);
}


/*
    printf("Placeholder as a pointer:                       %p\n", placeholder);
    printf("Placeholder first address content as a pointer: %p\n", *placeholder);

    printf("Placeholder elt 0 as a pointer:                 %p\n", placeholder[0]);
    printf("Placeholder elt 1 as a pointer:                 %p\n", placeholder[1]);
    printf("Placeholder elt 2 as a pointer:                 %p\n", placeholder[2]);

    printf("Placeholder elt 0 subelt 0 as an int:           %d\n", placeholder[0][0]);
    printf("Placeholder elt 0 subelt 1 as an int:           %d\n", placeholder[0][1]);
    printf("Placeholder elt 1 subelt 0 as an int:           %d\n", placeholder[1][0]);
    printf("Placeholder elt 1 subelt 1 as an int:           %d\n", placeholder[1][1]);
    printf("Placeholder elt 2 subelt 0 as an int:           %d\n", placeholder[2][0]);
    printf("Placeholder elt 2 subelt 1 as an int:           %d\n", placeholder[2][1]);

    printf(">>>>Finished!\n");

}


*/

int other(){
    char row1[] = {0,0,0,1,0,0,0,0,0};
    char row2[] = {1,1,1,1,1,1,1,1,1};
    char row3[] = {0,1,0,0,0,0,0,1,0};

    int row_idx;


    row_idx = -2;
    for(int j=0; j<9; j++){
        printf("j: %d, row[j]: %d ", j, row1[j]);
        if (row1[j] == 1) row_idx = (row_idx == -2) ? j : -1;
        printf("%d\n", row_idx);
    }
    printf("%d\n", row_idx);

    printf("\n\n");

    row_idx = -2;
    for(int j=0; j<9; j++){
        printf("j: %d, row[j]: %d ", j, row2[j]);
        if (row2[j] == 1) row_idx = (row_idx == -2) ? j : -1;
        printf("%d\n", row_idx);
    }
    printf("%d\n", row_idx);

    printf("\n\n");

    row_idx = -2;
    for(int j=0; j<9; j++){
        printf("j: %d, row[j]: %d ", j, row3[j]);
        if (row3[j] == 1) row_idx = (row_idx == -2) ? j : -1;
        printf("%d\n", row_idx);
    }
    printf("%d\n", row_idx);

    printf("\n\n");
}