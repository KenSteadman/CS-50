import sys


def main():
    """
    Entry point for the program.
    Prompts the user for a credit card number, checks if it passes the checksum test, and identifies the credit card type.
    """
    # Get credit card number from user input
    cc_number = user_input()

    # Check if the credit card number passes the checksum test
    if (not verify_checksum(cc_number)):
        print("INVALID")
        sys.exit()
    else:
        identify_credit_card_type(cc_number)


def identify_credit_card_type(c_num):
    """
    Identifies the type of credit card based on its number.
    Supports AMEX, Mastercard, and Visa cards.
    """
    # Check if the credit card is an AMEX card (15 digits, starting with 34 or 37)
    if len(str(c_num)) == 15 and (str(c_num)[0:2] == "34" or str(c_num)[0:2] == "37"):
        print("AMEX")
        sys.exit()

    # Check if the credit card is a Mastercard (16 digits, starting with 51-55)
    elif len(str(c_num)) == 16 and 51 <= int(str(c_num)[0:2]) <= 55:
        print("MASTERCARD")
        sys.exit()

    # Check if the credit card is a Visa card (13 or 16 digits, starting with 4)
    elif str(c_num)[0] == "4" and (len(str(c_num)) == 13 or len(str(c_num)) == 16):
        print("VISA")
        sys.exit()

    # If none of the above conditions are met, the credit card is invalid
    else:
        print("INVALID")
        sys.exit()
        

def user_input():
    """
    Prompts the user for input and returns the input as an integer if it is a positive credit card number.
    Continues to prompt the user until a valid input is entered.
    """
    while True:
        try:
            cc = int(input("Enter credit card number: "))
            if cc > 0:
                break
        except ValueError:
            pass

    return cc


def verify_checksum(x):
    """
    Verifies that the credit card number passes the checksum test.
    Returns True if the number passes the test, False otherwise.
    """
    # Reverse the credit card number
    credit_card_number = str(x)
    reversed_ccn = credit_card_number[::-1]

    # Initialize a sum to hold the values of the digits in the credit card number
    sum = 0

    # Iterate through the digits in the reversed credit card number
    for i in range(len(reversed_ccn)):
        # If the index of the digit is odd (e.g. 1, 3, 5, etc.), double its value
        if i % 2 == 1:
            digit = int(reversed_ccn[i]) * 2
            # If the doubled value is greater than 9, add the digits of the value together (e.g. 18 -> 1 + 8 = 9)
            if digit > 9:
                sum += digit // 10 + digit % 10
            else:
                sum += digit
        # If the index of the digit is even (e.g. 0, 2, 4, etc.), add its value to the sum
        else:
            sum += int(reversed_ccn[i])

    # Return whether the sum is divisible by 10, indicating that the credit card number passes the checksum test
    return sum % 10 == 0


if __name__ == "__main__":
    main()
