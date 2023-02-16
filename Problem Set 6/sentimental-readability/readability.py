import cs50


def main():
    # Prompt the user for input
    text = cs50.get_string("Please enter text: ")

    # Count the number of letters, words, and sentences in the text
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Calculate the Coleman-Liau index
    index = Coleman_Liau_index(letters, words, sentences)

    # Output the grade level based on the index
    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {int(index)}")


def count_letters(text):
    """Count the number of letters in the text.

    Args:
        text (str): The text to count the letters of.

    Returns:
        int: The number of letters in the text.
    """
    l_count = 0
    for l in text:
        if l.isalpha():
            l_count += 1
    return l_count


def count_words(text):
    """Count the number of words in the text.

    Args:
        text (str): The text to count the words of.

    Returns:
        int: The number of words in the text.
    """
    w_count = len(text.split())
    return w_count


def count_sentences(text):
    """Count the number of sentences in the text.

    Args:
        text (str): The text to count the sentences of.

    Returns:
        int: The number of sentences in the text.
    """
    s_count = 0
    # List of punctuation marks that indicate the end of a sentence
    sentence_punctuation = [".", "?", "!"]
    for s in text:
        if s in sentence_punctuation:
            s_count += 1
    return s_count


def Coleman_Liau_index(letters, words, sentences):
    """Calculate the Coleman-Liau index for the given text.

    Args:
        letters (int): The number of letters in the text.
        words (int): The number of words in the text.
        sentences (int): The number of sentences in the text.

    Returns:
        float: The Coleman-Liau index for the text.
    """
    # Calculate the average number of letters per 100 words and the average number of sentences per 100 words
    L = letters / words * 100
    S = sentences / words * 100
    # Calculate the Coleman-Liau index
    index = round(0.0588 * L - 0.296 * S - 15.8)

    return index


if __name__ == "__main__":
    main()
