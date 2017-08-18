#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// define a struct for BYTE and a constant for JPEG
typedef uint8_t BYTE;
#define JPEG 512

int main(int argc, char *argv[]) {
  // ensure proper usage
  if (argc != 2) {
    fprintf(stderr, "Usage: ./recover image\n");
    return 1;
  }

  // remember filename
  char *filename = argv[1];

  // open input file
  FILE *inptr = fopen(filename, "r");
  if (inptr == NULL) {
    fprintf(stderr, "Could not open %s.\n", filename);
    return 2;
  }

  // allocate enough memory for JPEG & raw_file
  BYTE * buffer = malloc(JPEG);
  char *raw_file = malloc(sizeof(char) * 8);

  // set output file empty before iteration
  FILE *image = NULL;

  // ensure enough memory for buffer & raw_file
  if (buffer == NULL) {
    fprintf(stderr, "Not enough memory\n");
    return 3;
  }
  if (raw_file == NULL) {
    fprintf(stderr, "Not enough memory\n");
    return 4;
  }

  // look through the raw file for a JPEG
  int count = 0;
  while (fread(buffer, JPEG, 1, inptr)) {
    // look for JPEG signature
    if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff
      && (buffer[3] & 0xf0) == 0xe0) {
      // close output file if there is an image in it
      if (image != NULL)
        fclose(image);

      // print and open a new output file
      sprintf(raw_file, "%03i.jpg", count);
      image = fopen(raw_file, "w");
      count++;
    }

    // write in new output file
    if (image != NULL)
      fwrite(buffer, JPEG, 1, image);
  }

  // close the opened files and free the memory
  fclose(inptr);
  fclose(image);
  free(buffer);
  free(raw_file);

  // render success
  return 0;
}
