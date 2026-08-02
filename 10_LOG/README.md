# 10_LOG · 로그 관리 (rsyslog + 모니터링)

rsyslog로 로그를 분류·원격 전송하고, Prometheus·Loki·Grafana로 통합 모니터링을 구성한 실습.

- 로컬 로그: rsyslog (/etc/rsyslog.conf, /etc/rsyslog.d/*.conf)
- 원격 전송: 514/udp(@), 514/tcp(@@)
- 저널: systemd-journald (journalctl)
- 모니터링: Prometheus(자원) + Loki(로그) + Grafana(시각화)

로그 데이터(/var/log/*)는 사용자 활동·IP·인증 기록이 담겨 저장소에서 제외. 설정 파일만 포함.

## rsyslog 문법

facility.level action 형식.

- facility: kern, user, daemon, cron, mail, authpriv, local0-7
- level: emerg > alert > crit > err > warning > notice > info > debug
- action: 파일 경로 / 사용자 / @호스트(udp) / @@호스트(tcp)

## 원격 로그 전송 (이 실습)

클라이언트(server1) → 로그 서버(main)

- local2.notice   /var/log/file.log   (로컬 기록)
- local2.warning  @192.168.10.10      (원격 전송, udp)

로그 서버(main)는 514 포트를 열어 수집. udp는 @, tcp는 @@ 접두어.

## 주요 명령

- logger -p local2.notice "test message"   (테스트 로그 생성)
- journalctl -f -u sshd                     (실시간 + 특정 서비스)
- journalctl -p err                         (err 이상만)
- journalctl --since today

## 모니터링 스택 (파일 외)

- Prometheus + node_exporter: 서버 자원 수집 (9090, 9100)
- Loki + promtail: 로그 수집·전송 (3100)
- Grafana: 시각화 대시보드 (3000)

## 포함 파일

- remote.conf : rsyslog 원격 전송 설정
- promtail-config.yml : Loki 로그 전송 설정
