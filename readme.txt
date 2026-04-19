tần số sóng mang là 20Khz
Cách dùng là mọi người cha cách để làm sao có được dự án trên máy tính của mình
rồi dùng lệnh python main.py để chạy    
để biết thêm chi tiết thì tra AI tích hợp sẵn trong vscode 
hoặc nếu không có thì có thể dùng link https:ở trên github của dự án và quẳng cho AI nó đọc

hướng dẫn do AI viết để xem thêm

# SSB MODULATION PROJECT

Dự án mô phỏng quá trình điều chế SSB (Single-Sideband Modulation) bằng Python, tái hiện hoàn toàn các thao tác xử lý bằng MATLAB.
- Tần số lấy mẫu (Sample Rate): 192 kHz
- Tần số sóng mang (Carrier Frequency): 20 kHz

---

## HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH (CÁCH DÙNG)

### Bước 1: Tải dự án về máy tính
Để lấy mã nguồn dự án, bạn có thể sử dụng Git để clone về máy:
```bash
git clone <đường-dẫn-github-của-dự-án>
```
*(Nếu không dùng git, bạn có thể tải file `.zip` trực tiếp từ GitHub rồi giải nén ra).*

### Bước 2: Cài đặt thư viện
Trong dự án này, môi trường ảo (venv) đang được sử dụng. Sau khi mở dự án bằng phần mềm lập trình (ví dụ VSCode), bạn mở Terminal lên và chạy lệnh sau để cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```
*(Yêu cầu máy tính đã cài đặt Python).*

### Bước 3: Chạy chương trình
Sau khi cài xong, bạn gõ lệnh dưới đây vào Terminal (đảm bảo Terminal đang ở thư mục gốc chứa file `main.py`):
```bash
python main.py
```
Chương trình sẽ tự động thực hiện các bước theo đúng trình tự:
1. Ghi âm âm thanh.
2. Lọc tạp âm dư thừa (Butterworth Filter).
3. Thực hiện Điều chế SSB.
4. Hiện cửa sổ vẽ phổ tín hiệu.
5. Cuối cùng, xuất ra một file âm thanh `.wav`.

---

## TÌM HIỂU THÊM CHI TIẾT CODE
- Bạn hoàn toàn có thể hỏi trực tiếp các công cụ **AI tích hợp sẵn trong VSCode** (ví dụ: GitHub Copilot, Cline, v.v.) để yêu cầu mô tả và tìm lỗi.
- Hoặc tham khảo cách này: chép đường dẫn dự án trên GitHub và quẳng cho các AI (hoặc trợ lý AI khác) để chúng đọc và giải thích mọi logic trong dự án giúp bạn.
