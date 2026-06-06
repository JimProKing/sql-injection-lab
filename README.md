# SQL Injection 실습 랩

**직접 공격해보고, 방어 방법을 비교하며 배우는 SQL 인젝션 교육 자료**

한국어로 작성된 실습 중심의 SQL Injection 학습 랩입니다.

---

## 🚀 빠르게 시작하기

| 방법 | 설명 | 링크/위치 |
|------|------|----------|
| **가장 쉬움** | 설치 없이 브라우저에서 바로 실습 | `browser-simulator.html` |
| **강력 추천** | Python으로 실제 DB에 공격하기 | `python/vulnerable_app.py` |
| Tomcat 환경 | JSP + JDBC 실습 | `jsp/` 폴더 |

자세한 시작 방법은 **[START_HERE.md](START_HERE.md)** 를 열어보세요.

---

## 이 자료에서 배울 수 있는 것

- Classic 인증 우회 (`' OR 1=1 --`)
- UNION SELECT를 이용한 데이터 추출
- Boolean-based / Time-based Blind SQL Injection
- Second Order SQL Injection
- **취약한 코드 vs 안전한 코드** 직접 비교 (PreparedStatement)

---

## 저장소 구조

```
sql-injection-lab/
├── browser-simulator.html     # 설치 없이 바로 하는 시뮬레이터
├── START_HERE.md              # 처음 보는 사람을 위한 가이드
├── payloads-cheatsheet.md     # 주요 공격 페이로드 모음
├── python/
│   ├── vulnerable_app.py      # ← 여기서 실제 공격 연습
│   └── secure_app.py          # 안전한 버전
└── jsp/
    ├── vuln-*.jsp             # 취약한 JSP 예제
    └── secure-*.jsp           # PreparedStatement 적용 예제
```

---

## 주의사항

> **이 자료는 교육 목적으로만 만들어졌습니다.**
> 실제 서비스나 허가받지 않은 시스템에는 절대 사용하지 마세요.

---

## 상세 가이드

아래는 기존 상세 설명입니다.

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
- **Boolean-based**: 참/거짓에 따라 페이지 응답이 달라짐
- **Time-based**: `SLEEP(3)`, `BENCHMARK()` 등으로 응답 시간을 이용

### 2.3 Second-order SQLi
- 입력 시점에는 공격이 일어나지 않음
- 나중에 그 값이 다른 쿼리에 사용될 때 공격 발동

---

## 3. 실습 환경 구성

### 방법 A: Python Flask + SQLite (가장 추천)

```powershell
cd python
python db_init.py
python vulnerable_app.py
```

### 방법 B: JSP + MySQL
`db_setup_mysql.sql` 실행 후 `jsp/` 폴더의 파일들을 사용하세요.

### 방법 C: 브라우저 시뮬레이터
`browser-simulator.html`을 그대로 열어보세요.

---

## 5. 방어 방법 (가장 중요)

**최선의 방어는 PreparedStatement**입니다.

```java
// 나쁨 (절대 이렇게 하지 마세요)
String sql = "SELECT * FROM users WHERE id = " + id;

// 좋음
String sql = "SELECT * FROM users WHERE id = ?";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setInt(1, id);
```

---

**이 실습 자료는 교육 목적으로만 사용하세요.**