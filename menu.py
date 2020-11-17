# -*- coding: utf-8 -*-
import news
import database
import matplotlib.pyplot as plt
import deletestopword
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from underthesea import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def get_news():
    print('\n\n[INFO] Chờ vài phút!...')

    for page in range(1, 3):
        URL = f'https://dantri.com.vn/su-kien/trang-{page}.htm'
        news.get_news(URL)

    print('\n\n[INFO] Xong!')


def search_news():
    search_text = input('Từ khóa: ')

    # kết nối database
    db = database.connect_database()

    all_news = []

    for x in db.aggregate([{'$group': {'_id': '$category', 'count': {'$sum': 1}}}]):
        for doc in db.find({'category': x['_id']}):
            all_news.append(doc['title'] + '\n' + doc['quote'])

    vector = TfidfVectorizer()
    x = vector.fit_transform(all_news)
    search_text = search_text.lower()
    te = word_tokenize(search_text, format='text')
    te = deletestopword.remove_stopword(te)
    te = vector.transform([te])
    length = str(te).split('\t')

    if len(length) > 1:
        re = cosine_similarity(x, te)

        result = []

        for i in range(len(re)):
            result.append(re[i][0])

        for i in np.argsort(result)[-20:][::-1]:
            print(all_news[i].split('\n')[0])

    else:
        print(f'Không tìm thấy bài viết có từ khóa "{search_text}"!')


def get_category():
    name = []
    value = []

    # kết nối database
    db = database.connect_database()

    # group và in số lượng từng thể loại
    print('\n SỐ LƯỢNG BÀI VIẾT THEO TỪNG THỂ LOẠI:\n')
    for x in db.aggregate([{'$group': {'_id': '$category', 'count': {'$sum': 1}}}]):
        print(f"{x['_id']}: {x['count']}")
        name.append(x['_id'])
        value.append(x['count'])

    # vẽ biểu đồ
    plt.barh(name, value, color='blue')
    plt.title("THỐNG KÊ SỐ LƯỢNG BÀI VIẾT THEO TỪNG THỂ LOẠI")
    plt.show()


def common_word():
    # kết nối database
    db = database.connect_database()

    for category in db.aggregate([{'$group': {'_id': '$category'}}]):
        my_string = ''

        for col in db.find({'category': category['_id']}):
            my_string += deletestopword.remove_stopword(col['content'] + col['title'] + col['quote'])

        list_string = [my_string]
        vector = CountVectorizer().fit(list_string)
        bag_of_words = vector.transform(list_string)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [(word, sum_words[0, idx]) for word, idx in vector.vocabulary_.items()]
        words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)

        print(f"\nThể loại: {category['_id']} \n - Từ xuất hiện nhiều nhất: {words_freq[0][0]} \n - Số lần xuất hiện: {words_freq[0][1]}")


search_news()
