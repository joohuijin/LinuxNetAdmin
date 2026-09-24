# 12_SSH · SSH 서버 (sshd)

SSH로 원격 접속과 공개키 인증을 구성한 실습. server2에서 접속 별칭을 사용해 server1의 root 계정으로 접속 확인.

- 패키지: openssh-server, openssh, openssh-clients
- 데몬: sshd (22/tcp)
- 주 설정: /etc/ssh/sshd_config, /etc/ssh/sshd_config.d/*.conf
- 클라이언트 설정: ~/.ssh/config
- 방화벽: ssh

## 동작 원리

서버 호스트 키 확인과 키 교환으로 암호화 연결을 수립한 뒤 사용자 인증을 수행.

- 호스트 키: 접속 대상 서버의 신원 확인
- 사용자 공개키 인증: 클라이언트의 개인키 서명을 서버에 등록된 공개키로 검증
- 개인키 passphrase: 개인키 파일을 보호하는 암호로, 서버 계정 패스워드와 별개

## 이 실습 구성

- 접속 방향: server2(192.168.10.30) → server1(192.168.10.20)
- 별칭: sshserver / 접속 계정: root
- 인증키 경로: ~/.ssh/id_rsa
- 호스트 키 기록 경로: ~/.ssh/my_known_hosts
- 세 VM 모두 22번 포트, root 로그인 및 공개키·패스워드 인증 허용
- AllowTcpForwarding 유효값: 세 VM 모두 yes
- GatewayPorts 유효값: main·server1은 yes, server2는 no

root 로그인과 패스워드 허용은 수업용 설정. 포워딩 허용 설정은 확인했으며 실제 터널 동작은 별도 미검증.

## 작업 절차

- 패키지 설치: dnf install openssh-server openssh-clients
- 서버 설정: /etc/ssh/sshd_config 및 sshd_config.d/*.conf
- 문법 확인: sshd -t / 유효값 확인: sshd -T
- 서비스 기동: systemctl enable --now sshd
- 키 생성: ssh-keygen -t rsa
- 공개키 등록: ssh-copy-id -i ~/.ssh/id_rsa.pub root@192.168.10.20
- 별칭 설정: server2의 /root/.ssh/config

위 절차는 수업 내용 요약. 저장된 설정과 아래 접속 결과를 실제 확인 근거로 사용.

## 접속 확인

server2에서 실행한 명령:

    ssh -o PreferredAuthentications=publickey -o StrictHostKeyChecking=yes sshserver 'hostname && whoami'

실제 결과:

    server1.example.com
    root

공개키 인증만 시도하고 호스트 키 확인을 강제한 조건에서 server1의 root 계정으로 원격 명령 실행 성공.

## 포함 파일

- server1/sshd_config: server1 서버 설정
- server1/sshd_config.d/01-permitrootlogin.conf: root 로그인 설정
- server2/sshd_config: server2 서버 설정
- server2/sshd_config.d/01-permitrootlogin.conf: root 로그인 설정
- server2/ssh_config: server2의 접속 별칭 설정 발췌

서버 설정은 주석과 빈 줄을 제외. 배포판의 50-redhat.conf와 암호화 정책 파일은 제외했으므로 전체 설정을 대체하는 배포용 파일은 아님.

개인키·공개키 원문·authorized_keys·known_hosts·my_known_hosts·로그인 암호는 저장소에 포함하지 않음.
