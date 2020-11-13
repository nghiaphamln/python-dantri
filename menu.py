# -*- coding: utf-8 -*-
import news
import database
import matplotlib.pyplot as plt
import deletestopword
from sklearn.feature_extraction.text import CountVectorizer


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

    # tạo index
    db.create_index([('quote', 'text')])

    # search và trả về list kết quả
    data = list(db.find({'$text': {'$search': search_text}}).limit(10))

    # có tìm được bài viết không?
    if len(data) == 0:
        print(f'\n\nKhông tìm thấy bài viết có từ khóa "{search_text}"! \n')
        return

    # 10 bài viết liên quan
    i = 0
    print(f'Các bài viết có từ khóa "{search_text}":\n')
    for x in data:
        i += 1
        print(f"     {i}. {x['title']}")

    # chọn bài để đọc
    while True:
        choose = input("\nBài viết muốn xem (Enter để bỏ qua): ")

        # Enter để thoát
        if choose == '':
            break

        # in bài viết đã chọn
        try:
            hihi = data[int(choose) - 1]['title']
            print('\n CHI TIẾT BÀI VIẾT: \n')
            print(f"  - Tiêu đề: {data[int(choose) - 1]['title']}")
            print(f"  - Thể loại: {data[int(choose) - 1]['category']}")
            print(f"  - Liên kết: {data[int(choose) - 1]['link']}")
            print(f"  - Trích dẫn: {data[int(choose) - 1]['quote']}")
            print(f"  - Nội dung: {data[int(choose) - 1]['content']}")
            break
        except:
            print("\nBài viết không tồn tại!")


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
