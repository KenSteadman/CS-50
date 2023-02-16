import cs50


def main():
    # Prompt the user for the amount of change owed
    change_owed = -1
    while change_owed < 0:
        change_owed = cs50.get_float("Change owed: ")

    # Convert the change owed to cents
    change_owed_cents = int(change_owed * 100)

    # Initialize the number of coins to 0
    num_coins = 0

    # Calculate the number of quarters needed
    num_coins += change_owed_cents // 25
    change_owed_cents %= 25

    # Calculate the number of dimes needed
    num_coins += change_owed_cents // 10
    change_owed_cents %= 10

    # Calculate the number of nickels needed
    num_coins += change_owed_cents // 5
    change_owed_cents %= 5

    # Calculate the number of pennies needed
    num_coins += change_owed_cents

    # Print the minimum number of coins needed
    print(num_coins)


if __name__ == "__main__":
    main()
