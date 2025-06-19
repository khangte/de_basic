# 진행과정

첫 번째: docker-compose 활용해서 Streamlit app 시각화
두 번째: docker-compose 활용해서 FastAPI + Streamlit (ML)
세 번째: docker-compose 활용해서 MySQL + Streamlit (CRUD)

# 핵심적인 명령어

1. 모든 서비스 빌드 & 실행
```bash
docker compose up --build 
```
- Dockerfile 기반으로 이미지 빌드 후 컨테이너 실행
- ```--build``` 는 코드 변경이 있을 때만 사용(없으면 ```docker compose up```만 사용 가능)

2. 서비스 종료 + 컨테이너 삭제
```bash
docker compose down
```
- 실행 중인 컨테이너를 종료하고 삭제
- 네트워크, 컨테이너, container_name 등도 제거됨
- 볼륨은 유지됨
    + ```--volumes``` 는 볼륨까지 삭제

3. 서비스만 종료하고 삭제는 하지 않기
```bash
docker compose stop
```
- 컨테이너를 종료만 함

4. 중단된 서비스 재시작
```bash
docker compose start
```
- ```docker compose stop```으로 멈춘 컨테이너를 다시 시작
- 새로 빌드하지 않음, 이전 상태 유지

5. 컨테이너 재시작 (중단 상태든 실행 중이든 재시동)
```bash
docker compose restart
```
- stop + start를 한 번에 수행
- 컨테이너 재시작(중단 상태든 실행 중이든 강제로 새로 시작됨)
 