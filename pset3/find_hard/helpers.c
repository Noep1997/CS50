/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>
#include "helpers.h"


#include <stdio.h>


#define MAX 65536

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
 * Sorts array of n values using Counting Sort (O(n)).
 */
void sort(int values[], int n) {
  // initialize variables
  int result_array[n], max = 0, i;

  // search for maximum value
  for (i = 0; i < n; i++)
    max = (values[i] > max ? values[i] : max);

  // initialize array for counters with max value
  int count_array[max + 1];
  for (i = 0; i < max + 1; i++)
    count_array[i] = 0;

  // count presence of every unique value
  for (i = 0; i < n; i++)
    count_array[values[i]]++;

  // fill counter array
  for (i = 1; i < max + 1; i++)
    count_array[i] = count_array[i] + count_array[i - 1];

  // fill result array with sorted values
  for (i = 0; i < n; i++)
    result_array[count_array[values[i]] - 1] = values[i];
    count_array[values[i]]--;

  // put result back in original array
  for (i = 0; i < n; i++)
    values[i] = result_array[i];

  // render success
  return;
}
