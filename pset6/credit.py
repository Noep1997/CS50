from __future__ import print_function
import cs50
import math

# check the validity of the credit card number
def main():
    # recover number from get_card_number() function
    cc_number = get_card_number()

    cc_len, total_sum, first_two = 0, 0, 0
    mult_by_two = False

    # iterate over credit card number
    while cc_number > 0:
        cur_digit = cc_number % 10

        # add number to sum and multiply by two every other number
        if mult_by_two:
            if cur_digit < 5:
                total_sum += cur_digit * 2
            else:
                total_sum += cur_digit * 2 - 9
        else:
            total_sum += cur_digit

        # keep track of first two digits
        first_two = cur_digit * 10 + math.floor(first_two / 10)

        # prepare for next iteration of the loop
        mult_by_two = not mult_by_two
        cc_number = math.floor(cc_number / 10)
        cc_len += 1

    # check if the card is valid, and if so which type it is
    if total_sum % 10 != 0:
        print("INVALID")
    elif (first_two >= 40 and first_two <= 49) and (cc_len == 13 or cc_len == 16):
        print("VISA")
    elif (first_two == 34 or first_two == 37) and (cc_len == 15):
        print("AMEX")
    elif (first_two >= 51 and first_two <= 55) and (cc_len == 16):
        print("MASTERCARD")
    else:
        print("INVALID")

# prompt the user for the card number
def get_card_number():
    print("Card Number: ", end="")

    # prompt the user for a positive integer
    while True:
        number = cs50.get_int()

        # case for out of bound value
        if number < 0:
            print("Retry: ", end="")

        # case for in bound value
        if number > 0:
            break

    return number

# call main
if __name__ == "__main__":
    main()
