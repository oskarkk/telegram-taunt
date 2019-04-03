def polish1(text):
    polishLetters = 'ąćęłńóśźż'
    asciiLetters = 'acelnoszz'
    for index, letter in enumerate(polishLetters):
        text = text.replace(letter, asciiLetters[index])
    return text

def polish2(text):
    translateDic = {pl: latin for pl, latin in zip('ąćęłńóśźż','acelnoszz')}
    return text.translate(translateDic)

#text = 'Zażółć gęślą jaźń'

def clean(text):
    punctuation = ",.-?!'"
    for char in punctuation:
        text = text.replace(char,'')
    text = text.lower()
    text = polish1(text)
    return text