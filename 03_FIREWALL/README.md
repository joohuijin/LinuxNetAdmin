# 03_FIREWALL · 방화벽 (firewalld)

firewalld의 public zone에 서비스·포트를 개방한 실습. 이후 챕터(DNS·WEB·FTP·MAIL·Samba·NFS·iSCSI·MySQL)에서 필요한 서비스를 누적 개방.

## 개방한 서비스 (public zone)

- 웹: http, https
- 이름: dns
- 파일: ftp, nfs, mountd, rpc-bind, samba, samba-client
- 메일: smtp, smtps, pop3, pop3s, imap, imaps
- DB/기타: mysql, iscsi-target, ssh, cockpit, telnet

## 개방한 포트

- 953/tcp, 3389/tcp, 13306/tcp, 60000-60100/tcp

## 핵심 명령

```bash
# 서비스 영구 개방 후 적용
firewall-cmd --permanent --add-service=http --add-service=https
firewall-cmd --reload

# 런타임 설정을 영구로 저장
firewall-cmd --add-service=dns
firewall-cmd --runtime-to-permanent

# 확인
firewall-cmd --list-all
```

- `--permanent` 없이 실행하면 런타임 구성이라 재부팅 시 사라짐 → `--reload` 또는 `--runtime-to-permanent` 필요

## 파일

- `public.xml` : 실습으로 수정한 public zone 설정
