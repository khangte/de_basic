FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 모델생성 단계 추가
RUN python train.py

CMD ["uvicorn", "api:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
