
# @searchMusic:
#    - Không sử dụng thread
#    - Không có thông báo khi loading
def searchMusic(self, text):
    if "none" in text:
        self.response("Xin lỗi, tôi không nghe rõ bạn nói gì!")
    else:
        result = search_youtube([text])
        url = "https://www.youtube.com/watch?v=" + result[0]["id"]  
        webbrowser.open(url)
        self.response("Đã mở bài hát bạn yêu cầu.")