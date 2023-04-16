import requests
import sys

topic = sys.argv[1]

def get_news():
    r = requests.get(f'https://newsapi.org/v2/everything?q={topic}&pageSize=5&apiKey=bdc233a737a84cc2bc35d5c06602c0d5', 
                 headers={'Accept': 'application/json'})
    articles = r.json()['articles']
    for article in articles:
        print(article['title'])
        print(article['description'])
        print(f'Read more at {article["url"]}')
        print('###################################################')

get_news()