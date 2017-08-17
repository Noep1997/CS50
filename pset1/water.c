#include <stdio.h>
#include <cs50.h>

int main(void) {
  int mins;
  printf("Minutes: ");
  do {
    mins = GetInt();
    if (mins < 0)
      printf("Retry: ");
  } while (mins < 0);
  printf("Bottles: %i\n", mins * 12);

  // render success
  return 0;
}
