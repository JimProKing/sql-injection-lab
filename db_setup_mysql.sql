-- ============================================================
-- SQL Injection Lab - MySQL Database Setup
-- Run this in your MySQL server (or via any MySQL client)
-- ============================================================

DROP DATABASE IF EXISTS sqli_lab;
CREATE DATABASE sqli_lab CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sqli_lab;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    role ENUM('admin','user') DEFAULT 'user',
    secret_note TEXT
);

-- Products
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    description TEXT,
    stock INT DEFAULT 0
);

-- Comments (for second-order demo)
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    author VARCHAR(50),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample data
INSERT INTO users (username, password, email, role, secret_note) VALUES
('admin', 's3cr3tP@ssw0rd!', 'admin@crehacktive.com', 'admin', 'FLAG{this_is_the_real_admin_secret_from_mysql_2026}'),
('crehacktive', 'P@ssw0rd123', 'cre@crehacktive.com', 'user', 'My favorite color is blue'),
('guest', 'guest123', 'guest@example.com', 'user', 'I am just a guest'),
('developer', 'dev2026!', 'dev@company.com', 'user', 'DB password rotation policy: every 90 days');

INSERT INTO products (name, price, description, stock) VALUES
('Wireless Mouse', 25000, '고성능 2.4GHz 무선 맀우스', 120),
('Mechanical Keyboard', 89000, '청축 기계식 키보드 RGB', 45),
('USB-C Hub 7-in-1', 32000, 'HDMI, PD, USB3.0 지원', 200),
('27" QHD Monitor', 320000, 'IPS 144Hz', 30),
('Aluminum Laptop Stand', 18000, '접이식 노트북 받침대', 85);

INSERT INTO comments (author, content) VALUES
('user1', '키보드 타건감이 정말 좋습니다'),
('hacker', "'); DROP TABLE users; --"),
('tester', '배송 빠르고 포장도 깸깸했어요');

SELECT 'Database sqli_lab created successfully!' AS message;
SELECT 'Try connecting with the same credentials used in test.jsp' AS note;
SELECT 'Then copy the JSP files from sqli-lab/jsp/ into your Tomcat webapps/ROOT/sqli/' AS next_step;