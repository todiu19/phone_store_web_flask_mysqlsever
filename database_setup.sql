
CREATE DATABASE IF NOT EXISTS phone_store;
USE phone_store;

-- Bảng danh mục sản phẩm
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng người dùng
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng sản phẩm (điện thoại)
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    category_id INT,
    brand VARCHAR(100),
    model VARCHAR(100),
    color VARCHAR(50),
    storage VARCHAR(50),
    image VARCHAR(255),
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
-- Gio hang
CREATE TABLE IF NOT EXISTS cart_items(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    product_id INT,
    quantity INT DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE (user_id, product_id)
);
-- Bảng đơn hàng
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(100),
    customer_phone VARCHAR(20),
    customer_address TEXT,
    total_amount DECIMAL(10,2) NOT NULL,
    user_id INT NOT NULL,
    status ENUM('pending', 'confirmed', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Bảng chi tiết đơn hàng
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);






-- Thêm dữ liệu mẫu cho danh mục
INSERT INTO categories (name, description) VALUES
('iPhone', 'Điện thoại iPhone của Apple'),
('Samsung', 'Điện thoại Samsung Galaxy'),
('Xiaomi', 'Điện thoại Xiaomi'),
('OPPO', 'Điện thoại OPPO'),
('Vivo', 'Điện thoại Vivo'),
('OnePlus', 'Điện thoại OnePlus'),
('Huawei', 'Điện thoại Huawei'),
('Realme', 'Điện thoại Realme');

-- Thêm dữ liệu mẫu cho người dùng (password sẽ được cập nhật bằng script)
INSERT INTO users (username, email, password, role) VALUES
('admin', 'admin@phonestore.com', 'temp_password', 'admin'),
('user1', 'user1@example.com', 'temp_password', 'user');

-- Thêm dữ liệu mẫu cho sản phẩm
INSERT INTO products (name, description, price, stock, category_id, brand, model, color, storage, image, status) VALUES
('iPhone 15 Pro Max', 'iPhone 15 Pro Max với chip A17 Pro mạnh mẽ, camera 48MP và màn hình Super Retina XDR 6.7 inch', 29990000, 50, 1, 'Apple', 'iPhone 15 Pro Max', 'Titanium Natural', '256GB', 'images/ip15.png', 'active'),
('Samsung Galaxy S24 Ultra', 'Samsung Galaxy S24 Ultra với S Pen, camera 200MP và màn hình Dynamic AMOLED 2X 6.8 inch', 25990000, 30, 2, 'Samsung', 'Galaxy S24 Ultra', 'Titanium Black', '512GB', 'images/s24_ultra.jpg', 'active'),
('Xiaomi 14 Pro', 'Xiaomi 14 Pro với Snapdragon 8 Gen 3, camera Leica 50MP và màn hình AMOLED 6.73 inch', 18990000, 40, 3, 'Xiaomi', '14 Pro', 'Black', '256GB', 'images/xiaomi14pro.jpg', 'active'),
('OPPO Find X7 Ultra', 'OPPO Find X7 Ultra với camera Hasselblad 50MP, Snapdragon 8 Gen 3 và màn hình LTPO AMOLED 6.82 inch', 21990000, 25, 4, 'OPPO', 'Find X7 Ultra', 'Ocean Blue', '512GB', 'images/oppo_find_x7.jpg', 'active'),
('Vivo X100 Pro', 'Vivo X100 Pro với camera ZEISS 50MP, MediaTek Dimensity 9300 và màn hình AMOLED 6.78 inch', 19990000, 35, 5, 'Vivo', 'X100 Pro', 'Sunset Orange', '256GB', 'images/vivo_x100.jpg', 'active'),
('OnePlus 12', 'OnePlus 12 với Snapdragon 8 Gen 3, camera Hasselblad 50MP và màn hình LTPO AMOLED 6.82 inch', 17990000, 20, 6, 'OnePlus', '12', 'Silky Black', '256GB', 'images/oneplus12.jpg', 'active'),
('Huawei P60 Pro', 'Huawei P60 Pro với camera XMAGE 48MP, Kirin 9000S và màn hình OLED 6.67 inch', 16990000, 15, 7, 'Huawei', 'P60 Pro', 'Rococo Pearl', '512GB', 'images/huawei_p60.jpg', 'active'),
('Realme GT5 Pro', 'Realme GT5 Pro với Snapdragon 8 Gen 3, camera Sony IMX890 50MP và màn hình AMOLED 6.78 inch', 12990000, 45, 8, 'Realme', 'GT5 Pro', 'White', '256GB', 'images/realme_gt5.jpg', 'active');
-- Them du lieu
INSERT INTO products 
(name, description, price, stock, category_id, brand, model, color, storage, image, status)
VALUES
-- APPLE
('iPhone 16 Pro Max', 'iPhone 16 Pro Max với chip A18 Pro, camera 48MP và màn hình Super Retina XDR 6.9 inch.', 34990000, 40, 1, 'Apple', 'iPhone 16 Pro Max', 'Titanium Silver', '512GB', 'images/iphone16promax.jpg', 'active'),

