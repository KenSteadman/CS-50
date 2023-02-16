def main():
    # Main function that gets the height from the user and calls the build() function to print out the pyramid.
    height = user_input()
    build(height)


def user_input():
    # Gets the height of the pyramid from the user and returns it as an integer.
    while True:
        try:
            height = int(input("What height would you like?: "))
            if height > 0 and height < 9:
                break
            else:
                print("Please enter a number between 1 and 8")
        except ValueError:
            print("Please input a number")

    return height


def build(n):
    # Builds a pyramid of a given height using '#' characters and spaces.
    for i in range(0, n, 1):
        for j in range(0, n, 1):
            # The outer loop iterates through the rows of the pyramid, and the inner loop iterates through the columns.
            # If the row and column indices sum to a value less than n-1, a space is printed. Otherwise, a '#' character is printed.
            if (i + j < n - 1):
                # The 'end' parameter specifies the end of the line for the print statement.
                # In this case, it is set to an empty string so that the output is printed on the same line.
                print(" ", end="")
            else:
                print("#", end="")
        print()


if __name__ == "__main__":
    main()
