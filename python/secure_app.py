#!/usr/bin/env python3
"""
SQL Injection Lab - SECURE VERSION (using parameterized queries)

This is the correct way to build database queries.
Compare this with vulnerable_app.py to understand the difference.
"""
from flask import Flask, request, render_template_string, g
import sqlite3

app = Flask(__name__)
DB_PATH = "sqli_lab.db"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template_string('''
    <!doctype html>
    <html>
    <head><meta charset="utf-8"><title>SQLi Lab - SECURE</title></head>
    <body style="font-family:monospace; max-width:900px; margin:40px auto; line-height:1.6">
        <h1>🔒 SQL Injection Lab (SECURE VERSION)</h1>
        <p style="color:#0a0"><strong>이 버전은 안전하게 작성되었습니다. (Parameterized Queries)</strong></p>
        
        <h2>메뉴 (모두 안전하게 처리됨)</h2>
        <ul>
            <li><a href="/login">로그인</a></li>
            <li><a href="/search">상품 검색</a></li>
            <li><a href="/user?id=1">사용자 정보</a></li>
        </ul>

        <h2>핵심 방어 코드</h2>
        <pre style="background:#f0f0f0;padding:15px">
// VULNERABLE (절대 이렇게 하지 마세요)
query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
db.execute(query)

// SECURE (항상 이렇게 하세요)
query = "SELECT * FROM users WHERE username = ? AND password = ?"
db.execute(query, (username, password))
        </pre>

        <p>모든 입력값은 <strong>쿼리 구조와 분리</strong>되어 전달됩니다. 공격자가 입력한 따옴표, OR, UNION 등이 데이터로만 취급됩니다.</p>
        <p><a href="http://127.0.0.1:5000">Vulnerable 버전으로 이동</a></p>
    </body>
    </html>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    result = ""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # SECURE: Parameterized query
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        db = get_db()
        cur = db.execute(query, (username, password))  # <-- SAFE
        user = cur.fetchone()

        if user:
            result = f"<h3 style='color:green'>로그인 성공 (Secure)</h3><p>Welcome {user['username']}</p>"
        else:
            result = "<h3 style='color:red'>로그인 실패</h3>"

    return render_template_string('''
    <h1>Secure Login</h1>
    <form method="post">
        Username: <input type="text" name="username"><br>
        Password: <input type="text" name="password"><br>
        <input type="submit" value="Login">
    </form>
    {{ result|safe }}
    <p><a href="/">홈</a></p>
    ''', result=result)

@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    result_html = ""

    if keyword:
        # SECURE
        query = "SELECT id, name, price, description FROM products WHERE name LIKE ? OR description LIKE ?"
        like_pattern = f"%{keyword}%"
        db = get_db()
        rows = db.execute(query, (like_pattern, like_pattern)).fetchall()

        if rows:
            result_html = "<table border=1 cellpadding=8><tr><th>ID</th><th>Name</th><th>Price</th></tr>"
            for r in rows:
                result_html += f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['price']}</td></tr>"
            result_html += "</table>"
        else:
            result_html = "<p>결과 없음</p>"

    return render_template_string('''
    <h1>Secure Search</h1>
    <form><input type="text" name="q" value="{{ keyword }}"> <input type="submit" value="검색"></form>
    {{ result_html|safe }}
    <p style="color:#0a0">UNION 공격이 더 이상 동작하지 않습니다.</p>
    <p><a href="/">홈</a></p>
    ''', keyword=keyword, result_html=result_html)

@app.route('/user')
def user_detail():
    user_id = request.args.get('id', '1')
    # SECURE: Use parameter even for integer (still pass as string, driver handles it)
    query = "SELECT id, username, email, role FROM users WHERE id = ?"
    db = get_db()
    row = db.execute(query, (user_id,)).fetchone()

    if row:
        result = f"<p>Username: {row['username']} / Role: {row['role']}</p>"
    else:
        result = "<p>사용자 없음</p>"

    return render_template_string('''
    <h1>Secure User Detail</h1>
    <form>ID: <input type="text" name="id" value="{{ user_id }}"> <input type="submit"></form>
    {{ result|safe }}
    <p><a href="/">홈</a></p>
    ''', user_id=user_id, result=result)

if __name__ == '__main__':
    print("[*] Starting SECURE version on http://127.0.0.1:5001")
    app.run(debug=True, port=5001)