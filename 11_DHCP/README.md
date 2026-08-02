# 11_DHCP · DHCP 서버 (dhcpd)

DHCP로 네트워크 장비에 IP를 자동 할당한 실습. 동적 할당(범위)과 MAC 기반 고정 할당을 함께 구성. (main에서 서버 구축)

- 패키지: dhcp-server
- 데몬: dhcpd (67/udp)
- 주 설정: /etc/dhcp/dhcpd.conf
- 임대 기록: /var/lib/dhcpd/dhcpd.leases (실습 데이터라 저장소 제외)
- 방화벽: dhcp, dhcpv6

## 동작 원리 (DORA)

Discover(클라이언트 브로드캐스트) → Offer(서버) → Request(클라이언트) → Ack(서버 확정).

- DHCP 서버는 서비스 인터페이스에 고정 IP 필수 (자기 IP를 동적으로 못 받음)
- 서버와 클라이언트는 같은 대역에 존재 (다른 대역은 Bootp Relay 필요)
- 한 네트워크에 DHCP 서버는 원칙적으로 1대
- 실습 시 VMware 자체 DHCP는 반드시 꺼야 충돌 없음

## 이 실습 구성 (dhcpd.conf)

- 동적 범위: 192.168.10.51 ~ 192.168.10.80
- 게이트웨이: 192.168.10.2 / DNS: 192.168.10.20
- 임대: default 600s, max 7200s
- 고정 할당(MAC 기반):
  - server1 → 192.168.10.20
  - server2 → 192.168.10.30

## 작업 절차

- 패키지: dnf install dhcp-server
- 설정: /etc/dhcp/dhcpd.conf
- 기동: systemctl enable --now dhcpd
- 방화벽: firewall-cmd --permanent --add-service=dhcp --add-service=dhcpv6 ; firewall-cmd --reload

## 클라이언트 (참고)

- 동적: nmcli connection add con-name eth0-dhcp type ethernet ifname ens160
- 고정 할당: 서버 dhcpd.conf에 해당 MAC + fixed-address 지정
- 확장: DDNS (DNS ↔ DHCP 연동)

## 포함 파일

- dhcpd.conf : DHCP 서버 주 설정
