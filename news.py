import requests
from bs4 import BeautifulSoup
import database


# lấy soup
def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html5lib')


# lấy thể loại
def get_category(soup):
    return soup.find('ul', class_='dt-breadcrumb').find_all('li')[1].a.text


# lấy nội dung
def get_content(soup):
    return ' '.join((soup.find('div', class_='dt-news__body').text.replace('\n', ' ').replace('\r', '')).split())


# lấy id từ url
def get_id(url):
    id = url.split('-')
    return id[-1].replace('.htm', '')


# lấy link hình ảnh
def get_image(soup):
    imageList = []
    image = soup.findAll('img')

    for x in range(1, len(image)):
        imageList.append(image[x]['src'])

    return imageList


# lấy tất cả trường của một tin tức và insert vào database
def get_news(url):
    db = database.connect_database("news")
    soup = get_soup(url)
    a = soup.find_all('a', class_='news-item__sapo')

    for x in a:
        try:
            soup_in_link = get_soup('https://dantri.com.vn' + x.attrs['href'])
            key = {'_id': get_id(x.attrs['href'])}
            value = {
                '$set': {
                    'title': x.attrs['title'],
                    'link': 'https://dantri.com.vn' + x.attrs['href'],
                    'quote': x.text,
                    'image': get_image(soup_in_link),
                    'category': get_category(soup_in_link),
                    'content': get_content(soup_in_link)
                }
            }
            database.insert_database(key, value, db)
        except:
            pass

