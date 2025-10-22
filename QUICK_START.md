
## Bước 1: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

## Bước 2: Thiết lập database
1. Mở MySQL và tạo database:
```sql
CREATE DATABASE phone_store;
```

2. Import dữ liệu mẫu:
```bash
mysql -u root -p phone_store < database_setup.sql
```

## Bước 3: Cập nhật thông tin kết nối
Sửa file `DB_connect.py`:
```python
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",                    # Thay đổi username
        password="Tonguyen24@",         # Thay đổi password
        database="phone_store"
    )
    return conn
```

## Bước 4: Chạy ứng dụng
```bash
python app.py
```

## Bước 5: Truy cập trang web
Mở trình duyệt và truy cập: http://localhost:5000

## Các trang chính:
- **Trang chủ**: http://localhost:5000
- **Tìm kiếm**: http://localhost:5000/search
- **Giỏ hàng**: http://localhost:5000/cart
- **Quản lý sản phẩm**: http://localhost:5000/admin/products
- **Thêm sản phẩm**: http://localhost:5000/admin/add_product

## Dữ liệu mẫu:
- 8 danh mục điện thoại (iPhone, Samsung, Xiaomi, OPPO, Vivo, OnePlus, Huawei, Realme)
- 8 sản phẩm điện thoại mẫu với đầy đủ thông tin

## Lưu ý:
- Đảm bảo MySQL đang chạy
- Kiểm tra port 5000 không bị sử dụng
- Nếu có lỗi, kiểm tra log trong terminal

