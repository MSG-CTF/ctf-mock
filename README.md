# MSG CTF Mock API

Sentinel의 초기 개발과 장애 시나리오 시험에 사용하는 Django 서버입니다
실제 운영 서버와 구분된 환경에서 정상 응답·시간 초과·자원 부족·제공자 장애를 재현합니다

[플랫폼 전체 소개](https://github.com/MSG-CTF/msg-ctf.github.io)

## 맡은 일

- 백엔드·문제 인스턴스의 health와 상태 API 모사
- 할당량·예산·제공자 장애 시나리오 제어
- 스케줄러 신호·관리자 알림 수신 시험
- SLA 클라이언트와 연동하는 API·시나리오 테스트

## 함께 만든 사람들

| 기여자 | 기여 내용 | 관련 PR |
| --- | --- | --- |
| [minsoo0506](https://github.com/minsoo0506) | Django 기본 구조, Sentinel용 모사 API와 장애 시나리오·검사 설정 | [#1](https://github.com/MSG-CTF/ctf-mock/pull/1) · [#7](https://github.com/MSG-CTF/ctf-mock/pull/7) · [#8](https://github.com/MSG-CTF/ctf-mock/pull/8) |

2026-11-09까지 병합된 PR과 커밋을 기준으로 정리했습니다

## 기술 구성

Python · Django · Django REST Framework · SQLite · pytest

## 개발·운영 문서

- [기존 개발·설정 참고 문서](README.reference.md)
