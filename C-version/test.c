#include <stdio.h>

int main(){
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