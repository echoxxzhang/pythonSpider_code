# 大佬的爬小说方式
import urllib.request
import bs4
import re

# 模拟浏览器访问url并获取页面内容（即爬取源码）
def getHtml(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    headers = {"User-Agent":user_agent}
    request = urllib.request.Request(url,headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read()
    return html


# 爬取整个网页（这里就细致一些，指定编码之类的）
def parse(url):
    html_doc = getHtml(url)
    sp = bs4.BeautifulSoup(html_doc, 'html.parser', from_encoding="utf-8")
    return sp


# 获取书籍目录（正式开始了）
def get_book_dir(url):
    books_dir = []
    name = parse(url).find('div', class_='listmain')
    if name:
        dd_items = name.find('dl')
        dt_num = 0
        for n in dd_items.children:
            ename = str(n.name).strip()
            if ename == 'dt':
                dt_num += 1
            if ename != 'dd':
                continue
            books_info = {}
            if dt_num == 2:
                durls = n.find_all('a')[0]
                books_info['name'] = (durls.get_text())
                books_info['url'] = 'http://www.biqukan.com' + durls.get('href')
                books_dir.append(books_info)
    return books_dir


# 获取章节内容
def get_charpter_text(curl):
    text = parse(curl).find('div', class_='showtxt')
    if text:
        cont = text.get_text()
        cont = [str(cont).strip().replace('\r \xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0', '').replace('\u3000\u3000', '')]
        c = " ".join(cont)
        ctext = re.findall(r'^.*?html', c)
        return ctext
    else:
        return ''


# 获取书籍（目录和内容整合）
def get_book(burl):
    # 目录
    book = get_book_dir(burl)
    if not book:
        return book

    # 内容
    for d in book:
        curl = d['url']
        try:
            print('正在获取章节【{}】【内容】【{}】'.format(d['name'],d['url']))
            ctext = get_charpter_text(curl)
            d['text'] = ctext
            print(d['text'])
            print()
        except Exception as err:
            d['text'] = 'get failed'

    return book


if __name__ == '__main__':
    # 这里我先爬取一本书的，需要多本书，那就再加个爬取首页所有书籍的url就可以
    book = get_book('http://www.biqukan.com/1_1094/')
    print(book)