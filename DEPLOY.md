# 배포

## Docker Compose 실행

`.env.example`을 복사해 `.env`를 만들고 비밀 값을 설정한 뒤 실행합니다.

```bash
docker compose up --build -d
docker compose ps
```

서비스 확인 주소는 `http://localhost:8000/health/`입니다.

DB 데이터는 `piro-card-mysql-data` Docker named volume에 저장되어
컨테이너를 다시 생성해도 유지됩니다.

웹 컨테이너는 시작할 때 마이그레이션을 실행한 뒤 Django 서버를
`0.0.0.0:8000`에서 실행합니다.

## Docker Hub 배포

```bash
docker login
docker compose build web
docker compose push web
```

제출 링크:

```text
https://hub.docker.com/r/minseo0614/piro-card-game
```

## 운영 도메인 설정

배포 환경의 다음 값을 실제 도메인으로 변경합니다.

```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=example.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://example.com
```

Google Cloud Console에도 다음 주소를 추가합니다.

```text
승인된 JavaScript 원본: https://example.com
승인된 리디렉션 URI:
https://example.com/accounts/google/login/callback/
```
