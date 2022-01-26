polishLetters = 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ'
asciiLetters = 'acelnoszz'
punctuation = ",.-?!'"
lowercase = 'abcdefghijklmnopqrstuvwxyz'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

polish_map = str.maketrans(polishLetters, asciiLetters*2)
polish_map2 = list(zip(polishLetters, asciiLetters))
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
    polishLetters = 'ąćęłńóśźż'
    asciiLetters = 'acelnoszz'
    for index, letter in enumerate(polishLetters):
        text = text.replace(letter, asciiLetters[index])
    return text

def clean_legacy(text):
    for char in punctuation:
        text = text.replace(char,'')
    text = text.strip().lower()
    text = polish(text)
    return text
