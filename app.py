# Trang web bán điện thoại sử dụng Flask và MySQL
from operator import truediv
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from DB_connect import get_db_connection
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'Tonguyen24@'  # Cần thiết cho session

UPLOAD_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def init_cart():
    if 'cart' not in session:
        session['cart'] = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập để truy cập trang này!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập để truy cập trang này!', 'error')
            return redirect(url_for('login'))
        if session.get('user_role') != 'admin':
            flash('Bạn không có quyền truy cập trang này!', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ===============================
# TRANG CHỦ - DANH SÁCH ĐIỆN THOẠI
# ===============================
@app.route('/')
def index():
    init_cart()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE p.status = 'active'
        ORDER BY p.created_at DESC
    """)
    phones = cursor.fetchall()
    
    cursor.execute("SELECT * FROM categories ORDER BY name")
    categories = cursor.fetchall()
    
    conn.close()
    return render_template('index.html', phones=phones, categories=categories)
# =================================
# Số lượng sản phẩm trong giỏ hàng
# =================================
@app.context_processor
def inject_cart_count():
    count = 0
    if 'user_id' in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT SUM(quantity)
                        FROM cart_items 
                        WHERE user_id = %s
                        """,(session['user_id'],))
        count = cursor.fetchone()['SUM(quantity)'] or 0
        conn.close()
    elif 'cart' in session:
        count = sum(session['cart'].values())
    return dict(cart_count = count)

# ===============================
# ĐĂNG NHẬP
# ===============================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['user_role'] = user['role']
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')

    return render_template('login.html')

# ===============================
# ĐĂNG KÝ
# ===============================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp!', 'error')
            return render_template('register.html')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Kiểm tra username đã tồn tại
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            flash('Tên đăng nhập đã tồn tại!', 'error')
            conn.close()
            return render_template('register.html')
        
        # Kiểm tra email đã tồn tại
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            flash('Email đã tồn tại!', 'error')
            conn.close()
            return render_template('register.html')
        
        # Tạo user mới
        hashed_password = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO users (username, email, password, role) 
            VALUES (%s, %s, %s, 'user')
        """, (username, email, hashed_password))
        conn.commit()
        conn.close()
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# ===============================
# ĐĂNG XUẤT
# ===============================
@app.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('index'))

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
#ddaas them hang vao db
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if 'user_id' in session:
        cursor.execute("""INSERT INTO cart_items(user_id,product_id,quantity)
        VALUES(%s,%s,%s) 
        ON DUPLICATE KEY UPDATE 
            quantity = quantity + VALUES(quantity)
        """,(session['user_id'],product_id,quantity))
        conn.commit()
        #cap nhat lại so luong sp trong gio hang
        cursor.execute("SELECT SUM(quantity) AS total FROM cart_items WHERE user_id = %s", (session['user_id'],))
        count = cursor.fetchone()['total'] or 0 

    else:
        init_cart()
        cursor.execute("SELECT * FROM products WHERE id = %s AND status = 'active'", (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({'success': False, 'message': 'Sản phẩm không tồn tại!'})
        if product_id in session['cart']:
            session['cart'][product_id] += quantity
        else:
            session['cart'][product_id] = quantity
        session.modified = True
        #cap nhat lại so luong sp trong gio hang
        count = sum(session['cart'].values())
   
    conn.close()
    
    return jsonify({'success': True, 'message': 'Đã thêm vào giỏ hàng!','cart_count':count})

# ===============================
# XEM GIỎ HÀNG
# ===============================
#xem gio hang tu db
@app.route('/cart')
def cart():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cart_items=[]
    total = 0
    if 'user_id' in session:
        user_id = session['user_id']
        cursor.execute("""SELECT  *
                       FROM cart_items c 
                       JOIN products p ON  c.product_id = p.id
                       WHERE c.user_id = %s    
                        """,(user_id,))
        cart_items = cursor.fetchall()
        for item in cart_items:
            item['subtotal'] = item['price']*item['quantity']
            total+= item['subtotal'] 
    else:
        init_cart()
        if 'cart' in session:
            for id,quantity in session['cart'].items():
                cursor.execute("SELECT * FROM products WHERE id = %s",(id,))
                product = cursor.fetchone()
                if product:
                    product['quantity'] = quantity
                    product['subtotal'] = product['price']*quantity
                    cart_items.append(product)
                    total += product['subtotal']
    conn.close()
    return render_template('cart.html', cart_items=cart_items, total=total)

# ===============================
# CẬP NHẬT GIỎ HÀNG
# ===============================
#update quantity cho db and session
@app.route('/update_cart', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 0))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if 'user_id' in session:
        if quantity <= 0:
            cursor.execute("""DELETE FROM cart_items 
                            WHERE user_id = %s AND product_id = %s
                            """,(session['user_id'],product_id,))
        else :
            cursor.execute("""UPDATE cart_items 
                            SET quantity = %s 
                            WHERE user_id = %s AND product_id = %s
                            """,(quantity,session['user_id'],product_id,))
        conn.commit()
        conn.close()
    else:
        init_cart()
        if quantity <= 0:
            session['cart'].pop(product_id, None)
        else:
            session['cart'][product_id] = quantity
        session.modified = True
    return redirect(url_for('cart'))

# ===============================
# XÓA SẢN PHẨM KHỎI GIỎ HÀNG
# ===============================
#xoa khoi db
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'user_id' in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""DELETE FROM cart_items WHERE product_id = %s AND user_id = %s
                        """,(product_id,session['user_id'],))
        conn.commit()
        conn.close()
    else:
        init_cart()
        session['cart'].pop(str(product_id), None)
        session.modified = True
    return redirect(url_for('cart'))

