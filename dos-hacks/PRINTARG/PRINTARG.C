#include <stdio.h>

int main(int argc, char ** argv) {
    int i;

    printf("Arguments:\n\n");

    for (i = 0; i < argc; i++) {
        printf(" - %s\n", argv[i]);

        if (strlen(argv[i]) == 9) {
            char * p;
            sscanf(argv[i], "%p", &p);
            printf("%p\n", p);
        }
    }

    getch();
}

