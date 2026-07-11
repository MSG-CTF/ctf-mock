# ctf-mock

`ctf-mock`은 `sentinel` 개발과 통합 테스트를 위한 Django 기반 mock 서버입니다.

실제 본 CTF 서버, scheduler, broker, admin alert 채널이 완성되기 전까지 `sentinel`이 바라볼 최소 mocking API를 제공합니다.

## 목적

- Django 기반 본 CTF 서버의 health 상태를 mocking합니다.
- 문제 인스턴스의 health, timeout 상태를 mocking합니다.
- scheduler signal, admin alert 수신 endpoint를 제공합니다.
- quota, budget, provider 장애 상황을 테스트할 수 있게 합니다.

## 기술 스택

- Python
- Django
- Django REST Framework
- SQLite

## 디렉토리 구조

```text
ctf-mock/
  config/       # Django 프로젝트 설정
  mock_api/     # sentinel 연동용 mock API
  tests/        # API 및 시나리오 테스트
```

## MVP 범위

초기 MVP는 `sentinel` 연동 검증에 필요한 API만 구현합니다.

- `GET /health`
- `GET /api/status`
- `GET /api/instances`
- `GET /api/instances/{instanceId}/health`
- `GET /api/broker/accounts`
- `POST /api/scheduler/signals`
- `POST /api/admin/alerts`
- `POST /api/scenarios`

## 개발 원칙

- 실제 운영 데이터를 저장하지 않습니다.
- secret, token, flag, raw request body를 로그에 남기지 않습니다.
- 브루마블형 CTF 전체 기능이 아니라 `sentinel` 테스트에 필요한 최소 기능만 구현합니다.
