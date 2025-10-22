create database cardDB
use cardDB
CREATE TABLE Students (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100),
    age INT
);
select * from products

CREATE TABLE Products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100),
    price DECIMAL(10,2),
	image_url NVARCHAR(255) 
);

delete from Products

CREATE TABLE Cart (
    id INT IDENTITY(1,1) PRIMARY KEY,
    student_id INT,
    product_id INT,
    quantity INT,
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
);
delete from cart
