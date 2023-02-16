#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <ctype.h>
#include <string.h>

#define OUT 0
#define IN 1


int count_sentences(string text, int string_length);
int count_words(string text, int string_length);
int count_letters(string text, int string_length);
int readability_index(int sentence, int word, int letters);
void grade_response(int index);



int main(void)
{
    string text = get_string("Please enter text: "); // gets user input

    int string_length = strlen(text); // finds length of text

    int sentences = count_sentences(text, string_length); // function return sentence count
    int words = count_words(text, string_length); // function returns word count
    int letters = count_letters(text, string_length); // function retuns letter count
    int index = readability_index(sentences, words, letters); // returns Coleman-Liau index
    grade_response(index); // prints grade leve

    return 0;



}


int count_sentences(string text, int string_length) // function returns the count of sentence in text
{
    int sentences = 0;
    for (int i = 0; i < string_length; i++)
    {
        // counts the number of sentences by find periods, exclamations, and question marks
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }

    return sentences;
}

int count_words(string text, int string_length)// function returns the count of word in text
{
    int words = 0;
    int state = OUT; // sets initial state
    for (int i = 0; i < string_length; i++)
    {
        // If next character is a separator, set the
        // state as OUT
        if (text[i] == ' ' || text[i] == '\n' || text[i] == '\t' || text[i] == '\0')
        {
            state = OUT;
        }
        // If next character is not a word separator and
        // state is OUT, then set the state as IN and
        // increment word count
        else if (state == OUT)
        {
            state = IN;
            words++;
        }
    }

    return words;
}

int count_letters(string text, int string_length)// function returns  the count of letters in text
{
    int letters = 0;
    for (int i = 0; i < string_length; i++)
    {
        if (isalpha(text[i])) //identifies only letters
        {
            letters++;
        }
    }

    return letters;
}

int readability_index(int sentence, int words, int letters)
{
    int index = 0;
    float words_per100 = words / 100.0; // calculates word per 100

    float L = letters / words_per100; // calculation letters per 100 words

    float S = sentence / words_per100;// calculation sentences per 100 words

    index = round(0.0588 * L - 0.296 * S - 15.8); //Coleman-Liau index

    return index;
}

void grade_response(int index)
{
    if (index >= 16) // prints response for grade greater than or equal to 16
    {
        printf("Grade 16+\n");
    }
    else if (index < 1) // prints response for levels below grade 1
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index); // prints response for grade leve 1 to 15
    }
}