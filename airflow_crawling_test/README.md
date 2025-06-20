# 파일 구성
- airflow 폴더 생성
  + dags 폴더
  + logs 폴더
  + output 폴더
- dags 폴더 생성
  + 파이썬 파일 하나 생성
- requirements.txt
- 라이브러리 설치 셸스크립트(install_airflow.sh)
- airflow 실행 셸스크립트(run_airflow.sh)

## 파일 구조
```text
./
├── airflow/
│   ├── dags/
│   ├── logs/
│   └── ouput/
│       └── result_*.csv
│
├── dags/   
│   └── web_crawling_to_csv.py # DAG 코드
│
├── install_airflow.sh
├── README.md
├── requierments.txt
└── run_airflow.sh
```

---

# 실행방법

## 가상환경 설정
```bash
uv venv --python 3.11
source .venv/bin/activate
```

## 파일 실행 권한 부여
```bash
chmod +x install_airflow.sh
```

## Airflow 및 패키지 설치
```bash
./install_airflow.sh
```

## 10분간 Airflow 실행
```bash
./run_airflow.sh
```

## 접속 방법
http://localhost:8080/dags/apt_trade_to_csv/grid
