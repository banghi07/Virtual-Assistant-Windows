from news_window import Ui_Form
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from PyQt5.QtGui import QImage, QPixmap
import feedparser
import requests
import time
import urllib3


class News:
    def __init__(self, result):
        # app = QtWidgets.QApplication(sys.argv)
        self.Form = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.Form)
        self.set_news_form()
        self.result = result
        # self.result = self.get_news()

        widget_list = list()

        for i in range(5):
            widget = QtWidgets.QWidget(self.ui.scrollAreaWidgetContents)
            widget.setFixedSize(535, 500)
            widget_layout = QtWidgets.QVBoxLayout(widget)
            widget_layout.setContentsMargins(0, 0, 0, 30)

            s = "no_" + str(i)

            label_img = QtWidgets.QLabel(widget)
            url_img = self.result[s]["cover_img"]
            label_img.setPixmap(QPixmap(url_img))
            label_img.setScaledContents(True)
            # label_img.setFixedSize(250, 150)
            widget_layout.addWidget(label_img)

            label_title = QtWidgets.QLabel(widget)
            label_title.setText("[Title] " + self.result[s]["title"])
            widget_layout.addWidget(label_title)

            label_decs = QtWidgets.QLabel(widget)
            label_decs.setText("[Desc] " + self.result[s]["description"])
            label_decs.setWordWrap(True)
            widget_layout.addWidget(label_decs)

            label_link = QtWidgets.QLabel(widget)
            label_link.setText("[Link] " + self.result[s]["link"])
            label_decs.setWordWrap(True)
            widget_layout.addWidget(label_link)

            widget_list.append(widget)

        for w in widget_list:
            self.ui.verticalLayout.addWidget(w)

        self.Form.show()
        # sys.exit(app.exec_())

    def set_news_form(self):
        self.Form.setWindowTitle("Tin Tức")
        self.ui.tabWidget.setTabText(0, "Tin mới nhất")

    def get_news(self):
        url = "https://vnexpress.net/rss/tin-moi-nhat.rss"

        def split_content(text):
            i_desc = text.rfind(">")
            i_start_img = text.rfind("src=")
            i_end_img = text.rfind("/>")

            if i_start_img == -1:
                image_cover = "none"
            else:
                link_image = text[i_start_img + 5 : i_end_img - 2]
                image_cover = link_image.replace("amp;", "")

            description = text[i_desc + 1 :]
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
        result = {}

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

            if "none" in img_url:
                article = {
                    "title": article_title,
                    "published_at": article_published_at,
                    "cover_img": "./image/no_img.jpg",
                    "description": content["desc"],
                    "link": article_link,
                }
            else:
                img_data = requests.get(img_url).content
                with open(filename, "wb") as handler:
                    handler.write(img_data)

                article = {
                    "title": article_title,
                    "published_at": article_published_at,
                    "cover_img": filename,
                    "description": content["desc"],
                    "link": article_link,
                }

            key = "no_" + str(i)
            result.update({key: article})
            i += 1

        return result


if __name__ == "__main__":
    News()
