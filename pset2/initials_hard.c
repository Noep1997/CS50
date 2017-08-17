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

  // verifying for spaces before the name
  if (name[0] != ' ')
    printf("%c", name[0]);

  // printing the rest of the initials
  for (int j = 0; j < strlen(name) - 1; j++) {
    if (name[j] == ' ' && name[j + 1] != ' ')
      printf("%c", name[j + 1]);
  }
  printf("\n");

  // render success
  return 0;
}
