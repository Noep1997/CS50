#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
  // verify valid number of arguments
  if (argc != 2) {
    printf("Usage: ./caesar k\n");
    return 1;
  }

  // initialize variables
  int key;
  char *text;
  k = atoi(argv[1]);

  // prompt user for text to be ciphered
  printf("plaintext: ");
  text = GetString();
  printf("ciphertext: ");

  // cipher the text
  for (int i = 0; i < strlen(text); i++) {
    if (isalpha(text[i]) == 0)
      printf("%c", text[i]);
    else if (islower(text[i]))
      printf("%c", (text[i] - 'a' + key) % 26 + 'a');
    else
      printf("%c", (text[i] - 'A' + key) % 26 + 'A');
  }
  printf("\n");

  // render success
  return 0;
}
