#include <stdio.h>

#define X_DIM 3
#define Y_DIM 3
#define CELL_SZ 2

#define IDX_ARR_LEN 3 // not the same as X or Y_DIM!

typedef char CELL[CELL_SZ];          // the basic unit, a char pair.
typedef CELL MYGRID[X_DIM][Y_DIM];   // it's a 2-dimensional grid of cells, as you explained
typedef CELL *CELLPTR_ARR[IDX_ARR_LEN]; // IDX_ARR_LEN pointers to cells
typedef int IDX_ARR[IDX_ARR_LEN][2];     // the 2 is unrelated to CELL_SZ (it's x and y)

CELLPTR_ARR *subfinder(MYGRID *p_grid, IDX_ARR *idxArr) {
    static CELLPTR_ARR result_array;
    int x, y;

    for (int i = 0; i < IDX_ARR_LEN; i++) {
        x = (*idxArr)[i][0];
        y = (*idxArr)[i][1];

        CELL *addr = &(*p_grid)[x][y];
        result_array[i] = addr;
    }

    // Advantage: array out-of-bounds warning.
    // printf("%d\n", (*idxArr)[IDX_ARR_LEN][0]);
    return &result_array;
}

char diagValAt(CELLPTR_ARR* cellPtrArrPtr, int arrIdx, int cellIdx)
{
    return (*(*cellPtrArrPtr)[arrIdx])[cellIdx];
}

int main() {
    MYGRID example_grid = {
            { {1, 1}, {1, 2}, {1, 3} },
            { {2, 1}, {2, 2}, {2, 3} },
            { {3, 1}, {3, 2}, {3, 3} }
    };
    printf("Original center is (%d, %d).\n", example_grid[1][1][0], example_grid[1][1][1]);

    IDX_ARR diag_indeces = { {0,0}, {1,1}, {2,2} };
    CELLPTR_ARR *diagonal = subfinder(&example_grid, &diag_indeces);

    printf("Diagonal is        (%d, %d).\n", (*(*diagonal)[0])[0], (*(*diagonal)[0])[1]);
    printf("                   (%d, %d).\n", (*(*diagonal)[1])[0], (*(*diagonal)[1])[1]);
    printf("                   (%d, %d).\n", (*(*diagonal)[2])[0], (*(*diagonal)[2])[1]);
                                                                                   
    // Changing center cell to 7/8
    example_grid[1][1][0] = 7;
    example_grid[1][1][1] = 8;
    printf("Center is (%d, %d).\n", example_grid[1][1][0], example_grid[1][1][1]);
    printf("Diagonal is        (%d, %d).\n", (*(*diagonal)[0])[0], (*(*diagonal)[0])[1]);
    printf("                   (%d, %d).\n", (*(*diagonal)[1])[0], (*(*diagonal)[1])[1]);
    printf("                   (%d, %d).\n", (*(*diagonal)[2])[0], (*(*diagonal)[2])[1]);

    // Changing middle cell's first elem to 0 through diagonal
    (*(*diagonal)[1])[0] = 0;
    printf("Original center is (%d, %d).\n", example_grid[1][1][0], example_grid[1][1][1]);
    printf("Diagonal center is (%d, %d).\n", (*(*diagonal)[1])[0], (*(*diagonal)[1])[1]);

    // the proper bracketing of the diagonal access gave me a headache.
    // Of course, one could brake it down into steps:
    // diagonal is a pointer to a subthing; de-referenced, it is an array of pointers to cell; 
    // assigned, it is adjusted to a pointer to its first element

    CELL** cellPtrArr = *diagonal;
    CELL* cellPtr = cellPtrArr[1]; // middle
    char* cell = *cellPtr;
    printf("%d %d\n", cell[0], cell[1]);

    // Or you turf it to a function you never look at again once it's tested.
    printf("%d %d\n", diagValAt(diagonal,1,0), diagValAt(diagonal,1,1));

}