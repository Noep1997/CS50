#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void) {
  // prompt user for name
  char *name = GetString();

  // convert everything to uppercase
  for (int i = 0; i < strlen(name); i++)
    name[i] = toupper(name[i]);

  // print initials
  printf("%c", name[0]);
  for (int j = 1; j < strlen(name); j++) {
    if (name[j] == ' ')
      printf("%c", name[j + 1]);
  }
  printf("\n");

  // render success
  return 0;
}
