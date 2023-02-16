def main():
    # Main function that gets the height from the user and calls the build() function to print out the pyramid.
    height = user_input()
    build(height)


def user_input():
    # Gets the height of the pyramid from the user and returns it as an integer.
    # Validates the user input to ensure it is a number between 1 and 8 (inclusive).
    while True:
        try:
            # Prompt the user to enter the height of the pyramid
            height = int(input("What height would you like?: "))

            # Check if the height is between 1 and 8 (inclusive)
            if height >= 1 and height <= 8:
                # If the height is valid, exit the loop
                break
            else:
                # If the height is not valid, display an error message
                print("Please enter a number between 1 and 8")
        except ValueError:
            # If the user input is not a number, display an error message
            print("Please input a number")

    # Return the height as an integer
    return height


def build(n):
    # Use a loop to print each row of the pattern
    for i in range(n):
        # Build the row by concatenating the spaces and hashes
        row = ""
        for j in range(n - i - 1):
            # Add spaces to the row
            row += " "
        for j in range(i + 1):
            # Add hashes to the row
            row += "#"
        row += "  "
        for j in range(i + 1):
            # Add hashes to the row
            row += "#"

        # Print the row
        print(row)


# Call the main function
if __name__ == "__main__":
    main()
