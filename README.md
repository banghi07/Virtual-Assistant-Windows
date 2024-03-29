# Virtual-Assistant

Các chức năng chính:

1. Hiển thị ngày giờ
2. Mở video nhạc trên Youtube
3. Xem dự báo thời tiết
4. Đọc tin tức, thời sự
5. Tra cứu định nghĩa với Wikipedia
6. Mở ứng dụng, phần mềm
7. Mở website
8. Tra cứu từ điển
9. Tìm kiếm từ khóa với Google

Gọi "Trợ giúp" để xem các tính năng được hỗ trợ.

## Note

Những file chính để run code:

- ./audio/
- ./icon/
- ./image/
- ./themes/
- assistant.py (function **main**)
- assistant_sys_tray_icon.py
- assistant_threads.py
- assistant_window.py

## Changelog

### [12/30/2020]

- Cập nhật lại tính năng kiểm tra kết nối internet cho chính xác hơn

### [12/29/2020]

- Giao diện: 100%
- Tổng tiến độ: 100%
- Thêm cửa sổ trợ giúp
- Thêm kiểm tra internet trước khi thực hiện

### [12/28/2020]

- Giao diện: 95%
- Tổng tiến độ: 90%
- Đã thêm giao diện cho chức năng translation
- Đã thêm system_tray_icon

### [21/12/2020]

- Giao diện: 75%
- Tổng tiến độ: 80%
- Đã thêm search_default_window và các tính năng như open_website, open_application

### [19/12/2020]

- Tiến độ: 50%
- Các cửa sổ hiện có: main_window, error_window, clock_window, date_window, weather_window, loading_window, news_window

### [12/12/2020]

- Loại bỏ các module cửa sổ riêng
- Gộp các cửa sổ lại thành một module duy nhất: assistant_window.py
- Thêm style sheet cho module trên (light theme)
- Tiến độ: 15%

### [12/1/2020]

- Thêm class cho chức năng từ điển
- Cửa sổ hiển thị từ được dịch thuộc dạng popup
- Thêm nút để thoát khỏi vòng lặp từ điển (tắt chức năng từ điển)

### [11/25/2020]

- Thêm class weather và cửa sổ hiển thị thời tiết

### [11/21/2020]

- Tách function system tray icon sang class mới
- Thêm class news để hiển thị ảnh bìa, tiêu đề, tóm tắt & liên kết (của RSS) lên cửa sổ mới - news_window
- Thêm một số icon & hình ảnh

### [11/10/2020]

- Cập nhật rss cho function read_news
- Thêm system tray icon cho assistant (gồm 3 tính năng chính hide window, show window và exit)

### [11/5/2020]

- Thêm tên thread và signal để theo dõi thread bằng terminal
- Tách những class về thread sang module mới để dễ quản lý
- Cập nhật function thời tiết: xác định vị trí hiện tại bằng IP Address
- Cho function speak chạy trên thread mới để tăng tốc độ phản hồi
- Tra cứu wikipedia bằng một câu (xóa câu hỏi của trợ lý ảo), vd: tra cứu khoa học máy tính
- Mở nhạc, video chỉ với một câu, vd: mở video hoa hải đường
- Thêm một số xử lý ngoại lệ
