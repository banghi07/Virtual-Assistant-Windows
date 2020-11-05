import re

text = "dự báo thời tiết tỉnh cần thơ"
reg_ex = re.search("tỉnh", text)


if reg_ex:
    start = reg_ex.end() + 1
    end = len(text)
    city = text[start:end]
    print(city)
else:
    print("false")
