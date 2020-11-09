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

Gọi "Trợ giúp" hoặc "Help" để được hướng dẫn.

## Note

Những file chính để run code: 

* main.py
* mainwindow.py
* assistant_threads.py
* ./audio

## Changelog

### [11/5/2020]

* Thêm tên thread và signal để theo dõi thread bằng terminal
* Tách những class về thread sang module mới để dễ quản lý
* Cập nhật function thời tiết: xác định vị trí hiện tại bằng IP Address
* Cho function speak chạy trên thread mới để tăng tốc độ phản hồi
* Tra cứu wikipedia bằng một câu (xóa câu hỏi của trợ lý ảo), vd: tra cứu khoa học máy tính
* Mở nhạc, video chỉ với một câu, vd: mở video hoa hải đường
* Thêm một số xử lý ngoại lệ
