#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open files
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 2;
    }

    //Initialize
    BYTE buffer[512]; // create array of 512

    int jpeg_count = 0; // jpeg count

    FILE *out_pointer = NULL; // set poitner to written to NULL

    // filename sting
    char filename[8] = {0};

    while (fread(buffer, 512, 1, input))
    {
        if (buffer[0] == 0xFF && buffer[1] == 0xD8 && buffer[2] == 0xFF && (buffer[3] & 0xF0) ==  0xE0)
        {
            //close outptr if jpeg was found before and written into ###.jpg
            if (out_pointer != NULL)
            {
                fclose(out_pointer);
            }

            sprintf(filename, "%03d.jpg", jpeg_count++);

            //open a new outptr for writing a new found jpeg
            out_pointer = fopen(filename, "w");
        }
        if (out_pointer != NULL)
        {
            fwrite(buffer, 512, 1, out_pointer);
        }

    }
    //close
    fclose(input);
    fclose(out_pointer);
    return 0;

}