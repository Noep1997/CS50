/**
 * Implements a dictionary's functionality.
 */

#include "dictionary.h"

// establish struct for linked lists
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// define the hashtable
node *hashtable[SIZE];

// initiate misspelled wordcount
unsigned int wordcount = 0;

// Hash function taken from reddit user delipity:
// https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/cf9nlkn
int hash_it(char* needs_hashing) {
    unsigned int hash = 0;
    for (int i = 0, n = strlen(needs_hashing); i < n; i++)
        hash = (hash << 2) ^ needs_hashing[i];
    return hash % SIZE;
}

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word) {
    // defines wordlength a non-constant char copy of word
    int wordlength = strlen(word);
    char wordcopy[wordlength + 1];

    // sets every character to lowercase through wordcopy to make words
    for (int i = 0; i < wordlength; i++)
        wordcopy[i] = tolower(word[i]);
    wordcopy[wordlength] = '\0';

    // assign cursor to the first node of the bucket
    node *cursor = hashtable[hash_it(wordcopy)];

    // compare word with the entries in the hashtable
    while (cursor) {
        if (strcasecmp(word, cursor->word) == 0)
            return true;
        cursor = cursor->next;
    }
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary) {
   // opens the dictionary file (and sanity check if it can't be opened)
    FILE *file = fopen(dictionary, "r");
    if (!file) {
        printf("Could not open file");
        return 1;
    }

    char word[LENGTH + 1];

    // scan dictionary one word at a time
    while (fscanf(file, "%s", word) != EOF) {
        // allocate memory to each new node (and sanity check if no new node)
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL) {
            unload();
            return false;
        }

        // copy word into node
        strcpy(new_node->word, word);
        wordcount++;

        // insert new_node into our linked list
        new_node->next = hashtable[hash_it(word)];
        hashtable[hash_it(word)] = new_node;
    }
    fclose(file);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void) {
    return wordcount;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void) {
    // iterates through the hashtable
    for (int i = 0; i < SIZE; i++) {
        node *cursor = hashtable[i];

        // free all the linked lists nodes one at a time
        while (cursor) {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
