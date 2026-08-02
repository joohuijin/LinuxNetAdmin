# 04_DNS · DNS 서버 (bind/named)

세 서버가 도메인을 나눠 맡는 계층형 DNS 구축 실습. 정방향·역방향 zone 구성, 도메인 위임, master/slave까지 진행.

- 패키지: bind, bind-utils
- 데몬: named (53/udp, 53/tcp)
- 주 설정: `/etc/named.conf`, `/etc/named.rfc1912.zones`
- zone 데이터: `/var/named/*.zone`, `/var/named/*.rev`
- 방화벽: dns 서비스 개방

## 서버 구성

| 서버 | 도메인 | 역할 |
|------|--------|------|
| main | root(.) / com | 상위 도메인 서버 |
| server1 | example.com | 하위 도메인 서버 |
| server2 | test.com | 하위 도메인 서버 |

- 도메인 위임: root → com → example/test 순으로 질의 위임
- 상위에서 하위 서버를 NS + glue 레코드로 지정

## 주요 레코드 (RR)

- `NS` : 도메인 담당 네임서버
- `A` : 도메인 → IP
- `PTR` : IP → 도메인 (역방향)
- `MX` : 메일 서버
- `CNAME` : 별칭

## 작업 절차

```bash
# 패키지 설치
dnf install bind bind-utils

# 설정 후 서비스 기동
systemctl enable --now named

# 방화벽 개방
firewall-cmd --permanent --add-service=dns
firewall-cmd --reload
```

## 확인 명령

```bash
nslookup www.example.com          # 정방향 질의
nslookup -q=PTR 192.168.10.20     # 역방향 질의
dig example.com
```

## 폴더 구성

- `main/` : root·com zone 설정
- `server1/` : example.com zone 설정
- `server2/` : test.com zone 설정
