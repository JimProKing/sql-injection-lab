# SQL Injection 실습 랩

**직접 공격해보며 방어 방법을 비교하는 SQL 인젝션 교육용 프로젝트**

Python Flask와 JSP로 만든 실습 용 프로젝트입니다. 취약한 코드와 안전한 코드(PreparedStatement)를 비교하며 인증 우회, UNION, Blind SQLi 등 다양한 공격 기법을 직접 체험해 볼 수 있어요.

## ✨ 특징

- **Python Flask + SQLite** 취약 앱 + 안전 버전 비교
- **JSP 예제** 포함 (Tomcat + MySQL)
- 브라우저만으로 동작하는 인터랙티브 시뮬레이터
- 실제 공격 페이로드 수반 (payloads-cheatsheet)
- CLI 시뮬레이터도 제공

## 🚀 시작하기

### 1. Python 버전 (Windows 추천)

```powershell
cd sqli-lab\python

# Flask 설치
python -m pip install -r requirements.txt

# DB 초기화
python db_init.py

# 취약한 앱 실행 (창 열어둔 상태로 유지)
python vulnerable_app.py
```

브라우저에서 [http://127.0.0.1:5000](http://127.0.0.1:5000) 접속

> **Windows 팀**: `python` 대신 `py` 명령을 사용해도 됩니다.

### 2. 설치 없이 바로 테스트

`browser-simulator.html` 파일을 더블클릭해서 열어보세요.

### 3. Secure 버전 비교

다른 터미널에서:
```powershell
python secure_app.py
```
http://127.0.0.1:5001

## 📁 프로젝트 구조

```
sqli-lab/
├── README.md
├── LICENSE
├── browser-simulator.html      # 설치 없이 바로 실습
├── payloads-cheatsheet.md      # 공격 페이로드 모음
├── .gitignore
├── python/
│   ├── vulnerable_app.py       # 취약 버전 (Flask)
│   ├── secure_app.py           # 안전 버전
│   ├── db_init.py
│   ├── cli_simulator.py
│   └── requirements.txt
└── jsp/
    ├── vuln-*.jsp                # 취약 JSP 예제
    └── secure-*.jsp              # PreparedStatement 적용 버전
```

## 🎯 배울 수 있는 것

- Classic 인증 우회 (`admin' -- `)
- UNION-based 데이터 추출
- Boolean-based / Time-based Blind SQLi
- Second-order SQL Injection
- PreparedStatement를 이용한 안전한 방어 방법

## ⚠️ 주의사항

이 프로젝트는 **교육 목적** 으로 의도적으로 취약하게 만든 것입니다. 실제 서비스에 적용하거나 허가받지 않은 시스템에 사용하지 마세요.

## 📋 라이센스

MIT License
