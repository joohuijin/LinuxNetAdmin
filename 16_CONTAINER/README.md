# 16_CONTAINER · 컨테이너 관리 (Podman)

Podman을 이용한 이미지·컨테이너 관리, 스토리지·네트워크 구성 및 systemd 연동 학습 정리.

- 패키지: podman, container-tools
- 확인한 Podman 버전: 5.4.0
- 시스템 레지스트리 설정: /etc/containers/registries.conf
- 사용자 레지스트리 설정: ~/.config/containers/registries.conf
- 이미지 빌드 파일: Containerfile
- Podman은 컨테이너 관리에 상시 실행되는 중앙 데몬을 필수로 요구하지 않음

## 동작 원리

이미지를 바탕으로 격리된 프로세스 실행 환경인 컨테이너를 생성.

- 이미지: 애플리케이션과 실행에 필요한 파일을 담은 실행 기반
- 컨테이너: 이미지로 생성한 실행 인스턴스
- namespace: 프로세스·네트워크·마운트 등의 자원 접근 범위를 격리
- cgroups: CPU·메모리 등의 자원 사용 관리
- SELinux·Seccomp: 접근 제어와 시스템 호출 제한
- VM과 달리 호스트 커널을 공유
- Rootful: root 계정으로 관리
- Rootless: 일반 사용자 권한으로 관리하며, 사용자별 저장소와 컨테이너를 구분

## 주요 학습 내용

- 이미지 검색·다운로드·태그·업로드
- Containerfile을 이용한 이미지 빌드
- 컨테이너 생성·실행·중지·삭제
- 환경변수를 이용한 애플리케이션 설정 전달
- 볼륨·바인드 마운트를 이용한 데이터 보존
- 포트 매핑을 이용한 호스트와 컨테이너 포트 연결
- 사용자 정의 네트워크 구성
- systemd를 이용한 컨테이너 서비스 관리

## 주요 명령

- 이미지 목록: podman images
- 이미지 다운로드: podman pull
- 이미지 빌드: podman build
- 전체 컨테이너 목록: podman ps -a
- 컨테이너 생성·실행: podman create / podman run
- 실행 상태 변경: podman start / stop / restart
- 컨테이너 내부 명령 실행: podman exec
- 파일 복사: podman cp
- 컨테이너·이미지 삭제: podman rm / podman rmi
- 네트워크·볼륨 목록: podman network ls / podman volume ls

수업에서는 podman generate systemd를 이용한 유닛 생성도 학습.
Rootless 사용자 유닛은 systemctl --user로 관리.

## 확인한 환경

- 세 VM 모두 Podman 5.4.0 설치 확인
- server1에는 container-tools 설치
- 조회 당시 세 VM의 root 소유 컨테이너 목록은 비어 있음
- server1의 root 이미지 저장소에 registry.access.redhat.com/ubi8/httpd-24:latest 존재
- 세 VM의 root 환경에서 podman 이름의 bridge 네트워크 확인
- server1에 appdev·consvc 사용자와 Containerfile 두 개의 존재 확인
- Containerfile 위치: /root/podman/python36-app, /root/podman/httpd-app
- 일반 사용자 컨테이너 조회는 런타임 디렉터리 부재로 실패하여 상태 미확인
- 이미지 빌드·컨테이너 실행·웹 응답은 이번 정리에서 재검증하지 않음

## 포함 파일

- README.md: 수업 내용과 확인한 환경 정리

Containerfile·서비스 설정·인증 파일·환경변수 파일은 포함하지 않음.
레지스트리 계정 정보, 비밀번호, 토큰과 컨테이너 데이터도 제외.
