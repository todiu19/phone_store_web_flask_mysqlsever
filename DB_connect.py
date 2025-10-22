# Kết nối MySQL cho trang web bán điện thoại
import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",      # máy local
        user="root",           # user của MySQL
        password="Tonguyen24@",  # thay bằng mật khẩu thật
        database="phone_store"  # tên database mới cho trang web bán điện thoại
    )
    return conn
