# python 3.10을 기반으로 한 경량 이미지 사용
FROM python:3.10-slim

# 컨테이너 내 작업 디렉토리 설정 (이후 모든 명령은 /app 디렉토리 기준으로 실행됨)
WORKDIR /app

# 의존성 목록 파일 복사 (requirements.txt → /app/requirements.txt)
COPY requirements.txt .

# 이미지에 명령어 결과를 영구적으로 반영한다.
# 필요한 패키지 설치
RUN pip install -r requirements.txt

# 현재 디렉토리의 모든 파일을 컨테이너의 /app 디렉토리로 복사
COPY . .

# 컨테이너가 노출할 포트 설정 (Streamlit 기본 포트)
EXPOSE 8501

# 컨테이너 실행 시 Streamlit 앱 실행 (주의: CMD는 JSON 형식으로 써야 함. 아래 참고)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
