import requests
import json

code = '300033'

def cninfo_news(code):
    # url1 = 'http://www.cninfo.com.cn/cninfo-new/disclosure/szse/fulltext'
    url1 = 'http://www.cninfo.com.cn/new/singleDisclosure/fulltext'
    data = {
        'stock':code,
        'pageNum':1,
        'pageSize':20,
        'plate':'szse',
        'tabname':'latest',
        'limit':''
    }

    content_str = requests.post(url1,data=data)
    content = json.loads(content_str.text)
#    return content

#def parse_content(content):
    main_url = 'http://www.cninfo.com.cn/'
    all_news = content['classifiedAnnouncements']
    #news_num = content['totalAnnouncement']
    #print(content['classifiedAnnouncements'][0][0])
    titles = []
    dates = []
    urls = []
    for day_news in all_news:
        for news in day_news:
            name = news['secName']
            title = name+':'+news['announcementTitle']
            date = list(news['adjunctUrl'].split('/'))[1]
            url_p = main_url + news['adjunctUrl']
            titles.append(title)
            dates.append(date)
            urls.append(url_p)
    return(titles,dates,urls)

def cninfo_news2(code):
    titles,dates,urls = cninfo_news(code)
    keywords = '质押'
    new_titles = []
    new_dates = []
    new_urls = []
    for i in range(len(titles)):
        if keywords in titles[i]:
            new_titles.append(titles[i])
            new_dates.append(dates[i])
            new_urls.append(urls[i])

    return (new_titles, new_dates, new_urls)

if __name__ == '__main__':
   titles,dates,urls = cninfo_news(code)
   print(titles)
