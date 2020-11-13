import string


def get_stopword():
    stop_word = []

    with open("vietnamese-stopwords-dash.txt", encoding="utf-8") as f:
        txt = f.read()
        for word in txt.split():
            stop_word.append(word)
        f.close()

    return stop_word


def remove_stopword(text):
    stop_word = get_stopword()
    remove_character = string.punctuation
    punc = list(remove_character)
    stop_word = stop_word + punc
    my_string = ''

    for word in text.split(' '):
        if word not in stop_word:
            if ('_' in word) or ('|' in word) or (word.isalpha() is True) or (word.isdigit() is True):
                my_string = my_string + word + ' '

    return my_string
