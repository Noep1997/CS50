#include <stdio.h>
#include <stdlib.h>
#include "bmp.h"

int main(int argc, char *argv[]) {
  // declare the factor n
  int n = atoi(argv[1]);

  // ensure proper usage
  if (argc != 4 || n < 1 || n > 100) {
    fprintf(stderr, "Usage: ./resize n infile outfile\n");
    return 1;
  }

  // remember filenames
  char *infile = argv[2];
  char *outfile = argv[3];

  // open input file
  FILE *inptr = fopen(infile, "r");
  if (inptr == NULL) {
    fprintf(stderr, "Could not open %s.\n", infile);
    return 2;
  }

  // open output file
  FILE *outptr = fopen(outfile, "w");
  if (outptr == NULL) {
    fclose(inptr);
    fprintf(stderr, "Could not create %s.\n", outfile);
    return 3;
  }

  // read infile's BITMAPFILEHEADER
  BITMAPFILEHEADER bf;
  fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

  // read infile's BITMAPINFOHEADER
  BITMAPINFOHEADER bi;
  fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

  // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
  if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
      bi.biBitCount != 24 || bi.biCompression != 0) {
    fclose(outptr);
    fclose(inptr);
    fprintf(stderr, "Unsupported file format.\n");
    return 4;
  }

  // Define new resized bi & bf
  BITMAPFILEHEADER bf_resized = bf;
  BITMAPINFOHEADER bi_resized = bi;

  // Define new resized bi & bf height & width
  bi_resized.biWidth = bi.biWidth * n;
  bi_resized.biHeight = bi.biHeight * n;

  // determine padding and resized padding for scanlines
  int padding =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
  int new_padding = (4 - (bi_resized.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

  // determine resized image size
  bi_resized.biSizeImage = ((sizeof(RGBTRIPLE) * bi_resized.biWidth)
                                + new_padding) * abs(bi_resized.biHeight);

  bf_resized.bfSize = bi_resized.biSizeImage + sizeof(BITMAPFILEHEADER)
                                             + sizeof(BITMAPINFOHEADER);

  // write outfile's BITMAPFILEHEADER
  fwrite(&bf_resized, sizeof(BITMAPFILEHEADER), 1, outptr);

  // write outfile's BITMAPINFOHEADER
  fwrite(&bi_resized, sizeof(BITMAPINFOHEADER), 1, outptr);

  // iterate over infile's scanlines
  for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++) {
    // iterate over file n times
    for (int k = 0; k < n; k++) {
      // iterate over pixels in scanline
      for (int j = 0; j < bi.biWidth; j++) {
        // temporary storage
        RGBTRIPLE triple;

        // read RGB triple from infile
        fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

        // write RGB triple to outfile
        for (int l = 0; l < n; l++)
          fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
      }

      // adding new padding
      for (int m = 0; m < new_padding; m++)
        fputc(0x00, outptr);

      // bring the pointer back to beginning of scanline
      if (k < n - 1)
        fseek(inptr, -bi.biWidth * sizeof(RGBTRIPLE), SEEK_CUR);
    }
    // skip over padding, if any
    fseek(inptr, padding, SEEK_CUR);
  }
  // close infile & outfile
  fclose(inptr);
  fclose(outptr);

  // render success
  return 0;
}
