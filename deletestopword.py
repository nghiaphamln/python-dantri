def get_stopword():
    with open('stopword.txt', encoding='utf-8', mode='r+') as file:
        stopWord = file.readlines()
    return stopWord


def remove_stopword(text):
    stopWord = get_stopword()
    text = ' '.join([word for word in text.split() if word + '\n' not in stopWord])
    return text
