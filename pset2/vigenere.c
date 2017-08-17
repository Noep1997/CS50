#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <cs50.h>

// define max key length for array purpose
#define MAX 50

int main(int argc, char** argv) {
  // Verifying the number of command-line arguments
  if (argc != 2) {
    printf("Usage: ./vigenere k\n");
    return 1;
  }

  // initialize variables
  int length;
  char plaintext[MAX], tmp;

  // verifying that argv is only alphabetical
  for (int i = 0; argv[1][i] != '\0'; i++) {
    if (isalpha(argv[1][i]) == 0) {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
  }

  // getting the length of the key for the modulo
  length = strlen(argv[1]);

  // getting the input string
  printf("plaintext: ");
  fgets (plaintext, MAX, stdin);

  // initialize key and saving argv1 as a string
  char key[length];
  strcpy(key, argv[1]);

  // alphabet index to check for uppercase and lowercase
  for (int j = 0; j < length; j++)
    key[j] -= (key[j] <= 'Z' ? 'A' : 'a');

  // cipher algorithm to encrypt plaintext
  printf("ciphertext: ");
  for (int k = 0, count = 0, n = strlen(plaintext); k < n; k++) {
    if (isalpha(plaintext[k]) == 0)
      printf("%c", plaintext[k]);
    else {
      tmp = (plaintext[k] <= 'Z' ? 'A' : 'a');
      plaintext[k] = plaintext[k] - tmp;
      printf("%c", (((plaintext[k] + key[count % length]) % 26) + tmp));
      count++;
    }
  }

  // print new line and render success
  printf("\n");
  return 0;
}
