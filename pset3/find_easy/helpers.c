/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false, in O(nlog(n)).
 */
bool search(int value, int values[], int n) {
  // initialize variables
  int start = 0, end = n - 1, half;

  // search the list by dividing in half each time
  while (start <= end) {
    half = (start + end) / 2;

    if (values[half] < value)
      start = half + 1;
    else if (values[half] > value)
      end = half - 1;
    // found if equal
    else
      return true;
  }

  // not found
  return false;
}

/**
 * Sorts array of n values using Bubble Sort (O(n^2)).
 */
void sort(int values[], int n) {
  // initialize variables
  int i, tmp, count;

  do {
    // reset count as false (0) everytime
    count = 0;
    for (i = 0; i < (n - 1); i++) {
      if (values[i] > values[i + 1]) {
        // swaps if left value bigger than right value
        tmp = values[i];
        values[i] = values[i + 1];
        values[i + 1] = tmp;
        count++;
      }
    }
  } while (count > 0);

    // render success
    return;
}
