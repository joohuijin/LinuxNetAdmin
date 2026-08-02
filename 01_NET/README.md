# 01_NET · 네트워크 설정 (CentOS 9)

NetworkManager로 고정 IP를 수동 설정한 실습. 설정은 `/etc/NetworkManager/system-connections/`의 프로필로 저장.

- 대상: server1 (ens160)
- 방식: method=manual (고정 IP)

## 설정 내용 (eth0.nmconnection)

- IP: 192.168.10.20/24
- gateway: 192.168.10.2
- DNS: 192.168.10.20, 8.8.8.8
- dns-search: example.com

## 핵심 명령

```bash
# 연결 이름을 eth0로 변경 후 활성화
nmcli connection modify <연결명> connection.id eth0
nmcli connection up eth0

# 설정 확인
ip addr                    # IP 확인
ip route                   # gateway 확인
cat /etc/resolv.conf       # DNS 확인
```

## 파일

- `eth0.nmconnection` : 실제 연결 프로필 (사설 IP)
