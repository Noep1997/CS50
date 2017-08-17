#include <stdio.h>
#include <cs50.h>

int main(void) {
  // initialize variables
  int height;

  // prompt user for height
  printf("Height: ");
  do {
    height = GetInt();
    if (height < 0 || height > 23)
      printf("Retry: ");
  } while (height < 0 || height > 23);

  // print the bypramid
  for (int i = 0; i < height; i++) {
    for (int j = 1; j < (height - i); j++)
      printf(" ");
    for (int k = 0; k < i; k++)
      printf("#");
    printf("#  ");
    for (int l = 0; l < i; l++)
      printf("#");
    printf("#\n");
  }

  // render success
  return 0;
}
