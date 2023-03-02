#include <stdio.h>
#include <stdbool.h> 
#include <stdlib.h>
#include <string.h>


int main() {
    char first[] = "-----";
    char second[7];

    for(int j=0; j<6; j++) second[j] = '-';
    second[5] = '\0';

    printf("First  string: %s\n", first);
    printf("Second string: %s\n", second);
    printf("Does it match? %s\n\n", (!strcmp(first, second)) ? "Yes!" : "No.");
    

}