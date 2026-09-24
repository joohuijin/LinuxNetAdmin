# 15_iSCSI · iSCSI 스토리지

server1의 iSCSI Target과 server2의 Initiator 구성을 학습한 실습. 현재 남아 있는 Initiator 설정과 조회 당시 상태를 정리.

- Target 패키지: targetcli
- Initiator 패키지: iscsi-initiator-utils
- 통신: 3260/tcp
- Target 저장 설정: /etc/target/saveconfig.json
- Initiator 식별자: /etc/iscsi/initiatorname.iscsi
- Target 서비스: target.service
- Initiator 관련 서비스: iscsid.service, iscsi.service
- 방화벽 서비스: iscsi-target

## 동작 원리

Target이 제공하는 블록 스토리지에 Initiator가 IP 네트워크를 통해 접속.

- DAS: 서버에 직접 연결하는 스토리지
- NAS: 네트워크를 통해 파일 단위로 제공하는 스토리지
- SAN: 네트워크를 통해 블록 단위로 제공하는 스토리지. iSCSI는 IP SAN 방식
- Target: 저장 공간을 제공하는 측
- Initiator: 저장 공간을 사용하는 측
- IQN: Target·Initiator의 식별 이름
- Portal: Target 접속 IP와 포트
- Backstore: 실제 저장 공간을 제공하는 디스크·파일 등의 자원
- LUN: Target이 제공하는 논리 장치의 번호
- TPG: Portal·LUN·ACL 등을 묶어 관리하는 단위
- ACL: 접근을 허용할 Initiator와 LUN 매핑 관리
- CHAP: 필요에 따라 사용하는 인증 방식으로, 로그인 자체와는 구분

targetcli는 설정 도구이며 실제 Target의 데이터 처리는 Linux 커널의 LIO가 담당.

## 이 실습 구성

- server1(192.168.10.20): Target 구성 실습 대상
- server2(192.168.10.30): Linux Initiator 구성 실습 대상
- server2 IQN: iqn.2014-06.com.example:server2
- Windows Server 2012 Initiator 구성도 수업 범위에 포함되며, 현재 설정·연결 결과는 미수집

## 작업 절차

수업에서 다룬 작업 흐름:

- Target 패키지 설치: dnf install targetcli
- Target 구성: Backstore → Target IQN → TPG의 Portal·LUN·ACL 설정
- 설정 저장: targetcli의 saveconfig
- 부팅 시 설정 복원: target.service 사용
- 방화벽: Target에 3260/tcp 접근 허용
- Initiator 패키지 설치: dnf install iscsi-initiator-utils
- Initiator IQN 확인 후 Target 검색(Discovery) 및 로그인
- 연결된 세션과 블록 장치 확인

위 내용은 수업 절차 요약이며, 이번 정리에서 재구성하거나 실행한 절차는 아님.

## 확인 결과

- server1에 targetcli 2.1.57 설치 확인
- server1의 target.service는 inactive, TCP 3260 대기 소켓 없음
- 현재 saveconfig.json의 Backstore와 Target은 각각 0개
- /etc/target 하위 2단계 조회 범위에서 별도 백업 JSON 파일 없음
- server2의 iscsid.service·iscsi.service는 inactive
- iscsiadm -m node: No records found
- iscsiadm -m session: No active sessions
- server2의 Initiator IQN 설정은 보존되어 있음

현재 남아 있는 자료로는 과거 Target의 디스크·LUN·ACL 구성과 접속 성공 여부를 확인할 수 없음.

## 포함 파일

- server2/initiatorname.iscsi: 실제 설정에서 추출한 Initiator IQN

IQN은 장치 식별자이며 인증 비밀번호가 아님.
CHAP 인증정보, 디스크 데이터와 saveconfig.json 원문은 포함하지 않음.
