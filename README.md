# 피로그래머 숫자 카드 게임

## 과제 개요

- 기술 스택: Django, HTML/CSS/JavaScript, Docker
- 요구사항: 게임 기능 구현, Docker 이미지 배포 및 Compose 구현
- 노션 링크: 팀 노션 공개 URL 추가 예정
- Docker 이미지: 이미지 업로드 후 아래 링크로 제출

```text
https://hub.docker.com/r/minseo0614/piro-card-game
```

## 로컬 실행

```bash
source .venv/bin/activate
python manage.py migrate
python manage.py runserver
```

## Docker Compose 실행

```bash
docker compose up --build -d
```

자세한 배포 방법은 [DEPLOY.md](DEPLOY.md)를 참고합니다.
