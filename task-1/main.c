#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void not_called()
{
    printf("Enjoy your shell!\n");
    system("/bin/bash");
}

void vulnerable_function(char *string)
{
    char buffer[8];
    strcpy(buffer, string);
}

int main(int argc, char **argv)
{

    if (argc != 2)
    {
        printf("Please specify one argument!\n");
        return 0;
    }

    vulnerable_function(argv[1]);

    return 0;
}
