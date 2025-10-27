# PhoneStore - Trang web bán điện thoại

## Tính năng

### Cho khách hàng:
- ✅ Trang chủ hiển thị sản phẩm nổi bật
- ✅ Tìm kiếm và lọc sản phẩm theo danh mục
- ✅ Xem chi tiết sản phẩm
- ✅ Giỏ hàng (thêm, sửa, xóa sản phẩm)
- ✅ Đặt Hàng 

### Cho quản trị viên:
- ✅ Quản lý sản phẩm (thêm, sửa, xóa)
- ✅ Quản lý danh mục sản phẩm
- ✅ Upload hình ảnh sản phẩm
- ✅ Thống kê sản phẩm


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


Email: [tonguyen191224@gmail.com]

