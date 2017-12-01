import tushare as ts
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime,timedelta


HOWLONG = 120
DAYS = [(datetime.now() - timedelta(days = i)).strftime('%Y-%m-%d') for i in range(HOWLONG)]
def get_news(code):
    news_list = ts.get_notices(code)
    titles = list(news_list['title'])
    dates = list(news_list['date'])
    urls = list(news_list['url'])

    #print(titles,dates,urls)
    return(titles,dates,urls)

def get_news2(code):
    news_list = ts.get_notices(code)
    titles = list(news_list['title'])
    dates = list(news_list['date'])
    urls = list(news_list['url'])
    keywords = '质押'
    new_titles = []
    new_dates = []
    new_urls = []
    for i in range(len(titles)):
        if keywords in titles[i]:
            new_titles.append(titles[i])
            new_dates.append(dates[i])
            new_urls.append(urls[i])

    return(new_titles,new_dates,new_urls)



def get_note(code,date):
    titles=[]
    dates = []
    urls = []
    try:
        news_list = ts.get_notices(code,date)
        for title,date,url in zip(news_list['title'],news_list['date'],news_list['url']):
            titles.append(title)
            dates.append(date)
            urls.append(url)
    except IndexError:
        pass
    return(titles,dates,urls)

def get_all_note(code):
    days = DAYS
    title_list = []
    date_list = []
    url_list = []
    for day in days:
        titles,dates,urls = get_note(code,day)
        title_list += titles
        date_list += dates
        url_list += urls
    return(title_list,date_list,url_list)


def get_all_note2(code):
    days = DAYS
    title_list = []
    date_list = []
    url_list = []
    keywords = '质押'
    for day in days:
        titles,dates,urls = get_note(code,day)
        if keywords in titles:
            title_list += titles
            date_list += dates
            url_list += urls
    return(title_list,date_list,url_list)

def get_pda(urls):
    pda_urls = []
    for url1 in urls:
        web_data = requests.get(url1)
        time.sleep(0.3)
        web_data.encoding = 'gb2312'
        page_date = web_data.text
        soup = BeautifulSoup(page_date,'lxml')
        #pattern = re.compile('gallery:(.*?)"]},', re.S)
        pda_url = soup.find('th',style="text-align:center").find('a').get('href')
        #print(pda_urls)
        pda_urls.append(pda_url)
    return pda_urls

def get_pda1(url):
    web_data = requests.get(url)
    web_data.encoding = 'gb2312'
    page_date = web_data.text
    soup = BeautifulSoup(page_date,'lxml')
    pda_url = soup.find('th',style="text-align:center").find('a').get('href')
    return pda_url


def main():
    code = '600393'
    *args,urls = get_news(code)
    print(get_pda(urls))


if __name__ == '__main__':
    main()