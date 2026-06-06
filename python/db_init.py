#!/usr/bin/env python3
"""
SQL Injection Lab - Database Initialization
Run this once to create the practice database with sample data.
"""
import sqlite3
import os

DB_PATH = "sqli_lab.db"

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"[*] Removed existing {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Users table - classic target
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            secret_note TEXT
        )
    ''')

    # Products table - for UNION and search examples
    c.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT,
            stock INTEGER DEFAULT 0
        )
    ''')

    # Comments table - for second-order SQLi demo
    c.execute('''
        CREATE TABLE comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Sample users
    users = [
        (1, 'admin', 's3cr3tP@ssw0rd!', 'admin@crehacktive.com', 'admin', 'FLAG{this_is_the_admin_secret_note_2026}'),
        (2, 'crehacktive', 'P@ssw0rd123', 'cre@crehacktive.com', 'user', 'My favorite color is blue'),
        (3, 'guest', 'guest123', 'guest@example.com', 'user', 'Just a regular user'),
        (4, 'developer', 'dev2026!', 'dev@company.com', 'user', 'Remember to rotate the DB password every 90 days'),
    ]
    c.executemany('INSERT INTO users (id, username, password, email, role, secret_note) VALUES (?,?,?,?,?,?)', users)

    # Sample products
    products = [
        (1, 'Wireless Mouse', 25000, '고성능 무선 마우스, 2.4GHz', 120),
        (2, 'Mechanical Keyboard', 89000, '청축 기계식 키보드, RGB 백라이트', 45),
        (3, 'USB-C Hub', 32000, '7-in-1 USB 허브 (HDMI 포함)', 200),
        (4, '27인치 모니터', 320000, 'QHD IPS 패널, 144Hz', 30),
        (5, '노트북 스탠드', 18000, '알루미늄 접이식 스탠드', 85),
    ]
    c.executemany('INSERT INTO products (id, name, price, description, stock) VALUES (?,?,?,?,?)', products)

    # Sample comments (for second order demo)
    comments = [
        ('user1', '이 키보드 정말 좋네요!'),
        ('hacker', "'); DROP TABLE users; --"),  # malicious comment for second-order demo
        ('tester', '배송이 빠르았습니다'),
    ]
    c.executemany('INSERT INTO comments (author, content) VALUES (?,?)', comments)

    conn.commit()
    conn.close()
    print(f"[+] Database initialized: {DB_PATH}")
    print("[+] Tables: users, products, comments")
    print("[+] Sample accounts:")
    print("    admin / s3cr3tP@ssw0rd!  (admin)")
    print("    crehacktive / P@ssw0rd123")
    print("    guest / guest123")

if __name__ == "__main__":
    init_db()