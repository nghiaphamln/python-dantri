from menu import *
from os import system


menu = """

Menu:

1. Cập nhật tin tức.
2. Tìm kiếm bài viết theo từ khóa.
3. Thống kê số lượng bài viết của từng chủ đề.
4. Thống kê từ xuất hiện nhiều nhất của từng chủ đề.
0. Exit/Quit
"""

while True:
    print(menu)
    ans = input("Chọn chức năng: ")
    if ans == "1":
        get_news()

    elif ans == "2":
        search_news()

    elif ans == "3":
        get_category()

    elif ans == "4":
        common_word()

    elif ans == "0":
        break

    else:
        print('Không tồn tài chức năng này!')
        system('pause')