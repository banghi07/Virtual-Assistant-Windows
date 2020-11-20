import requests
from pprint import pprint
import webbrowser
import feedparser
import time

# q = "kết quả bầu cử tổng thống mỹ"

# url = "https://timkiem.vnexpress.net/?q={}".format(q)

# res = requests.get(url).text
# print(res)


"""
News API:

url = "https://newsapi.org/v2/top-headlines?country=vi&apiKey=9142524a349142a29898ed332a516dc4"

response = requests.get(url).json()

pprint(response) """


# * RSS VNEXPRESS:

url = "https://vnexpress.net/rss/tin-moi-nhat.rss"

# response = requests.get(url).text
# pprint(response)

# =========================================================


def split_content(text):
    i_desc = text.rfind(">")
    i_start_img = text.rfind("src=")
    i_end_img = text.rfind("/>")

    description = text[i_desc + 1 :]
    link_image = text[i_start_img + 5 : i_end_img - 2]

    image_cover = link_image.replace("amp;", "")

    content = {"desc": description, "l_img": image_cover}

    return content


def week_day(i):
    if i == 0:
        return "Thứ hai"
    elif i == 1:
        return "Thức ba"
    elif i == 2:
        return "Thứ tư"
    elif i == 3:
        return "Thứ năm"
    elif i == 4:
        return "Thứ sáu"
    elif i == 5:
        return "Thứ bảy"
    elif i == 6:
        return "Chủ nhật"


def time_format(s_time):
    wday = week_day(s_time.tm_wday)
    t = time.strftime("%d-%m-%Y, %H:%M:%S")
    temp = wday + " " + t
    return temp


feed = feedparser.parse(url)
feed_entries = feed.entries

i = 0
text = ""

for entry in feed_entries:
    if i == 5:
        break

    article_title = entry.title
    article_link = entry.link
    article_published_at = entry.published
    article_published_at_parsed = entry.published_parsed  # Time object
    article_published_at = time_format(article_published_at_parsed)
    content = split_content(entry.summary)

    filename = "./image/cover" + str(i) + ".jpg"
    img_url = content["l_img"]
    img_data = requests.get(img_url).content
    with open(filename, "wb") as handler:
        handler.write(img_data)

    temp = "[Title] {}\n[Published at] {}\n[Image cover] {}\n[Description] {}\n[Link] {}\n\n"
    text = text + temp.format(
        article_title,
        article_published_at,
        content["l_img"],
        content["desc"],
        article_link,
    )
    i += 1

print(text)

# print(week_day(2))
