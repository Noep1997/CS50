from __future__ import print_function
import cs50

# print the pyramid
def main():
    # recover height from get_positive_int() function
    height = get_positive_int()

    # print the pyramid
    for n in range(height):
        for i in range(height - (n + 1)):
            print(" ", end="")

        for j in range(n + 1):
            print("#", end="")

        print("  ", end="")

        for k in range(n):
            print("#", end="")

        print("#")

# prompt the user height of pyramid
def get_positive_int():
    print("Height: ", end="")

    # prompt the user for a positive integer
    while True:
        height = cs50.get_int()

        # case for out of bound value
        if height > 23 or height < 0:
            print("Retry: ", end="")

        # case for in bound value
        if 0 <= height <= 23:
            break

    return height

# call main
if __name__ == "__main__":
    main()
