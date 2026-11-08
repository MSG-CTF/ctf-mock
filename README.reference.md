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
  mock_api/     # sentinel 연동용 mock API와 scenario 상태
  tests/        # API 및 시나리오 테스트
```

## 실행 방법

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

## 테스트

```bash
pytest
python manage.py check
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

## Mock API

| Method | Path | 설명 |
| --- | --- | --- |
| GET | `/health` | 본 CTF Django 서버 health 상태 |
| GET | `/api/status` | login, scoreboard, challenge, submission API 상태 |
| GET | `/api/instances` | sentinel이 감시할 문제 인스턴스 목록 |
| GET | `/api/instances/{instanceId}/health` | 문제 인스턴스 health 상태 |
| GET | `/api/broker/accounts` | quota, budget, provider 상태 |
| POST | `/api/scheduler/signals` | scheduler signal 수신 |
| POST | `/api/admin/alerts` | admin alert 수신 |
| POST | `/api/scenarios` | 장애 scenario 활성화/비활성화 |

장애 상태를 mocking하는 API는 sentinel이 실제 장애로 판단할 수 있도록 `503` 또는 `504`를 반환합니다.

| Scenario | 영향 |
| --- | --- |
| `django_down` | `/health`가 Django 서버 장애를 반환 |
| `django_db_down` | `/health`가 DB 연결 장애를 반환 |
| `django_cache_down` | `/health`가 cache 장애를 반환 |
| `django_api_timeout` | `/api/status`의 주요 API가 timeout 상태로 변경 |
| `instance_unhealthy` | 문제 인스턴스 health가 unhealthy 상태로 변경 |
| `instance_timeout` | 문제 인스턴스 health가 timeout 상태로 변경 |
| `ttl_expired` | 문제 인스턴스 생성 시간이 TTL 초과 상태로 변경 |
| `idle_timeout` | 문제 인스턴스 마지막 활동 시간이 idle timeout 초과 상태로 변경 |
| `quota_exhausted` | broker 계정 quota가 소진된 상태로 변경 |
| `budget_risk` | broker 계정 budget risk가 warning 상태로 변경 |
| `provider_failure` | provider adapter 장애 상태로 변경 |
| `broker_unavailable` | broker 조회 장애 상태로 변경 |

`/api/scenarios` 요청 예시는 다음과 같습니다.

```json
{
  "scenario": "django_db_down",
  "enabled": true
}
```

scenario를 초기화하려면 다음 요청을 보냅니다.

```json
{
  "scenario": "reset"
}
```

## Postman 테스트 순서

1. `GET http://localhost:8000/health`
2. `POST http://localhost:8000/api/scenarios`
3. `GET http://localhost:8000/health`
4. `GET http://localhost:8000/api/instances`
5. `GET http://localhost:8000/api/instances/inst-001/health`
6. `GET http://localhost:8000/api/broker/accounts`
7. `POST http://localhost:8000/api/scheduler/signals`
8. `POST http://localhost:8000/api/admin/alerts`

## 개발 원칙

- 실제 운영 데이터를 저장하지 않습니다.
- secret, token, flag, raw request body를 로그에 남기지 않습니다.
- 브루마블형 CTF 전체 기능이 아니라 `sentinel` 테스트에 필요한 최소 기능만 구현합니다.
