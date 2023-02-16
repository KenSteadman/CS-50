import csv
import sys


def main():
    """
    The main function of the program. It reads the database and DNA sequence files,
    finds the longest match of each STR in the DNA sequence, and checks the database for
    matching profiles. If a match is found, it prints the name of the matching person.
    If no match is found, it prints "No match".
    """

    # Check for correct command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py *.csv *.txt")
        sys.exit(1)

    # Read database file into a variable
    database_file, subsequences = load_database()
    # Read DNA sequence file into a variable
    dna_sequence = load_DNA_file()
    # Find longest match of each STR in DNA sequence
    result = {}
    for subsequence in subsequences:
        result[subsequence] = longest_match(dna_sequence, subsequence)

    # Check database for matching profiles
    for person in database_file:
        match = 0
        for subsequence in subsequences:
            if int(person[subsequence]) == result[subsequence]:
                match += 1

        # If all subsequences matched, print the name of the matching person and return
        if match == len(subsequences):
            print(person["name"])
            return

    # If no matching person is found, print "No match"
    print("No match")
    return


def load_database():
    """
    Reads the database CSV file specified in the command-line arguments and returns the
    database as a list of dictionaries, with the list of STRs as a separate list.
    """
    database = []
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            database.append(row)

        subsequences = list(database[0].keys())[1:]

    return database, subsequences


def load_DNA_file():
    """
    Reads the DNA sequence TXT file specified in the command-line arguments and returns
    the DNA sequence as a string.
    """
    with open(sys.argv[2], "r") as file:
        dna_sequence = file.read()

    return dna_sequence


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
