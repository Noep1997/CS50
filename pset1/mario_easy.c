#include <stdio.h>
#include <cs50.h>

int main(void) {
  // initialize variables
  int height;

  // prompt user for height input
  printf("Height: ");
  do {
    height = GetInt();
    if (height < 0 || height > 23)
      printf("Retry: ");
  } while (height < 0 || height > 23);

  // print half-pyramid
  for (int i = 0; i < height; i++) {
    for (int j = 2; j <= (height - i); j++) {
      printf(" ");
      for (int k = 0; k <= i; k++)
        printf("#");
      printf("#\n");
  }

  // render success
  return 0;
}
