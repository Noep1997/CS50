#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void) {
  // initialize variables
  float change;
  int coins, cents;

  // prompt user for amount of change
  printf("O hai! How much change is owed?\n");
  do {
    change = GetFloat();
    if (change < 0)
      printf("How much change is owed?\n");
  } while (change < 0);

  // convert change in dollars to cents and initialize coins
  cents = round(change * 100);
  coins = 0;

  // compute the number of coins and print it
  while (cents >= 0) {
    (cents >= 25) ? (coins++, cents -= 25) :
    (cents >= 10) ? (coins++, cents -= 10) :
    (cents >= 5)  ? (coins++, cents -= 5)  :
    (cents >= 1)  ? (coins++, cents--) : (printf("%i\n", coins), cents--);
  }

  // render success
  return 0;
}
