# 09_SMB · 파일 공유 (Samba)

Samba로 Windows/Linux 간 파일 공유를 구성한 실습. 공유 정의, 사용자 인증, 접근 제어(valid users, write list)까지 진행. (server1에서 구축)

- 패키지: samba, samba-client, cifs-utils
- 데몬: smbd (139·445/tcp), nmbd (138·139/udp)
- 주 설정: `/etc/samba/smb.conf`
- 인증: security=USER (Samba 자체 사용자 DB)
- 방화벽: samba, samba-client

## 공유 정의 (smb.conf)

| 공유 | 경로 | 접근 제어 |
|------|------|-----------|
| public | /samba | guest ok, valid users=smbuser1 smbuser2 |
| test1 | /smbshare | write list=@marketing |
| homes | (사용자 홈) | 개인 홈 디렉터리 |

- hosts allow: 127., 192.168.10., 192.168.20. (지정 대역만 접속)

## 사용자 매핑

Samba는 리눅스 계정과 이름으로 매핑. 리눅스 사용자와 Samba 사용자를 각각 생성해야 함.

```bash
# 리눅스 사용자 (로그인 불가, 비번 불필요)
useradd -M -s /sbin/nologin smbuser1

# Samba 사용자 추가 (비번 설정)
smbpasswd -a smbuser1
smbpasswd -e smbuser1        # 활성화

# 확인
pdbedit -L                   # Samba 사용자 목록
```

## 작업 절차

```bash
# 패키지 설치
dnf install samba samba-client cifs-utils

# 문법 점검
testparm

# 서비스 기동
systemctl enable --now smb nmb

# 방화벽 개방
firewall-cmd --permanent --add-service={samba,samba-client}
firewall-cmd --reload
```

## 클라이언트 접근

```bash
smbclient -L 192.168.10.20 -U smbuser1        # 공유 자원 확인
mount -t cifs //192.168.10.20/public /mnt/server -o user=smbuser1
```

## 보안 주의 (파일 미포함)

- `passdb.tdb` (Samba 비번 DB)는 인증 정보라 저장소에서 제외
- 클라이언트 영구 마운트 시 `credentials` 파일(username/password)은 chmod 600 + 저장소 제외
