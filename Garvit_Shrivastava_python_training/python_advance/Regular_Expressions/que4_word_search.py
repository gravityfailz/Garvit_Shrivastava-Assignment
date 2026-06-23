"""
Question 4 - Regular Expressions

Use re.search() to check
whether a word exists
in a sentence.
"""

import re


def word_exists(sentence: str, word: str) -> bool:
    """
    Return True if the word exists.
    otherwise false
    """

    # re.search() checks whether
    # the word is present.
    # re.escape() treats special regex
    # characters as normal text.
    # re.IGNORECASE makes the search
    # case-insensitive.
    return bool(re.search(re.escape(word), sentence, re.IGNORECASE))


if __name__ == "__main__":

    print("\n--- Word Search ---")

    sentence = "Python is a language used in AIML."
    word = input("Enter word: ")

    # Display search result.
    if word_exists(sentence, word):
        print("Word found.")
    else:
        print("Word not found.")