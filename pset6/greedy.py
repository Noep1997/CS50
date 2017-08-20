import cs50

def main():
    # recover change from get_change() function
    change = get_change()

    # convert change in dollars to cents and initialize coins
    cents = round(change * 100)
    coins = 0

    # compute the number of coins and print it
    while cents >= 0:
        coins += 1
        if cents >= 25:
            cents -= 25
        elif cents >= 10:
            cents -= 10
        elif cents >= 5:
            cents -= 5
        elif cents >= 1:
            cents -= 1
        else:
            # reduce 1 coin to balance for extra one added by last loop iteration
            # and reduce 1 cent to reach negative cents and exit loop
            coins -= 1
            cents -= 1
            print("{}".format(coins))

    # render success
    return 0

# prompt the user for the change owed
def get_change():
    print("O hai! How much change is owed?")

    # prompt the user for a positive integer
    while True:
        change = cs50.get_float()

        # case for out of bound value
        if change < 0:
            print("How much change is owed?")

        # case for in bound value
        if change >= 0:
            break

    return change

# call main
if __name__ == "__main__":
    main()