('Samsung Galaxy S25 Ultra', 'Galaxy S25 Ultra với camera 200MP, S Pen và màn hình Dynamic AMOLED 2X 6.8 inch.', 31990000, 35, 2, 'Samsung', 'Galaxy S25 Ultra', 'Titanium Gray', '512GB', 'images/galaxy_s25ultra.jpg', 'active'),

('Xiaomi 15 Pro', 'Xiaomi 15 Pro trang bị Snapdragon 8 Gen 4, camera Leica 50MP và sạc nhanh 120W.', 19990000, 45, 3, 'Xiaomi', '15 Pro', 'Graphite Black', '512GB', 'images/xiaomi15pro.jpg', 'active'),

('OPPO Find X8', 'OPPO Find X8 với camera Hasselblad 50MP, màn hình AMOLED 6.8 inch và sạc 100W.', 22990000, 25, 4, 'OPPO', 'Find X8', 'Ocean Blue', '256GB', 'images/oppo_findx8.jpg', 'active'),

('Vivo X200 Pro', 'Vivo X200 Pro dùng Dimensity 9400, camera ZEISS 50MP và pin 5000mAh sạc 120W.', 21990000, 30, 5, 'Vivo', 'X200 Pro', 'Sunset Gold', '512GB', 'images/vivo_x200pro.jpg', 'active'),

('OnePlus 13', 'OnePlus 13 trang bị Snapdragon 8 Gen 4, camera Hasselblad và màn hình LTPO AMOLED 6.82 inch.', 20990000, 28, 6, 'OnePlus', '13', 'Emerald Green', '512GB', 'images/oneplus13.jpg', 'active'),

('Huawei Mate 70 Pro', 'Huawei Mate 70 Pro với chip Kirin 9010, camera XMAGE và màn hình OLED cong 6.7 inch.', 25990000, 22, 7, 'Huawei', 'Mate 70 Pro', 'Rococo Pearl', '512GB', 'images/huawei_mate70pro.jpg', 'active'),

('Realme GT6 Pro', 'Realme GT6 Pro sử dụng Snapdragon 8 Gen 3, màn hình AMOLED 6.78 inch và pin 5500mAh.', 14990000, 40, 8, 'Realme', 'GT6 Pro', 'Lunar Silver', '256GB', 'images/realme_gt6pro.jpg', 'active'),

('iPhone 16', 'iPhone 16 bản tiêu chuẩn với chip A18 Bionic, camera kép và màn hình 6.1 inch.', 25990000, 50, 1, 'Apple', 'iPhone 16', 'Blue Titanium', '256GB', 'images/iphone16.jpg', 'active'),

('Samsung Galaxy Z Fold 6', 'Galaxy Z Fold 6 với thiết kế gập cải tiến, chip Snapdragon 8 Gen 3 và màn hình 7.6 inch.', 39990000, 18, 2, 'Samsung', 'Galaxy Z Fold 6', 'Phantom Black', '512GB', 'images/galaxy_zfold6.jpg', 'active');

-- Tạo index để tối ưu hiệu suất
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_brand ON products(brand);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);

