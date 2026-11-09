<div align="center">
<h1>MSG CTF · SLA / Mock API</h1>
<p>Sentinel 개발 환경에서 정상 응답과 장애 상황을 재현하는 테스트 서버</p>
<p><a href="https://msg-ctf.github.io/platform.html">플랫폼</a> · <a href="#development">개발 문서</a></p>
</div>

<h2 align="center">Overview</h2>

<table align="center">
<tr><th width="260">응답 모사</th><th width="260">장애 재현</th><th width="260">연동 시험</th></tr>
<tr><td align="center">서비스 health·인스턴스 상태</td><td align="center">시간 초과·자원 부족·제공자 장애</td><td align="center">스케줄러 신호·관리자 알림</td></tr>
</table>

<h2 align="center">Contributors</h2>

<table align="center">
<tr><th align="center" colspan="12"><a href="https://github.com/MSG-CTF/sentinel">SLA</a></th></tr>
<tr>
<td align="center" valign="top" colspan="12" width="780"><a href="https://github.com/minsoo0506"><img src="https://avatars.githubusercontent.com/u/68321360?v=4&amp;s=128" width="52" height="52" alt="minsoo0506"></a><br><a href="https://github.com/minsoo0506"><b>minsoo0506</b></a><br><sub>Django · 모사 API<br>장애 시나리오·검사 설정</sub></td>
</tr>
</table>

<details>
<summary>기여 기록 · 관련 PR</summary>

| 기여자 | 기여 내용 | 관련 PR |
| --- | --- | --- |
| [minsoo0506](https://github.com/minsoo0506) | Django 기본 구조, Sentinel용 모사 API와 장애 시나리오·검사 설정 | [#1](https://github.com/MSG-CTF/ctf-mock/pull/1) · [#7](https://github.com/MSG-CTF/ctf-mock/pull/7) · [#8](https://github.com/MSG-CTF/ctf-mock/pull/8) |

</details>

<h2 align="center">Tech Stack</h2>

<p align="center"><img src="https://raw.githubusercontent.com/MSG-CTF/msg-ctf.github.io/67e93a09ce630910f98ae56fb118ca1317af78e0/assets/tech/djangorest.svg" width="44" height="44" alt="Django REST" title="Django REST"><br><sub>Django REST</sub><br><sub>Python · Django · SQLite · pytest</sub></p>

## Development

```bash
python -m pip install -r requirements.txt
python manage.py runserver
```

- [설치·실행 안내](README.reference.md)

<p align="center"><sub><a href="https://github.com/MSG-CTF/msg-ctf.github.io/blob/67e93a09ce630910f98ae56fb118ca1317af78e0/docs/tech-icons.md">아이콘 출처</a></sub></p>
