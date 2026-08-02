# 02_SELINUX · SELinux 관리 (CentOS 9)

SELinux 동작 모드를 permissive로 전환한 실습. 접근제어를 DAC에서 MAC으로 강화하는 계층.

## 모드 요약

- enforcing : 접근제어 적용 + 로깅 (기본 활성)
- permissive : 접근제어 미적용 + 로깅만 (테스트·문제해결용)
- disabled : 사용 안 함

## 핵심 명령

```bash
# 즉시 permissive 전환 (재부팅 없이)
setenforce 0

# 영구 설정 (config 수정)
sed -i 's/^SELINUX=enforcing/SELINUX=permissive/' /etc/selinux/config

# 상태 확인
sestatus
getenforce
```

- 참고: RHEL/CentOS 9부터 config의 `SELINUX=disabled`는 정책 미로드 상태라, 완전 비활성화는 `grubby --update-kernel ALL --args selinux=0` 사용

## 파일

- `selinux-config.txt` : config 핵심 설정 발췌 (permissive / targeted)
