polish_letters = 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ'
ascii_letters = 'acelnoszz'
punctuation = ",.-?!'"
lowercase = 'abcdefghijklmnopqrstuvwxyz'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

polish_map = str.maketrans(polish_letters, ascii_letters*2)
punc_map = str.maketrans('', '', punctuation)
case_map = str.maketrans(uppercase, lowercase)

all_map = polish_map | punc_map | case_map


# remove punctuation, trailing whitespace, 
# change to lowercase, replace polish letters with ascii
def clean(text):
    text = text.strip().translate(all_map)
    return text


# LEGACY

# replace polish letters with ascii
def polish(text):
    polish_letters = 'ąćęłńóśźż'
    ascii_letters = 'acelnoszz'
    for index, letter in enumerate(polish_letters):
        text = text.replace(letter, ascii_letters[index])
    return text

def clean_legacy(text):
    for char in punctuation:
        text = text.replace(char,'')
    text = text.strip().lower()
    text = polish(text)
    return text
