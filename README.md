# PhoneStore - Trang web bán điện thoại

Trang web bán điện thoại được xây dựng bằng Flask và MySQL với giao diện hiện đại và responsive.

## Tính năng

### Cho khách hàng:
- ✅ Trang chủ hiển thị sản phẩm nổi bật
- ✅ Tìm kiếm và lọc sản phẩm theo danh mục
- ✅ Xem chi tiết sản phẩm
- ✅ Giỏ hàng (thêm, sửa, xóa sản phẩm)
- ✅ Giao diện responsive, thân thiện với mobile

### Cho quản trị viên:
- ✅ Quản lý sản phẩm (thêm, sửa, xóa)
- ✅ Quản lý danh mục sản phẩm
- ✅ Upload hình ảnh sản phẩm
- ✅ Thống kê sản phẩm

## Cài đặt

### 1. Cài đặt Python và MySQL
- Python 3.8+
- MySQL 5.7+ hoặc 8.0+

### 2. Clone repository
```bash
git clone <repository-url>
cd MyFlaskApp_advance
```

### 3. Tạo virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate
```

### 4. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 5. Thiết lập cơ sở dữ liệu
1. Tạo database MySQL:
```sql
CREATE DATABASE phone_store;
```

2. Chạy file SQL để tạo bảng và dữ liệu mẫu:
```bash
mysql -u root -p phone_store < database_setup.sql
```

3. Cập nhật thông tin kết nối trong `DB_connect.py`:
```python
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="phone_store"
    )
    return conn
```

### 6. Chạy ứng dụng
```bash
python app.py
```

Truy cập: http://localhost:5000

## Cấu trúc dự án

```
MyFlaskApp_advance/
├── app.py                 # File chính chứa routes và logic
├── DB_connect.py          # Kết nối cơ sở dữ liệu
├── database_setup.sql     # Script tạo database và dữ liệu mẫu
├── requirements.txt       # Dependencies
├── static/
│   ├── images/           # Thư mục chứa hình ảnh sản phẩm
│   └── style.css         # CSS tùy chỉnh
└── templates/
    ├── base.html         # Template cơ sở
    ├── index.html        # Trang chủ
    ├── product_detail.html # Chi tiết sản phẩm
    ├── cart.html         # Giỏ hàng
    ├── search.html       # Tìm kiếm
    ├── admin_products.html # Quản lý sản phẩm
    ├── add_product.html  # Thêm sản phẩm
    └── edit_product.html # Chỉnh sửa sản phẩm
```

## Cấu trúc Database

### Bảng `categories`
- `id`: Khóa chính
- `name`: Tên danh mục
- `description`: Mô tả danh mục
- `created_at`: Thời gian tạo

### Bảng `products`
- `id`: Khóa chính
- `name`: Tên sản phẩm
- `description`: Mô tả sản phẩm
- `price`: Giá bán
- `stock`: Số lượng tồn kho
- `category_id`: ID danh mục (khóa ngoại)
- `brand`: Thương hiệu
- `model`: Model
- `color`: Màu sắc
- `storage`: Dung lượng lưu trữ
- `image`: Đường dẫn hình ảnh
- `status`: Trạng thái (active/inactive)
- `created_at`: Thời gian tạo
- `updated_at`: Thời gian cập nhật

### Bảng `orders` (cho tương lai)
- `id`: Khóa chính
- `customer_name`: Tên khách hàng
- `customer_email`: Email khách hàng
- `customer_phone`: Số điện thoại
- `customer_address`: Địa chỉ
- `total_amount`: Tổng tiền
- `status`: Trạng thái đơn hàng
- `created_at`: Thời gian tạo

### Bảng `order_items` (cho tương lai)
- `id`: Khóa chính
- `order_id`: ID đơn hàng (khóa ngoại)
- `product_id`: ID sản phẩm (khóa ngoại)
- `quantity`: Số lượng
- `price`: Giá tại thời điểm mua

## Sử dụng

### Trang chủ
- Hiển thị danh sách sản phẩm nổi bật
- Tìm kiếm sản phẩm theo tên, thương hiệu
- Lọc theo danh mục

### Chi tiết sản phẩm
- Xem thông tin chi tiết sản phẩm
- Thêm vào giỏ hàng
- Xem sản phẩm liên quan

### Giỏ hàng
- Xem danh sách sản phẩm đã chọn
- Cập nhật số lượng
- Xóa sản phẩm
- Tính tổng tiền

### Quản lý sản phẩm (Admin)
- Truy cập: `/admin/products`
- Thêm sản phẩm mới
- Chỉnh sửa thông tin sản phẩm
- Xóa sản phẩm (chuyển sang trạng thái inactive)
- Xem thống kê

## Tùy chỉnh

### Thêm danh mục mới
Chạy SQL:
```sql
INSERT INTO categories (name, description) VALUES ('Tên danh mục', 'Mô tả');
```

### Thay đổi giao diện
Chỉnh sửa file `static/style.css` hoặc các template trong thư mục `templates/`

### Thêm tính năng mới
1. Thêm route trong `app.py`
2. Tạo template tương ứng
3. Cập nhật database nếu cần

## Troubleshooting

### Lỗi kết nối database
- Kiểm tra thông tin kết nối trong `DB_connect.py`
- Đảm bảo MySQL đang chạy
- Kiểm tra database `phone_store` đã được tạo

### Lỗi upload hình ảnh
- Kiểm tra quyền ghi trong thư mục `static/images/`
- Đảm bảo file ảnh không quá 16MB

### Lỗi hiển thị
- Kiểm tra đường dẫn hình ảnh
- Xóa cache trình duyệt
- Kiểm tra console để xem lỗi JavaScript

## Phát triển tiếp

### Tính năng có thể thêm:
- [ ] Đăng nhập/đăng ký người dùng
- [ ] Hệ thống đánh giá sản phẩm
- [ ] Thanh toán online
- [ ] Quản lý đơn hàng
- [ ] API REST
- [ ] Tìm kiếm nâng cao
- [ ] So sánh sản phẩm
- [ ] Wishlist
- [ ] Newsletter

## License

MIT License

## Tác giả

Phát triển bởi: [Tên tác giả]
Email: [email@example.com]