# ===============================
# Xác nhận đặt hàng
# ===============================     
#          
@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        flash("Vui lòng đăng nhập để đặt hàng.")
        return redirect(url_for('login'))
    return render_template('checkout.html')

#===============================
# THÊM VÀO GIỎ HOÁ ĐƠN 
# ===============================
@app.route('/add_to_orders',methods=['POST'])
def add_to_orders():
    user_id = session['user_id']
    name = request.form['fullname']
    address = request.form['address']
    phone = request.form['phone_number']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    cursor.execute("""SELECT email FROM users 
                    WHERE id = %s
                    """,(user_id,))
    user = cursor.fetchone()
    cursor.execute("""SELECT SUM(p.price * c.quantity) AS total
                    FROM cart_items c
                    JOIN products p ON c.product_id = p.id 
                    WHERE c.user_id = %s
                    """,(user_id,))
    total = cursor.fetchone()['total'] or 0
    
    #Them vao table orders (thong tin nguoi dat va total)
    cursor.execute("""INSERT INTO orders(customer_name,customer_email,customer_address,customer_phone,total_amount,user_id) 
                    VALUES(%s,%s,%s,%s,%s,%s)
                    """,(name,user['email'],address,phone,total,user_id,))
    order_id = cursor.lastrowid # get id cuar order vuawf insert
    #get infor to insert to ordoer_items(chi tiet don hang)
    cursor.execute("""SELECT c.product_id,c.quantity,p.price AS price
                    FROM cart_items c
                    JOIN products p ON c.product_id = p.id
                    WHERE user_id = %s
                    """,(user_id,))
    cart_items = cursor.fetchall()
    for item in cart_items:
        cursor.execute("""INSERT INTO order_items(order_id,product_id,quantity,price) 
                        VALUES(%s,%s,%s,%s)
                        """,(order_id,item['product_id'],item['quantity'],item['price'],))
    cursor.execute("""DELETE FROM cart_items 
                    WHERE user_id = %s
                    """,(user_id,))
    conn.commit()
    conn.close()
    flash("Đặt hàng thành công! Cảm ơn bạn đã mua hàng.")
    return redirect(url_for('index'))


# ===============================
# Xem Danh Sachs Đơn Hàng
# ===============================
@app.route('/orders')
def orders_list():
    if 'user_id' in session:
        user_id = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary = True)
        if session.get('user_role') == 'admin':
            cursor.execute("""SELECT * 
                            FROM orders 
                            ORDER BY created_at DESC
                            """)
        if session.get('user_role') == 'user':
            cursor.execute("""SELECT * 
                            FROM orders
                            WHERE user_id = %s
                            ORDER BY created_at DESC
                            """,(user_id,))
        orders = cursor.fetchall()
        conn.close()
        return render_template('orders.html',orders = orders)
    # chuaw login thif return login
    return redirect(url_for('login'))

# ===============================
# Xem Chi Tiết Đơn Hàng
# ===============================
@app.route('/order_detail/<int:order_id>',methods = ["GET"])
def order_detail(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary = True)
    cursor.execute("""SELECT c.quantity,p.price AS price , p.name AS product_name
                    FROM order_items c
                    JOIN products p ON c.product_id = p.id
                    WHERE order_id = %s
                    """,(order_id,))
    items = cursor.fetchall()

    cursor.execute("""SELECT * 
                    FROM orders
                    WHERE id = %s
                    """,(order_id,))
    order = cursor.fetchone()
    conn.close()
    return render_template('order_detail.html',items = items,order = order)



# ===============================
# TRANG QUẢN LÝ SẢN PHẨM
# ===============================
@app.route('/admin/products')
@admin_required
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
@admin_required
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
        cursor = conn.cursor(dictionary = True)
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
@admin_required
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
@admin_required
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
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