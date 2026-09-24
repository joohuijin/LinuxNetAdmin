# 13_NTP · NTP 서버 (chrony)

main이 외부 NTP 서버와 동기화하고, server1·server2에 시간을 제공하는 실습.

- 패키지: chrony
- 데몬: chronyd (NTP 서비스 123/udp)
- 서비스: chronyd.service
- 주 설정: /etc/chrony.conf
- 방화벽 서비스: ntp

## 동작 원리

외부 NTP 서버 → main → server1·server2 순서로 시간 동기화.

- Stratum: 기준 시계로부터의 계층. 숫자만으로 실제 정확도를 판단하지 않음
- NTP: 시스템 시계를 기준 시간에 동기화
- Timezone: 같은 시각을 지역 시간으로 표시하는 기준
- 이 실습의 시간대: Asia/Seoul (KST, UTC+9)

## 이 실습 구성

main (192.168.10.10):

- server 1.asia.pool.ntp.org iburst
- server 2.asia.pool.ntp.org iburst
- server 3.ke.pool.ntp.org iburst
- allow 192.168.10.0/24: 해당 대역의 NTP 클라이언트 허용

server1·server2:

- server 192.168.10.10 iburst: main에서 시간 수신

공통 설정:

- iburst: 초기 시간 측정을 빠르게 수행
- makestep 1.0 3: 처음 3번의 시계 업데이트에서 오차가 1초를 초과하면 즉시 보정 허용
- rtcsync: Linux에서 시스템 시간을 RTC에 주기적으로 반영하도록 활성화

## 작업 절차

- 패키지 설치: dnf install chrony
- 시간대 설정: timedatectl set-timezone Asia/Seoul
- 서버·클라이언트 설정: /etc/chrony.conf
- 서비스 기동: systemctl enable --now chronyd
- 설정 변경 반영: systemctl restart chronyd
- main의 방화벽: 적용 zone에 ntp 서비스 허용
- 확인: chronyc sources -v, chronyc tracking, timedatectl

위 절차는 수업 내용 요약. 방화벽 규칙 자체의 출력은 별도로 수집하지 않음.

## 동기화 확인

2026-09-25 01:00 KST에 조회한 결과.

| VM | 선택된 시간 소스 | 자신의 Stratum | 동기화 |
| --- | --- | --- | --- |
| main | 162.159.200.1 | 4 | 정상 |
| server1 | 192.168.10.10 | 5 | 정상 |
| server2 | 192.168.10.10 | 5 | 정상 |

- 세 VM 모두 chronyd active, System clock synchronized: yes
- chronyc tracking의 Leap status: Normal
- 선택된 소스는 sources 출력에서 ^*로 표시
- 선택된 소스의 Reach는 모두 377: 최근 8번의 전송에 유효한 응답 수신
- Poll 6은 64초, Poll 7은 128초의 폴링 간격
- main의 외부 소스 주소와 Stratum은 조회 시점의 값이며 변경될 수 있음

## 포함 파일

- main/chrony.conf: 외부 시간 소스와 내부 클라이언트 허용 설정
- server1/chrony.conf: main을 참조하는 클라이언트 설정
- server2/chrony.conf: main을 참조하는 클라이언트 설정

실제 설정에서 주석과 빈 줄을 제외. /etc/chrony.keys는 경로만 기록되며 인증 키 파일 자체는 포함하지 않음.
sourcedir가 참조하는 동적 소스 파일과 실행 중 데이터·로그도 포함하지 않음.
