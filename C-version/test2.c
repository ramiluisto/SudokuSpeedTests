#include <stdio.h>

typedef char mygrid[3][3][2];
typedef char** subthing;

subthing subfinder(mygrid p_grid, int indeces[3][2]) {
    static char* result_array[3];
    int x, y;

    for(int i=0; i<3; i++) {
        x = indeces[i][0];
        y = indeces[i][1];

        char* new = p_grid[x][y];
        result_array[i] = new;
    }

    return result_array;
}

int main() {
    mygrid example_grid = {
            { {1, 1}, {1, 2}, {1, 3} }, 
            { {2, 1}, {2, 2}, {2, 3} }, 
            { {3, 1}, {3, 2}, {3, 3} }
        }; 
    printf("Original center is (%d, %d).\n", example_grid[1][1][0], example_grid[1][1][1]);

    int diag_indeces[3][2] = {{0,0}, {1,1}, {2,2}};
    subthing diagonal = subfinder(example_grid, diag_indeces);
    printf("Diagonal is        (%d, %d).\n", diagonal[1][0], diagonal[1][1]);

    example_grid[1][1][0] = 7;
    example_grid[1][1][1] = 8;
    printf("Original center is (%d, %d).\n", example_grid[1][1][0], example_grid[1][1][1]);
    printf("Diagonal is        (%d, %d).\n", diagonal[1][0], diagonal[1][1]);

    diagonal[1][0] = 0;
    printf("Original center is (%d, %d).\n", example_grid[1][1][0], example_grid[1][1][1]);
    printf("Diagonal is        (%d, %d).\n", diagonal[1][0], diagonal[1][1]);
}