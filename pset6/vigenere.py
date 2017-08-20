from __future__ import print_function
import cs50
import sys

# encrypt a text with the vigenere method
def main():
    # ensure proper usage
    if len(sys.argv) != 2 or not str.isalpha(sys.argv[1]):
        print("Usage: python vigenere.py k")
        exit(1)

    # get key and its length for modulo
    key = sys.argv[1]
    length = len(key)

    # prompt user for text
    print("plaintext: ", end="")
    plaintext = cs50.get_string()

    # convert to list
    keyList = list(key)
    textList = list(plaintext)

    # alphabet index to check for uppercase and lowercase
    for i in range(length):
        keyList[i] = chr(ord(keyList[i]) - (ord('A') if ord(keyList[i]) <= ord('Z') else ord('a')))

    # cipher algorithm to encrypt plaintext
    print("ciphertext: ", end="")
    count = 0
    for j in range(len(textList)):
        # do not encrypt nonalphabetical character
        if textList[j].isalpha() == False:
            print("{}".format(textList[j]), end="")
        else:
            tmp = ord('A') if ord(textList[j]) <= ord('Z') else ord('a')
            textList[j] = ord(textList[j]) - tmp
            print("{}".format(chr(((textList[j] + ord(keyList[count % length])) % 26) + tmp)), end="")
            count += 1

    # print newline and render success
    print("")
    return 0

# call main
if __name__ == "__main__":
    main()
