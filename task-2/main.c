#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *not_used = "/bin/sh";

void now_called(char *command)
{
    printf("Not quite a shell...\n");
    system(command);
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

    now_called("/bin/date");

    return 0;
}