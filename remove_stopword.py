import string


# lấy tất cả stopword từ file txt
def get_stop_word():
    stop_word = []

    # mở file và ghi vào list
    with open("vietnamese-stopwords-dash.txt", encoding="utf-8") as file:
        text = file.read()
        for word in text.split():
            stop_word.append(word)
        file.close()

    return stop_word


def remove_stop_word(text):
    # lấy tất cả những từ và kí tự cần loại bỏ
    stop_word = get_stop_word()
    remove_character = list(string.punctuation)
    stop_word += remove_character

    my_string = ""

    # loại bỏ stopword và trả về string
    for word in text.split():
        if word not in stop_word:
            if ("_" in word) or (word.isalpha() is True) or (word.isdigit() is True):
                my_string += word + " "

    return my_string
