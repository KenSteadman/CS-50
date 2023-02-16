// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>


#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 5381;

// Hash table
node *table[N];


// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    node *temp = NULL;
    for (temp = table[hash(word)]; temp != NULL; temp = temp->next)
    {
        if (strcasecmp(word, temp->word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Initialize hash value to a prime number
    unsigned int hash = 5381;

    // Iterate through each character in the word
    for (int i = 0; word[i] != '\0'; i++)
    {
        // Multiply the hash by a prime number and add the ASCII value of the character
        hash = ((hash << 5) + hash) + tolower(word[i]);
    }

    // Return the hash value modulo the number of buckets in the hash table
    return hash % N;
}

int count = 0;

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];

    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (!file)
    {
        fprintf(stderr, "Could not open Dictionary %s.\n", dictionary);
        return false;
    }

    // Initialize all elements of the hash table to NULL
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Initialize the counter for the number of words in the dictionary to 0
    count = 0;

    // Read each word in dictionary
    while (fscanf(file, "%s", word) == 1)
    {
        // Remove newline character from the end of the word
        word[strcspn(word, "\n")] = '\0';

        // Allocate memory for a new node
        node *temp = malloc(sizeof(node));
        if (temp == NULL)
        {
            fprintf(stderr, "Unable to allocate memory for new node.\n");
            return false;
        }

        // Store the word in the new node
        strcpy(temp->word, word);

        // Insert the new node at the head of the linked list for the appropriate bucket
        temp->next = table[hash(word)];
        table[hash(word)] = temp;

        // Increment the counter for the number of words in the dictionary
        count++;
    }

    // Close the dictionary file
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // return dictionary count
    if (count > 0)
    {
        return count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    int freed_count = 0;
    for (int i = 0; i < N; i++)
    {
        // Loop through every element in buckets
        while (table[i] != NULL)
        {
            node *temp = table[i]->next;
            free(table[i]);
            table[i] = temp;

            // Increment counter for number of nodes freed
            freed_count++;
        }
    }

    // Check if all nodes were properly freed
    if (freed_count != count)
    {
        return false;
    }

    // Set all elements of hash table to NULL
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    // Reset word count to 0
    count = 0;

    return true;
}





