# SQL Injection Lab - 시작 가이드

## 가장 빠르게 시작하는 방법 (추천 순서)

### 방법 1: 브라우서만 사용 (30초 커트)

1. `browser-simulator.html` 파일을 더블클릭해서 브라우저에서 열기
2. 로그인 우회, UNION 페이로드, Boolean 자동 추출 등을 바로 체험

### 방법 2: Python으로 제대로 실습 (가장 추천)

**PowerShell에서 실행:**

```powershell
cd C:\tomcat\webapps\ROOT\sqli-lab\python

# 1. DB 만들기 (처음 한 번만)
python db_init.py

# 2. 취약한 앱 실행
python vulnerable_app.py
```

브라우저에서 http://127.0.0.1:5000 열기

**Secure 버전과 동시에 비교하고 싶다면** (다른 터미널에서):
```powershell
python secure_app.py
```
→ http://127.0.0.1:5001

### 방법 3: Tomcat + JSP + MySQL

1. MySQL에서 DB 생성
   ```powershell
   cd C:\tomcat\webapps\ROOT\sqli-lab
   mysql -u root -p < db_setup_mysql.sql
   ```

2. MySQL JDBC 드라이버를 Tomcat `lib` 폴더에 복사 (아직 안 되어 있다면)

3. `jsp` 폴더 안 파일들을 `C:\tomcat\webapps\ROOT\sqli\` 로 복사

4. Tomcat 재시작 후 접속:
   - http://localhost:8080/sqli/vuln-login.jsp
   - http://localhost:8080/sqli/vuln-search.jsp

---

## 학습 로드맵

1. `browser-simulator.html` 로 개념 파악 (10분)
2. Python vulnerable_app.py 실행하고 로그인 우회 성공시키기
3. UNION으로 users 테이블 전체 덤프하기
4. Boolean Blind로 admin 비밀번호 일부 추출하기
5. `secure_app.py`와 비교하면서 왜 안전한지 확인
6. `README.md` 읽으면서 이론 정리
7. `payloads-cheatsheet.md` 보면서 더 많은 페이로드 연습
8. (선택) JSP 버전으로 실제 JDBC 환경에서도 같은 공격 재현

---

## 파일 설명

| 파일 | 설명 |
|------|------|
| `index.html` | 이 랩의 네비게이션 |
| `browser-simulator.html` | 설치 없이 바로 하는 인터랙티브 시뫄레이터 |
| `README.md` | 상세 이론 + 방어 방법 + 실습 가이드 |
| `payloads-cheatsheet.md` | 공격 페이로드 모음 |
| `python/vulnerable_app.py` | 실제로 동작하는 취약한 Flask 앱 |
| `python/secure_app.py` | PreparedStatement로 안전하게 만든 버전 |
| `python/cli_simulator.py` | 웹 없이 명령줄로 빠르게 테스트 |
| `jsp/*.jsp` | Tomcat/JDBC 환경용 예제 (vuln + secure) |
| `db_setup_mysql.sql` | MySQL용 테이블+데이터 생성 스크립트 |

---

**\uacbd고**: 이 모든 예제는 **\uad50육 목적**\uc73c로 의도적으로 취약하게 만들어졌습니다.
실제 서뱄스나 본인 소유가 아닌 시스템에는 절대 사용하지 마세요.