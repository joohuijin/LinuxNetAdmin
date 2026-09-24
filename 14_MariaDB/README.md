# 14_MariaDB · MariaDB 서버

MariaDB 설치와 DB·테이블·사용자 권한 관리, PHP 연결, 백업·복구를 학습한 실습. 저장소에는 확인한 서버 설정 항목과 현재 상태를 정리.

- 패키지: mariadb-server, mariadb
- 데몬: mariadbd (기본 3306/tcp)
- 서비스: mariadb.service
- 주 설정: /etc/my.cnf, /etc/my.cnf.d/*.cnf
- 데이터 디렉터리: /var/lib/mysql
- 방화벽 서비스: mysql

## 동작 원리

클라이언트가 MariaDB에 연결하면 사용자 인증과 권한에 따라 SQL을 실행.

- DBMS: 데이터베이스를 관리하는 소프트웨어
- Database: 관련 테이블을 묶는 단위
- Table: 열(Column)과 행(Row)으로 구성된 데이터 저장 구조
- 사용자 계정: 사용자 이름과 접속 출발지(Host)를 함께 구분
- PHP 연동: mysqli 등의 드라이버를 통해 DB에 연결

## 이 실습 구성

| VM | 확인한 설치 상태 | 현재 서비스 상태 |
| --- | --- | --- |
| main | mariadb-server·mariadb 미설치 | 해당 패키지 없음 |
| server1 | MariaDB 10.5.29, php-mysqlnd 8.0.30 | MariaDB·httpd 중지, php-fpm 실행 중 |
| server2 | MariaDB 10.5.29, php-mysqlnd 미설치 | MariaDB·httpd·php-fpm 비활성 |

server1·server2에서 확인한 설정:

- /etc/my.cnf가 /etc/my.cnf.d를 포함
- datadir=/var/lib/mysql
- socket=/var/lib/mysql/mysql.sock
- 조회 시 두 VM 모두 TCP 3306 대기 소켓 없음
- 선택 조회한 설정에서는 활성 bind-address·skip-networking 항목이 확인되지 않음

server1의 /var/www/html에 MariaDB 연결 및 로그인 관련 PHP 파일이 존재한다.
파일 존재만 확인했으며 현재 PHP↔DB 연결 성공 여부는 검증하지 않았다.

## 작업 절차

수업에서 다룬 작업 흐름:

- 패키지 설치: dnf install mariadb-server mariadb
- 서버 설정: /etc/my.cnf 및 /etc/my.cnf.d/mariadb-server.cnf
- 서비스 기동: systemctl enable --now mariadb
- DB 관리: 데이터베이스·테이블 생성과 조회, 데이터 입력·수정·삭제
- 접근 제어: 계정의 접속 출발지와 DB·테이블 권한 설정
- 원격 접속 점검: 대기 주소·포트, 방화벽, 계정·권한, SELinux
- 백업·복구: 논리적 백업과 물리적 백업의 절차 학습

위 내용은 수업 범위이며, 모든 작업의 현재 실행 성공을 의미하지 않음.

## 확인 결과

- server1·server2의 MariaDB 패키지와 설정 파일 존재 확인
- 데이터 디렉터리와 Unix 소켓 경로 확인
- 조회 당시 MariaDB 서비스는 모두 inactive
- 서비스 기동, DB 로그인, 쿼리 실행, PHP 연결 및 백업 복원은 이번 정리에서 재검증하지 않음

## 포함 파일

- server1/my.cnf: 설정 포함 디렉터리 발췌
- server1/mariadb-server.cnf: 설정 그룹·데이터·소켓 경로 발췌
- server2/my.cnf: 설정 포함 디렉터리 발췌
- server2/mariadb-server.cnf: 설정 그룹·데이터·소켓 경로 발췌

확인한 일부 설정 항목만 추출한 기록용 파일로, 원본 전체를 대체하는 배포용 설정이 아님.
비밀번호가 포함될 수 있는 PHP·SQL·사용자별 인증 설정과 DB 데이터·백업 파일은 포함하지 않음.
