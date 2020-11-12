import news
import database
import matplotlib.pyplot as plt
import numpy as np
import deletestopword


def get_news():
    print('\n\n[INFO] Chờ vài phút!...')

    for page in range(1, 3):
        URL = f'https://dantri.com.vn/su-kien/trang-{page}.htm'
        news.get_news(URL)

    print('\n\n[INFO] Xong!')


def search_news():
    # Search text
    search_text = input('Từ khóa: ')

    # Connect to database
    db = database.connect_database()

    # Create index
    db.create_index([('quote', 'text')])

    # Search and return list
    data = list(db.find({'$text': {'$search': search_text}}).limit(10))

    # Check search invalid
    if len(data) == 0:
        print(f'\n\nKhông tìm thấy bài viết có từ khóa "{search_text}"! \n')
        return

    # Print search result
    i = 0
    print(f'Các bài viết có từ khóa "{search_text}":\n')
    for x in data:
        i += 1
        print(f"     {i}. {x['title']}")

        # Choose post
    while True:
        choose = input("\nBài viết muốn xem (Enter để bỏ qua): ")

        # Enter to exit
        if choose == '':
            break

        # Print news
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
    # Syntax
    counts = dict()
    name = []
    value = []

    # Connect to database
    db = database.connect_database()
    data = db.find()

    # Get all category
    for x in data:
        word = x['category']

        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    print('\n SỐ LƯỢNG BÀI VIẾT THEO TỪNG THỂ LOẠI:\n')
    for x, y in counts.items():
        print(f'   - {x}: {y}')
        name.append(x)
        value.append(y)

    # Chart
    y_pos = np.arange(len(name))
    plt.bar(y_pos, value, color='blue')
    plt.title("THỐNG KÊ SỐ LƯỢNG BÀI VIẾT THEO TỪNG THỂ LOẠI")
    plt.xticks(y_pos, name, rotation=90, fontsize=10)
    plt.show()
    # Save as png
    # plt.savefig('./image/chart.png', dpi=1500)


def word_count(string):
    counts = dict()
    string = deletestopword.remove_stopword(string)
    words = string.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    sort_count = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    return sort_count[0]


def max_word():
    # Syntax
    category = []

    # Connect to database
    db = database.connect_database()
    data = db.find()

    # Get all category
    for word in data:
        if word['category'] not in category:
            category.append(word['category'])

    for x in category:
        my_string = ''
        for i in db.find({'category': x}):
            my_string += str(i['content'])
        temp = word_count(my_string)
        print(f" CHỦ ĐỀ: {x} \n  - Từ xuất hiện nhiều nhất: {temp[0]} \n  - Số lần xuất hiện: {temp[1]}\n")

