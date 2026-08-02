# 05_WEB · 웹 서버 (Apache httpd)

Apache httpd로 정적·동적 웹을 구성한 실습. 사용자 페이지, 가상호스트, CGI/WSGI/PHP, 접근 보호까지 진행. (server2에서 구축)

- 패키지: httpd, mod_ssl
- 데몬: httpd (80/tcp, 443/tcp)
- 주 설정: `/etc/httpd/conf/httpd.conf`, `/etc/httpd/conf.d/*.conf`
- 웹 소스: `/var/www/html/*`, `/www1/*`
- 방화벽: http, https 개방

## 실습 내용

| 항목 | 설정 파일 | 내용 |
|------|-----------|------|
| 가상호스트 | vhost.conf | ServerName·DocumentRoot(/www1) 기반 이름 가상호스팅 |
| 사용자 페이지 | userdir.conf | ~user01 개인 디렉터리 (public_html) |
| CGI (bash) | vhost.conf | ScriptAlias /cgi-bin/ → test.cgi |
| CGI (perl) | perl.conf | mod_perl, /perl 핸들러 |
| WSGI (python) | vhost.conf | WSGIScriptAlias /myapp → myapp.wsgi |
| PHP | php.conf | index.php 처리 |
| 접근 보호 | .htaccess | AllowOverride + 인증으로 디렉터리 보호 |

## 작업 절차

```bash
# 패키지 설치
dnf install httpd mod_ssl

# 서비스 기동
systemctl enable --now httpd

# 방화벽 개방
firewall-cmd --permanent --add-service={http,https}
firewall-cmd --reload
```

## 보안 실습 (파일 미포함)

- `.htaccess` + `AuthUserFile`로 특정 디렉터리를 인증 후에만 접근 가능하도록 보호
- 웹셸(shell_exec 기반 원격 명령 실행) 취약점을 재현하고, .htaccess 인증으로 차단하는 흐름을 학습
- 웹셸 원본 코드는 위험성 때문에 저장소에서 제외

## 폴더 구성

- `conf/` : httpd 주 설정 및 실습 conf.d 설정
- `www1/` : 가상호스트 문서 루트 (cgi-bin, wsgi, php, .htaccess)
