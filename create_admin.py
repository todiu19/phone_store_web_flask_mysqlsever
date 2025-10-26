#!/usr/bin/env python3
"""
Script để tạo admin user với password đã hash
"""
from werkzeug.security import generate_password_hash
from DB_connect import get_db_connection

def create_admin_user():
    # Tạo password hash cho admin
    admin_password = "admin123"  
    user_password = "user123"    

    admin_hash = generate_password_hash(admin_password)
    user_hash = generate_password_hash(user_password)
    
    print(f"Admin password hash: {admin_hash}")
    print(f"User password hash: {user_hash}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE users SET password = %s WHERE username = 'admin'", (admin_hash,))
        cursor.execute("UPDATE users SET password = %s WHERE username = 'user1'", (user_hash,))
        
        conn.commit()
        print("Đã cập nhật password thành công!")
        print("Admin login: admin / admin123")
        print("User login: user1 / user123")
        
    except Exception as e:
        print(f"Lỗi: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_admin_user()
