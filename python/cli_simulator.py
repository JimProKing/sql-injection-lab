#!/usr/bin/env python3
"""
SQL Injection Lab - Command Line Simulator
No web server needed. Great for quick experiments and understanding query construction.
"""
import sqlite3
import os

DB_PATH = "sqli_lab.db"

def init_if_needed():
    if not os.path.exists(DB_PATH):
        print("[!] DB not found. Running db_init.py first...")
        import db_init
        db_init.init_db()

def show_query_and_result(query, params=None):
    print("\n" + "="*70)
    print("실행될 쿼리:")
    print(query)
    if params:
        print(f"파라미터: {params}")
    print("="*70)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        if params:
            rows = conn.execute(query, params).fetchall()
        else:
            rows = conn.execute(query).fetchall()

        print(f"\n결과 행 수: {len(rows)}")
        for i, row in enumerate(rows, 1):
            print(f"  [{i}] {dict(row)}")
    except Exception as e:
        print(f"\n[에러 발생] {e}")
    finally:
        conn.close()

def demo_login():
    print("\n=== [1] 로그인 취약점 시뫄레이션 ===")
    print("VULNERABLE 코드:")
    print("  query = f\"SELECT * FROM users WHERE username='{u}' AND password='{p}'\"")
    print("  db.execute(query)   # <-- 직접 문자열 연결!\n")

    while True:
        u = input("Username (or 'quit'): ").strip()
        if u.lower() == 'quit':
            break
        p = input("Password: ").strip()

        # Vulnerable construction
        query = f"SELECT * FROM users WHERE username = '{u}' AND password = '{p}'"
        show_query_and_result(query)

        print("\n[공격 예시 입력]")
        print("  admin' -- ")
        print("  admin' OR '1'='1' -- ")
        print("  ' OR 1=1 -- ")

def demo_union():
    print("\n=== [2] UNION 기반 데이터 추출 시뫄레이션 ===")
    print("\uc6d0래 쿼리: SELECT id, name, price, description FROM products WHERE name LIKE '%...%'")

    keyword = input("\n검색어 입력 (예: %' UNION SELECT ... -- ): ").strip()
    query = f"SELECT id, name, price, description FROM products WHERE name LIKE '%{keyword}%' OR description LIKE '%{keyword}%'"
    show_query_and_result(query)

def demo_boolean_blind():
    print("\n=== [3] Boolean Blind 시뫄레이션 ===")
    print("\uc6d0래 쿼리: SELECT * FROM users WHERE id = <\uc785력값>")

    while True:
        uid = input("\nID 조건 입력 (예: 1 AND 1=1): ").strip()
        if not uid:
            break
        query = f"SELECT id, username, role FROM users WHERE id = {uid}"
        show_query_and_result(query)

def main():
    init_if_needed()
    print("SQL Injection CLI Simulator")
    print("DB:", DB_PATH)
    print("\n\uba54뉴:")
    print("  1. 로그인 (인증 우회)")
    print("  2. UNION 검색")
    print("  3. Boolean Blind (id 파라미터)")
    print("  4. 전체 사용자 덤프 (안전한 쿼리)")
    print("  q. 종료")

    while True:
        choice = input("\n선택: ").strip().lower()
        if choice == '1':
            demo_login()
        elif choice == '2':
            demo_union()
        elif choice == '3':
            demo_boolean_blind()
        elif choice == '4':
            show_query_and_result("SELECT id, username, role, secret_note FROM users")
        elif choice == 'q':
            break
        else:
            print("1, 2, 3, 4, q 중 선택")

if __name__ == "__main__":
    main()