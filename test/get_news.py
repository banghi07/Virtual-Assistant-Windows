import requests
from pprint import pprint
import webbrowser
import feedparser
# import feedparser
"""
q = "kết quả bầu cử tổng thống mỹ"

url = "https://timkiem.vnexpress.net/?q={}".format(q)

webbrowser.open(url) """


"""
News API:

url = "https://newsapi.org/v2/top-headlines?country=vi&apiKey=9142524a349142a29898ed332a516dc4"

response = requests.get(url).json()

pprint(response) """


# * RSS VNEXPRESS:

url = "https://vnexpress.net/rss/tin-moi-nhat.rss"

# response = requests.get(url)


# pprint(response[0])

news_feed = feedparser.parse(url)
entry = news_feed.entries[1]

print(entry.key())
