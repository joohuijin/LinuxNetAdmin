# 07_MAIL · 메일 서버 (postfix + dovecot)

postfix(SMTP)와 dovecot(POP3/IMAP)으로 메일 서버를 구성한 실습. 도메인별 송수신, SASL 인증, 별칭·포워딩까지 진행. 메일 서버는 DNS(MX 레코드)에 의존.

- SMTP: postfix (25/tcp, 465/tcp, 587/tcp)
- POP3/IMAP: dovecot (110/995/143/993)
- 주 설정: `/etc/postfix/main.cf`, `/etc/postfix/master.cf`, `/etc/dovecot/dovecot.conf`
- 인증: SASL (postfix → dovecot 위임, 시스템 계정 인증)
- 방화벽: smtp/smtps/submission + pop3(s)/imap(s)

## 서버 구성

| 서버 | 도메인 | 메일 호스트 |
|------|--------|-------------|
| server1 | example.com | mail.example.com |
| server2 | test.com | mail.test.com |

- 각 도메인마다 메일 서버 1대 구성
- DNS의 MX 레코드로 도메인 → 메일 서버 지정

## 인증 구조

- `smtpd_sasl_type = dovecot` : postfix가 dovecot에 인증 위임
- `smtpd_sasl_auth_enable = yes` : SMTP 인증 사용
- `permit_sasl_authenticated` : 인증된 사용자만 릴레이 허용 (오픈 릴레이 방지)

## 작업 절차

```bash
# 패키지 설치
dnf install postfix dovecot s-nail

# 서비스 기동
systemctl enable --now postfix dovecot

# 방화벽 개방
firewall-cmd --permanent --add-service={smtp,smtps,pop3,pop3s,imap,imaps}
firewall-cmd --reload

# 별칭 반영
newaliases
```

## 폴더 구성

- `server1/`, `server2/` : 각 도메인 메일 서버 설정
  - `postfix-main.conf` : postconf -n 발췌 (실제 변경 설정)
  - `master.cf`, `dovecot.conf`, `aliases`

## 실습 범위 (파일 외)

- 메일 송수신: local↔local, local↔remote, remote↔remote
- 포워딩·메일링 리스트: /etc/aliases
- 클라이언트: Evolution(Linux), Thunderbird(Windows)
- 보안 확장: anti-spam(Amavisd), anti-virus(ClamAV), 웹메일(RoundCube)
