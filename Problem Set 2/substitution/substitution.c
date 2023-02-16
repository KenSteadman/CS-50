#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>


bool key_validation(string key);
// string user_input();
void enciper(string key, string plain_text);

int main(int argc, string argv[])
{
    string key = argv[1];

    if (argc != 2)// if command line arguments are more or less than 2 return error and end immediately
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    if (key_validation(key)) // validate key
    {
        string plain_text = get_string("Plain text: "); // if key is validated prompt user for plain text to be encoded

        enciper(key, plain_text);// function to enciper plaintext with key
    }
    else
    {
        return 1; // if key is invalidated return 1
    }

}


bool key_validation(string key)
{
    int len = strlen(key); // length of key

    if (len != 26) // if length of key is not 26 print error messge and return false
    {
        printf("Key must contain 26 characters.\n");
        return false;
    }

    for (int i = 0; i < len; i++) // if key contains values other than alphabetical print error messge and return false
    {
        if (!isalpha(key[i]))
        {
            printf("Error: Key can only contain letters\n");
            return false;
        }
    }
    for (int i = 0; i < len - 1; i++)
    {
        for (int j = i + 1; j < len; j++) // if key print errohas repeated letter print error messge and return false
        {
            if (tolower(key[i]) == tolower(key[j]))
            {
                printf("Error: key cannot contain repeated characters\n");
                return false;

            }
        }
    }

    return true; // if all condition return true return true
}

void enciper(string key, string plain_text) // fuction to enciper plaintext to ciphertext
{
    printf("ciphertext: ");
    int input_len = strlen(plain_text);

    for (int i = 0; i < input_len; i++)
    {

        if (isalpha(plain_text[i])) // checks is letter is alphabetical
        {

            if (isupper(plain_text[i])) // checks is letter is uppercase
            {
                printf("%c", toupper(key[plain_text[i] - 'A'])); //if letter is uppercase print corresponding letter in key
            }
            if (islower(plain_text[i])) // checks is letter is lowercase
            {
                printf("%c", tolower(key[plain_text[i] - 'a'])); //if letter is lowercase print corresponding letter in key
            }
        }
        else
        {
            printf("%c", plain_text[i]); // if value of char is not alphabetical print char
        }

    }
    printf("\n");// print line break
}