# 08_NFS · NFS 공유 + Automount

NFS로 디렉터리를 네트워크 공유하고, autofs로 자동 마운트를 구성한 실습. (server1에서 구축)

- 패키지: nfs-utils (서버·클라이언트 공통), autofs (자동 마운트)
- 데몬: nfsd (2049/tcp)
- 주 설정: `/etc/exports`, `/etc/exports.d/*.exports`
- 방화벽: nfs 서비스 (NFSv3는 mountd·rpc-bind 추가)

## NFS 공유 설정 (exports)

| 공유 경로 | 허용 대역 | 옵션 |
|-----------|-----------|------|
| /share | 192.168.10.0/24 | rw, no_root_squash |
| /usr/share/man | 192.168.10.0/24 | ro |
| /export/home | 192.168.10.0/24 | rw |

- `root_squash`(기본): 클라이언트 root를 nobody로 취급 (권한 축소)
- `no_root_squash`: 클라이언트 root를 서버 root로 인정
- NFS는 이름이 아니라 UID로 소유자를 판단 → 서버·클라이언트 UID를 맞춰야 함

## 작업 절차

```bash
# 패키지 설치
dnf install nfs-utils

# /etc/exports 작성 후 공유 갱신
exportfs -rv

# 서비스 기동
systemctl enable --now nfs-server

# 방화벽 개방
firewall-cmd --permanent --add-service=nfs
firewall-cmd --reload
```

## 확인 명령

```bash
exportfs -v                        # (서버) 공유 옵션 확인
showmount -e 192.168.10.20         # (클라이언트) 공유 자원 확인
mount 192.168.10.20:/share /mnt/share
```

## Automount 실습 (파일 외)

autofs로 필요 시에만 마운트하고 미사용 시 자동 해제하는 구성.

- 직접 맵: `/etc/auto.master.d/direct.autofs` → `/etc/auto.direct` (절대 경로 마운트)
- 간접 맵: `/etc/auto.master.d/indirect.autofs` → `/etc/auto.indirect` (`*`/`&`로 사용자별 홈 자동 마운트)
- 직접 맵은 서비스 기동 시, 간접 맵은 접근 시점에 마운트 포인트 생성

## 관련 실습 (파일 외)

- CD/DVD 이미지 공유, NFS 원격 백업
- NFSv4-only 서버 (nfs.conf에서 vers3=n, rpcbind 마스크)
- HAProxy 웹 부하 분산 (NFS로 web1·web2가 동일 소스 공유)
