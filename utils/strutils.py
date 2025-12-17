import shutil
import string

def print_line(char):
    """
    Prints a line of a specified character that exactly matches the console width.
    """
    try:
        # Get the terminal size
        columns, _ = shutil.get_terminal_size()
        
        # Print the character repeated by the number of columns
        print(char * columns)
    except OSError:
        # Fallback if terminal size cannot be determined (e.g., not a real TTY)
        print(char * 80) # Print a default width of 80 characters

def print_newline(num = 1):
    """
    Prints a specified number of new lines.
    """
    if num < 1:
        raise ValueError("Number of new lines must be at least 1.")
    elif num == 1:
        print("")
    else:
        print("\n" * (num-1))

def clean_string(input_string):
    """
    Cleans a string by removing leading and trailing whitespace, removing punctuation and setting everything to lowercase.
    """
    return input_string.strip().translate(str.maketrans('', '', string.punctuation)).replace("\n", " ").replace("\r", " ").lower()