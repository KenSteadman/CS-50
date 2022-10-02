#include <cs50.h>
#include <stdio.h>




int main(void)
{
    long cc_number;
    do
    {
        // Input credit card (cc) number
        cc_number = get_long("Enter credit card number: ");
    }
    while (cc_number < 0);


    // Calculate the length of cc number
    int count = 0;
    long x = cc_number;
    while (x > 0)
    {
        x = x / 10;
        count++;
    }

    // Determine Validity of length
    if (count != 13 && count != 15 && count != 16)
    {
        printf("INVALID\n");
    }
    else
    {
        // Checksum variables
        int sum_1 = 0;
        int sum_2 = 0;
        int total = 0;


        // Create array of numbers from CC number
        int number[count];
        long cc_number_array = cc_number;
        for (int i = count - 1; i >= 0; i--)
        {
            number[i] = cc_number_array % 10;
            cc_number_array = cc_number_array / 10;
        }
        // Find product of every number in Credit card number array from the second to last number (times 2)
        for (int i = count - 2; i >= 0; i -= 2)
        {
            int result = number[i] * 2;
            sum_1 += result % 10;
            if (result > 9)
            {
                sum_1 += result / 10;
            }
        }
        // Sum all remaining numbers in Credit card number array
        for (int i = count - 1; i >= 0; i -= 2)
        {
            sum_2 += number[i];
        }

        total = sum_1 + sum_2;


        // Check validity of Credit Card Number for Checksum
        // If valid return company of Credit Cardnumber based on first 2 numbers of Credit card
        if (total % 10 != 0)
        {
            printf("INVALID\n");
        }
        else
        {

            long cc_id = cc_number;

            while (cc_id > 100)
            {
                cc_id = cc_id / 10;
            }


            if (cc_id == 37)
            {
                printf("AMEX\n");
            }
            else if (cc_id == 22 || cc_id == 55 || cc_id == 51)
            {
                printf("MASTERCARD\n");
            }
            else if (cc_id == 40 || cc_id == 41 || cc_id == 42)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
    }
}