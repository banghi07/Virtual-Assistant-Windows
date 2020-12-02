import sys
from PyQt5 import QtWidgets
from weather_window import Ui_Form
import requests
from geopy.geocoders import Nominatim
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from pprint import pprint


class Weather:
    def __init__(self, result):
        # app = QtWidgets.QApplication(sys.argv)
        self.Form = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.Form)
        self.result = result
        self.set_weather_window(self.result)
        self.Form.show()
        # sys.exit(app.exec_())

    def set_weather_window(self, result):
        # self.Form.setStyleSheet("background-color: white")
        self.Form.setWindowTitle("Dự báo thời tiết")

        # Display city name:
        widget = QtWidgets.QWidget()
        widget.setFixedHeight(50)
        widget_layout = QtWidgets.QHBoxLayout(widget)
        widget_layout.setContentsMargins(18, 0, 0, 0)
        lb_city = QtWidgets.QLabel()
        lb_city.setTextFormat(Qt.RichText)
        s = "<b>{}</b>".format(result["city"])
        lb_city.setText(s)
        lb_city.setStyleSheet("font-size: 20px;")
        widget_layout.addWidget(lb_city)
        self.ui.virticalLayout.addWidget(widget)

        # Display icon + temp:
        widget = QtWidgets.QWidget()
        widget_layout = QtWidgets.QHBoxLayout(widget)
        widget_layout.setContentsMargins(0, 10, 0, 0)

        lb_0 = QtWidgets.QLabel()
        widget_layout.addWidget(lb_0)

        no_icon = result["icon"]
        lb_icon = QtWidgets.QLabel()
        s = "./icon/weather/{}.png".format(no_icon)
        lb_icon.setPixmap(QPixmap(s))
        lb_icon.setScaledContents(True)
        lb_icon.setFixedSize(150, 150)
        # lb_icon.setStyleSheet("border: 1px solid black;")
        widget_layout.addWidget(lb_icon)

        lb_1 = QtWidgets.QLabel()
        lb_1.setFixedWidth(40)
        widget_layout.addWidget(lb_1)

        s = "{}<sup>o</sup>C".format(result["temp"])
        lb_temp = QtWidgets.QLabel()
        lb_temp.setTextFormat(Qt.RichText)
        lb_temp.setText(s)
        lb_temp.setStyleSheet("font-size: 50px;")
        lb_temp.setAlignment(Qt.AlignCenter)
        widget_layout.addWidget(lb_temp)

        lb_2 = QtWidgets.QLabel()
        widget_layout.addWidget(lb_2)

        self.ui.virticalLayout.addWidget(widget)

        # Display description
        widget = QtWidgets.QWidget()
        widget.setFixedHeight(50)
        widget_layout = QtWidgets.QHBoxLayout(widget)
        widget_layout.setContentsMargins(0, 10, 0, 0)

        lb = QtWidgets.QLabel()
        widget_layout.addWidget(lb)

        desc = str(result["desc"])
        desc = desc.capitalize()
        s = "<b>Cảm giác như {}<sup>o</sup>C. {}.</b>".format(
            round(result["feel_like"]), desc
        )
        lb_desc = QtWidgets.QLabel()
        lb_desc.setTextFormat(Qt.RichText)
        lb_desc.setAlignment(Qt.AlignCenter)
        lb_desc.setStyleSheet("font-size: 20px;")
        lb_desc.setText(s)
        widget_layout.addWidget(lb_desc)

        lb = QtWidgets.QLabel()
        widget_layout.addWidget(lb)

        self.ui.virticalLayout.addWidget(widget)

        # Display temp, humi, pre, wind, uvi, visibility
        widget = QtWidgets.QWidget()
        widget_layout = QtWidgets.QGridLayout(widget)
        widget_layout.setContentsMargins(0, 9, 0, 18)
        # widget_layout.setSpacing(0)

        s = "Áp suất: {}hPa".format(result["pressure"])
        lb_pressure = QtWidgets.QLabel()
        # lb_pressure.setTextFormat(Qt.RichText)
        lb_pressure.setStyleSheet("font-size: 20px")
        lb_pressure.setText(s)
        widget_layout.addWidget(lb_pressure, 0, 1)
        # self.ui.gridLayout.addWidget(lb_pressure, 2, 1)

        s = "Độ ẩm: {}%".format(result["humidity"])
        lb_humidity = QtWidgets.QLabel()
        # lb_humidity.setTextFormat(Qt.RichText)
        lb_humidity.setStyleSheet("font-size: 20px")
        lb_humidity.setText(s)
        widget_layout.addWidget(lb_humidity, 0, 2)
        # self.ui.gridLayout.addWidget(lb_humidity, 2, 2)

        s = "Có mây: {}%".format(result["cloud"])
        lb_cloud = QtWidgets.QLabel()
        # lb_cloud.setTextFormat(Qt.RichText)
        lb_cloud.setStyleSheet("font-size: 20px")
        lb_cloud.setText(s)
        widget_layout.addWidget(lb_cloud, 1, 1)
        # self.ui.gridLayout.addWidget(lb_cloud, 3, 1)

        s = "Tốc độ gió: {}m/s".format(result["wind_speed"])
        lb_wind = QtWidgets.QLabel()
        # lb_wind.setTextFormat(Qt.RichText)
        lb_wind.setStyleSheet("font-size: 20px")
        lb_wind.setText(s)
        widget_layout.addWidget(lb_wind, 1, 2)
        # self.ui.gridLayout.addWidget(lb_wind, 3, 2)

        s = "Chỉ số UV: {}".format(result["uvi"])
        lb_uvi = QtWidgets.QLabel()
        lb_uvi.setStyleSheet("font-size: 20px")
        lb_uvi.setText(s)
        widget_layout.addWidget(lb_uvi, 2, 1)

        s = "Tầm nhìn xa: {}km".format(float(result["visibility"]) / 1000)
        lb_vis = QtWidgets.QLabel()
        lb_vis.setStyleSheet("font-size: 20px")
        lb_vis.setText(s)
        widget_layout.addWidget(lb_vis, 2, 2)

        for i in range(3):
            widget1 = QtWidgets.QWidget()
            widget1.setFixedWidth(100)
            widget2 = QtWidgets.QWidget()
            widget2.setFixedWidth(100)
            widget_layout.addWidget(widget1, i, 0)
            widget_layout.addWidget(widget2, i, 3)

        self.ui.virticalLayout.addWidget(widget)

    def search_weather_default(self):
        url = "https://ipinfo.io/"
        response = requests.get(url).json()
        city = response["city"]
        region = response["region"]
        location = response["loc"].split(",")

        geolocator = Nominatim(user_agent="Virtual Assistant")
        display_name = geolocator.geocode(city).address

        lat = location[0]
        lon = location[1]
        api = "4e7ced343986de64b7f54296a111c208"
        part = "minutely,hourly,daily,alerts"
        units = "metric"
        lang = "vi"
        url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&units={}&lang={}&appid={}"
        url_one_call = url.format(lat, lon, part, units, lang, api)
        response = requests.get(url_one_call).json()

        # c_lat = response["lat"]
        # c_lon = response["lon"]
        c_cur_time = response["current"]["dt"]
        c_sunrise = response["current"]["sunrise"]
        c_sunset = response["current"]["sunset"]
        c_temp = response["current"]["temp"]
        c_feel_like = response["current"]["feels_like"]
        c_pressure = response["current"]["pressure"]
        c_humidity = response["current"]["humidity"]
        c_dew_point = response["current"]["dew_point"]
        c_clouds = response["current"]["clouds"]
        c_uvi = response["current"]["uvi"]
        c_visibility = response["current"]["visibility"]
        c_wind_speed = response["current"]["wind_speed"]
        # c_wind_gust = response["current"]["wind_gust"]
        c_wind_deg = response["current"]["wind_deg"]
        c_weather_id = response["current"]["weather"][0]["id"]
        c_weather_main = response["current"]["weather"][0]["main"]
        c_weather_description = response["current"]["weather"][0]["description"]
        c_weather_icon = response["current"]["weather"][0]["icon"]

        result = {
            "city": display_name,
            "icon": c_weather_icon,
            "feel_like": c_feel_like,
            "desc": c_weather_description,
            "temp": c_temp,
            "pressure": c_pressure,
            "humidity": c_humidity,
            "cloud": c_clouds,
            "wind_deg": c_wind_deg,
            "wind_speed": c_wind_speed,
            "uvi": c_uvi,
            "visibility": c_visibility,
        }
        return result


if __name__ == "__main__":
    Weather()