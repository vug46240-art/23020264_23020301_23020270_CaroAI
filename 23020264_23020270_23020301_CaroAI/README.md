## 🔍 Tổng quan

Trò chơi cờ Caro (hay còn gọi là Five-In-A-Row nhưng được biến thể) là một trò chơi chiến thuật đối kháng dành cho 2 người. Đồ án này mô phỏng bàn cờ kích thước 9x9. Mục tiêu của trò chơi là tạo thành một chuỗi liên tục gồm **4 quân cờ** (theo hàng ngang, dọc hoặc chéo) để giành chiến thắng. Theo luật quy định, trò chơi **không áp dụng luật chặn hai đầu**.
Trong dự án này, người chơi có thể thi đấu trực tiếp với Tác tử AI. Trí tuệ nhân tạo được xây dựng dựa trên thuật toán **Minimax** kết hợp kỹ thuật **cắt nhánh Alpha-Beta** nhằm tối ưu hóa nước đi. Toàn bộ logic và giao diện được xây dựng hoàn toàn bằng Python với thư viện `tkinter` tiêu chuẩn.

**Tính năng nổi bật:**
* Đồ họa Cyberpunk Neon với hiệu ứng phát sáng hiển thị trực quan.
* Tích hợp **Chế độ kiểm thử (Sandbox Mode)** cho phép tự do đặt quân để đo đạc số trạng thái và thời gian tính toán của AI.
* Cho phép chuyển đổi linh hoạt giữa thuật toán Pure Minimax và Alpha-Beta để so sánh hiệu năng.

---

## 📌 Yêu cầu hệ thống (Requirement)

Chương trình được viết hoàn toàn bằng Python thuần và sử dụng thư viện đồ họa GUI `tkinter` (đã được tích hợp sẵn trong thư viện chuẩn của Python). Do đó, bạn không cần cài đặt thêm thư viện bên ngoài như `pygame`.

Yêu cầu duy nhất:
* Cài đặt **Python 3.x** trở lên.

---
## 🎮 Cách tiến hành chơi
- Ở giao diện ảnh dưới, người chơi có thể lựa chọn thi đấu trực tiếp với AI với hai lựa chọn **BẠN ĐI TRƯỚC (X)** hoặc **AI ĐI TRƯỚC(X)**. Hệ thống sẽ mặc định ban đầu chạy **AI: Alpha-Beta** và người chơi có thể đổi sang lựa chọn **AI: Minimax** (không khuyến khích vì rất chậm, chỉ phù hợp để kiểm thử). Khi này thì người chơi chỉ việc bám theo luật chơi bên trên để thi đấu với AI
- Khi muốn kiểm định thế cờ, người chơi có thể bấm vào chế độ kiểm thử để đưa sang chế độ ON và xây dựng tùy thích ván cờ bằng cách đặt quân lần lượt X và O. Nếu muốn tìm nước đi tốt nhất sau thế cờ đó thì có thể chọn **Nước đi AI gợi ý** 
- Nút RESET hoạt động trên cơ chế xóa sạch toàn bộ quân cờ và đưa về trạng thái ban đầu của bàn cờ.
![alt text](image-3.png)
- Ván cờ kết thúc khi màn hình hiển thị như sau (Đối với máy tính):
![alt text](image-4.png)
## 📁 Cấu trúc thư mục (File Structure)

```text
├── main.py            # Chứa giao diện UI (Tkinter) và vòng lặp sự kiện chính
├── ai_logic.py        # Chứa lõi thuật toán AI (Minimax, Alpha-Beta, Evaluation)
├── game_rules.py      # Chứa module xử lý luật chơi (kiểm tra bàn cờ đầy, quét ô thắng)
├── requirements.txt  
└── README.md          # Tài liệu hướng dẫn sử dụng

