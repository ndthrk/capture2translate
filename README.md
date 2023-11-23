# Mục đích:
- Đọc truyện tranh (manga) bằng tiếng Anh mà không cần gõ lại để dịch
- Có thể chọn 1 vùng văn bản bằng tiếng Anh và dịch sang tiếng Việt
# Cách dùng và cách hoạt động:
- Yes, bạn cần cài đặt python để run code, giao diện đơn giản bằng **Tkinter**
- Khởi động phần mềm, **Ctrl + S** để bắt đầu lắng nghe sự kiện.
- **Z** là điểm bắt đầu, **X** là điểm kết thúc, 2 điểm này sẽ tạo 1 hình chữ nhật chứa vùng text
- Vùng cắt này được xử lý bằng cv2, sau đó được nhận diện bằng **pytesseract**
- Chuỗi string sau khi nhận diện được dịch bằng API của openai
- Văn bản được dịch và văn bản gốc được hiện lên giao diện của app **Tkinter**
# Nhược điểm:
- API openai có giới hạn, cần thay đổi nếu hết số lần. Có thể sử dụng API của google Translate (tuy nhiên sẽ có hạn chế)
- Giới hạn văn bản tuỳ thuộc vào API dịch.
- Độ nhận dạng một vài ký tự chưa cao, Ví dụ:
  + I thành | / \ tuỳ vào độ nghiêng
  + O thành 0
  + S thành 5
  + B thành 8,...
# Hướng phát triển:
- Nhập link đọc truyện, thu thập tất cả các ảnh truyện trong web.
- Xử lý, nhận diện những vùng chứa văn bản trong ảnh sau đó dịch
