
#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void) {
  // initialize variables
  long long cc;
  int cc_length, last_digit, first_digit, first_two, sum, curr, i;

  // prompt the user for a card number
  printf("Number: ");
  do {
    cc = GetLongLong();
    if (cc < 0)
      printf("Retry: ");
  } while (cc < 0);

  // initialize a value to most variables that will be used later
  cc_length = floor(log10(cc)) + 1;
  last_digit = cc % 10;
  first_digit = cc / pow(10, cc_length - 1);
  first_two = cc / pow(10, cc_length - 2);
  sum = 0;

  // compute the sum
  for (i = 1; i <= cc_length; i++) {
    // define current digit that's looked at
    curr = floor(fmod(cc / pow(10, cc_length - i), 10));

    // digits to double vary if the length of the card is even or odd
    if (cc_length % 2 == 0) {
      if (i % 2 == 1) {
        if (curr * 2 > 9)
          sum += 1 + (curr * 2) % 10;
        else
          sum += cur * 2
      }
      else
        sum += curr;
    else {
      if (i % 2 == 0) {
        if (curr * 2 > 9)
          sum += 1 + (curr * 2) % 10;
        else
          sum += curr * 2;
      }
      else
        sum += curr;
    }
  }

  // output which type of card it is
  if (sum % 10 == 0) {
    if (first_digit == 4 && (cc_length == 13 || cc_length == 16))
      printf("VISA\n");
    else if (cc_length == 16 && (first_two < 56 && first_two > 50))
      printf("MASTERCARD\n");
    else if (cc_length == 15 && (first_two == 34 || first_two == 37))
      printf("AMEX\n");
    else
      printf("INVALID\n");
  }
  else
    printf("INVALID\n");

  // render success
  return 0;
}
