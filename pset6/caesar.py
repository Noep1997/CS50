from __future__ import print_function
import cs50
import sys

# encrypt a text with the caesar method
def main():
    # ensure proper usage
    if len(sys.argv) != 2:
        print("Usage: python caesar.py k")
        exit(1)

    # define and convert key to int
    key = int(sys.argv[1])

    # prompt user for text
    print("plaintext: ", end="")
    plaintext = cs50.get_string()

    print("ciphertext: ", end="")
    # iterate over plaintext, encipher each character and print it
    for i in range(len(plaintext)):
        # do not encrypt nonalphabetical character
        if plaintext[i].isalpha() == False:
            print("{}".format(plaintext[i]), end="")

        # encryption for lowercase character
        if plaintext[i].islower():
            cipher_char = chr(((ord(plaintext[i]) - ord("a")) + key) % 26 + ord("a"))
            print("{}".format(cipher_char), end="")

        # encryption for uppercase character
        if plaintext[i].isupper():
            cipher_char = chr(((ord(plaintext[i]) - ord("A")) + key) % 26 + ord("A"))
            print("{}".format(cipher_char), end="")

    # print newline
    print("")

    # render success
    return 0

# call main
if __name__ == "__main__":
    main()
