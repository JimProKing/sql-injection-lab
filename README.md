# SQL Injection 실습

SQL 인젝션 공부하면서 직접 공격도 해보고 싶어서 만든 프로젝트예요.

Python Flask로 간단한 웹 앱을 하나 만들었고, 로그인이나 검색 같은 곳에 실제로 쿼리를 날리는 부분을 일부러 취약하게 짰습니다. 안전하게 짜는 방법(PreparedStatement)도 같이 넣어서 비교하면서 볼 수 있게 했어요.

JSP 버전도 있어서 Tomcat에서 MySQL 연결해서 테스트 해볼 수 있습니다.

## 어떻게 시작하나요?

제일 쉬운 건 browser-simulator.html 파일을 그냥 열어보는 거예요. 아무것도 설치 안 해도 바로 UNION이나 로그인 우회 테스트가 됩니다.

Python으로 제대로 실습하고 싶으면:

```powershell
cd python
python db_init.py
python vulnerable_app.py
```

http://127.0.0.1:5000 에서 열리면 로그인, 검색, 유저 조회 같은 페이지에서 페이로드를 넣어보세요.

secure_app.py 를 5001 포트로 띄워놓고 같이 보면 취약한 부분이 어디인지 바로 느껴집니다.

## 들어있는 내용

- 로그인 폼에서 admin' -- 같은 걸로 우회하기
- 검색에서 UNION SELECT 로 다른 테이블 데이터 가져오기
- id 값으로 Boolean blind, time based blind 테스트
- 댓글에 악성 쿼리를 저장해두고 나중에 실행되는 second order
- 그리고 PreparedStatement 로 제대로 막은 버전

payloads-cheatsheet.md 에 자주 쓰는 페이로드들 정리해놨습니다.

## 주의

이건 공부할 때 쓰라고 취약하게 만든 거라, 실제로 돌아가는 서비스에는 절대 쓰면 안 됩니다.

필요하면 cli_simulator.py 로 웹 없이도 간단히 테스트 해볼 수 있어요.