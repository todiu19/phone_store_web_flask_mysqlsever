# Trang web bán điện thoại sử dụng Flask và MySQL
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from DB_connect import get_db_connection
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Cần thiết cho session

# Thư mục chứa ảnh upload
UPLOAD_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Khởi tạo giỏ hàng trong session
def init_cart():
    if 'cart' not in session:
        session['cart'] = {}

# ===============================
# TRANG CHỦ - DANH SÁCH ĐIỆN THOẠI
# ===============================
@app.route('/')
def index():
    init_cart()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Lấy danh sách điện thoại với thông tin chi tiết
    cursor.execute("""
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE p.status = 'active'
        ORDER BY p.created_at DESC
    """)
    phones = cursor.fetchall()
    
    # Lấy danh sách danh mục
    cursor.execute("SELECT * FROM categories ORDER BY name")
    categories = cursor.fetchall()
    
    conn.close()
    return render_template('index.html', phones=phones, categories=categories)

# ===============================
# TRANG CHI TIẾT SẢN PHẨM
# ===============================
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    init_cart()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE p.id = %s AND p.status = 'active'
    """, (product_id,))
    product = cursor.fetchone()
    
    if not product:
        flash('Sản phẩm không tồn tại!', 'error')
        return redirect(url_for('index'))
    
    # Lấy sản phẩm liên quan
    cursor.execute("""
        SELECT * FROM products 
        WHERE category_id = %s AND id != %s AND status = 'active'
        LIMIT 4
    """, (product['category_id'], product_id))
    related_products = cursor.fetchall()
    
    conn.close()
    return render_template('product_detail.html', product=product, related_products=related_products)

# ===============================
# THÊM VÀO GIỎ HÀNG
# ===============================
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    init_cart()
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s AND status = 'active'", (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    if not product:
        return jsonify({'success': False, 'message': 'Sản phẩm không tồn tại!'})
    
    if product_id in session['cart']:
        session['cart'][product_id] += quantity
    else:
        session['cart'][product_id] = quantity
    
    session.modified = True
    return jsonify({'success': True, 'message': 'Đã thêm vào giỏ hàng!'})

# ===============================
# XEM GIỎ HÀNG
# ===============================
@app.route('/cart')
def cart():
    init_cart()
    cart_items = []
    total = 0
    
    if session['cart']:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        for product_id, quantity in session['cart'].items():
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            if product:
                product['quantity'] = quantity
                product['subtotal'] = product['price'] * quantity
                cart_items.append(product)
                total += product['subtotal']
        
        conn.close()
    
    return render_template('cart.html', cart_items=cart_items, total=total)

# ===============================
# CẬP NHẬT GIỎ HÀNG
# ===============================
@app.route('/update_cart', methods=['POST'])
def update_cart():
    init_cart()
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 0))
    
    if quantity <= 0:
        session['cart'].pop(product_id, None)
    else:
        session['cart'][product_id] = quantity
    
    session.modified = True
    return redirect(url_for('cart'))

# ===============================
# XÓA SẢN PHẨM KHỎI GIỎ HÀNG
# ===============================
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    init_cart()
    session['cart'].pop(str(product_id), None)
    session.modified = True
    return redirect(url_for('cart'))

# ===============================
# TRANG QUẢN LÝ SẢN PHẨM
# ===============================
@app.route('/admin/products')
def admin_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        ORDER BY p.created_at DESC
    """)
    products = cursor.fetchall()
    conn.close()
    return render_template('admin_products.html', products=products)

# ===============================
# THÊM SẢN PHẨM MỚI
# ===============================
@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        category_id = int(request.form['category_id'])
        brand = request.form['brand']
        model = request.form['model']
        color = request.form['color']
        storage = request.form['storage']
        
        # Xử lý upload ảnh
        image = request.files['image']
        if image and image.filename:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = f'images/{filename}'
        else:
            image_url = 'images/default_phone.png'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, description, price, stock, category_id, brand, model, color, storage, image, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'active')
        """, (name, description, price, stock, category_id, brand, model, color, storage, image_url))
        conn.commit()
        conn.close()
        
        flash('Thêm sản phẩm thành công!', 'success')
        return redirect(url_for('admin_products'))
    
    # Lấy danh sách danh mục
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories ORDER BY name")
    categories = cursor.fetchall()
    conn.close()
    
    return render_template('add_product.html', categories=categories)

# ===============================
# SỬA SẢN PHẨM
# ===============================
@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        category_id = int(request.form['category_id'])
        brand = request.form['brand']
        model = request.form['model']
        color = request.form['color']
        storage = request.form['storage']
        status = request.form['status']
        
        # Xử lý upload ảnh mới
        image = request.files['image']
        if image and image.filename:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = f'images/{filename}'
        else:
            # Giữ ảnh cũ
            cursor.execute("SELECT image FROM products WHERE id = %s", (product_id,))
            old_product = cursor.fetchone()
            image_url = old_product['image']
        
        cursor.execute("""
            UPDATE products 
            SET name=%s, description=%s, price=%s, stock=%s, category_id=%s, 
                brand=%s, model=%s, color=%s, storage=%s, image=%s, status=%s
            WHERE id=%s
        """, (name, description, price, stock, category_id, brand, model, color, storage, image_url, status, product_id))
        
        conn.commit()
        conn.close()
        flash('Cập nhật sản phẩm thành công!', 'success')
        return redirect(url_for('admin_products'))
    
    # Lấy thông tin sản phẩm và danh mục
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    
    cursor.execute("SELECT * FROM categories ORDER BY name")
    categories = cursor.fetchall()
    
    conn.close()
    return render_template('edit_product.html', product=product, categories=categories)

# ===============================
# XÓA SẢN PHẨM
# ===============================
@app.route('/admin/delete_product/<int:product_id>')
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET status = 'inactive' WHERE id = %s", (product_id,))
    conn.commit()
    conn.close()
    flash('Xóa sản phẩm thành công!', 'success')
    return redirect(url_for('admin_products'))

# ===============================
# TÌM KIẾM SẢN PHẨM
# ===============================
@app.route('/search')
def search():
    init_cart()
    query = request.args.get('q', '')
    category_id = request.args.get('category', '')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    sql = """
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE p.status = 'active'
    """
    params = []
    
    if query:
        sql += " AND (p.name LIKE %s OR p.brand LIKE %s OR p.model LIKE %s)"
        params.extend([f'%{query}%', f'%{query}%', f'%{query}%'])
    
    if category_id:
        sql += " AND p.category_id = %s"
        params.append(category_id)
    
    sql += " ORDER BY p.created_at DESC"
    
    cursor.execute(sql, params)
    phones = cursor.fetchall()
    
    # Lấy danh sách danh mục
    cursor.execute("SELECT * FROM categories ORDER BY name")
    categories = cursor.fetchall()
    
    conn.close()
    return render_template('search.html', phones=phones, categories=categories, query=query, selected_category=category_id)

if __name__ == '__main__':
    app.run(debug=True)