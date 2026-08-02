# 06_FTP · FTP 서버 (vsftpd)

vsftpd로 FTP 서버를 구성한 실습. 로컬 사용자 접속, chroot 격리, SSL 암호화, 사용자 접근 제어, passive 모드까지 진행. (server1에서 구축)

- 패키지: vsftpd
- 데몬: vsftpd (21/tcp)
- 주 설정: `/etc/vsftpd/vsftpd.conf`
- 방화벽: ftp 서비스 + passive 포트(60000-60100) 개방

## 주요 설정 (vsftpd.conf)

| 항목 | 설정 | 내용 |
|------|------|------|
| 로컬 사용자 | local_enable=YES | 시스템 계정 FTP 접속 허용 |
| 쓰기 | write_enable=YES | 업로드 허용 |
| 익명 | anonymous_enable=YES | 익명 접속 허용 |
| SSL | ssl_enable=YES | 로그인·데이터 전송 암호화 |
| userlist | userlist_enable=YES | user_list 기반 접근 제어 |
| passive | pasv 60000-60100 | 방화벽과 맞춘 수동 모드 포트 |

## 접근 제어 파일

- `ftpusers` : FTP 접속 차단 사용자 (시스템 계정)
- `user_list` : userlist 기반 허용/차단 목록
- `chroot_list` : chroot 격리 예외 사용자
- `banner.txt` : 접속 시 표시 배너

## 작업 절차

```bash
# 패키지 설치
dnf install vsftpd

# 서비스 기동
systemctl enable --now vsftpd

# 방화벽 개방 (서비스 + passive 포트)
firewall-cmd --permanent --add-service=ftp
firewall-cmd --permanent --add-port=60000-60100/tcp
firewall-cmd --reload
```
