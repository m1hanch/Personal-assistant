import requests
from bs4 import BeautifulSoup
import json


def get_news():
    url = "https://www.bbc.com/news/world"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    video_player_image = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQm42v1XDsudIs2WMM9yGupYi15ntu28Cg5w&usqp=CAU'
    articles = soup.find_all('li', class_='lx-stream__post-container')
    articles_list = []
    for article in articles:
        title = article.find('h3', class_='lx-stream-post__header-title').text
        source = article.find('h3', class_='lx-stream-post__header-title').find('a')
        img = article.find('img', class_='qa-srcset-image')
        img = img['src'] if img else video_player_image
        description = article.find('p', class_='lx-stream-related-story--summary qa-story-summary')
        description = description.text if description else article.find('p', class_='lx-media-asset-summary').text if article.find(
            'p', class_='lx-media-asset-summary') else article.find('div', 'lx-stream-post-body').text
        date = article.find('span', class_='qa-post-auto-meta').text
        article_data = {
            'title': title,
            'source': source,
            'img_link': img,
            'text': description,
            'date': date
        }
        articles_list.append(article_data)

    return articles_list


def get_tech_news(section: str):
    url = f"https://www.bbc.com/news/{section}"
    response = requests.get(url)
    response.encoding = 'utf-8'
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('div', class_='ssrcss-10i168z-LinkPost')
    articles_list = []

    for article in articles:
        source = 'https://www.bbc.com/' + article.find('a', class_='ssrcss-9haqql-LinkPostLink')['href']
        title = article.find('span', class_='ssrcss-1cm0vxx-LinkPostHeadline').text
        img = article.find('img')['src']
        published = article.find('span', class_='ssrcss-dyweam-Timestamp').text
        article_data = {
            'title': title,
            'source': source,
            'img_link': img,
            'date': published
        }
        articles_list.append(article_data)

    return articles_list


def get_sport_news():
    url = "https://en.as.com/soccer/"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article', class_='s')
    articles_list = []
    for article in articles:
        source = article.find('a').get('href')
        img = article.find('img').get('src')
        title = article.find('h2', class_='s__tl').text
        description = article.find('p', class_='s__sum')
        description = description.text if description else ''
        day = article.find('span', class_='s__day')
        day = day.text if day else ""
        hour = article.find('span', class_='s__hour')
        hour = hour.text if hour else ""
        date = f'{day} {hour}'

        article_data = {
            'title': title,
            'source': source,
            'img_link': img,
            'text': description,
            'date': date
        }
        articles_list.append(article_data)
    return articles_list


def get_politics_news():
    url = "https://www.foxnews.com/politics"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find('section', class_='collection collection-article-list').find_all('article', class_='article')
    articles_list = []
    for article in articles:
        source = "https://www.foxnews.com/"+article.find('a').get('href')
        img = article.find('img').get('src')
        title = article.find('h4', class_='title').text
        time = article.find('span', class_='time').text

        article_data = {
            'title': title,
            'source': source,
            'img_link': img,
            'date': time
        }
        articles_list.append(article_data)
    return articles_list


