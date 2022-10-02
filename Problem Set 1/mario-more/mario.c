#include <cs50.h>
#include <stdio.h>


// Prototypes
int user_input();
void write(int user_height);

int main(void)
{
    int user_height = user_input(); // Get user input and check conditions
    write(user_height);
}

// Function to create pyramid
void write(int user_height)
{
    for (int height = 0; height < user_height; height++)// Increasing variable and intiates line break
    {
        for (int spaces = user_height - height - 2; spaces >= 0; spaces--) // Create spaces to on left side
        {
            printf(" ");
        }
        for (int left_side = 0; left_side <= height; left_side++) // Print # on left side of pyramid
        {
            printf("#");
        }
        printf("  ");// Print center 2 spaces
        for (int right_side = 0; right_side <= height; right_side++)  // Print right side of pyramid
        {
            printf("#");
        }
        printf("\n");// break to next line
    }

}

// Function to get user input and check for conditions
int user_input()
{
    int number;
    do
    {
        number = get_int("What height would you like?: ");
    }
    while (number < 1 || number > 8);
    return number;
}