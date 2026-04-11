# 16. 레포지토리 관리

## 왜 레포 관리가 중요한가?

```
코드가 쌓이면:
  - 어떤 변경이 언제, 왜 일어났는지 추적해야 한다
  - 여러 작업을 동시에 진행할 수 있어야 한다
  - 실험하다 망쳐도 되돌릴 수 있어야 한다
  - 다른 사람(또는 미래의 나)이 이해할 수 있어야 한다

→ 체계 없이 시작하면 나중에 정리하기 훨씬 어렵다
```

---

## 1. 모노레포 vs 멀티레포

### 모노레포 (Monorepo)

하나의 레포에 여러 프로젝트/모듈을 함께 관리한다.

```
my-repo/
├── study/
├── project-a/
├── project-b/
└── shared/
```

| 장점 | 단점 |
|------|------|
| 코드 공유/참조가 쉬움 | 레포가 커지면 느려질 수 있음 |
| 관리 포인트 1개 | git 히스토리가 섞임 |
| 관련 변경을 한 커밋에 | 권한 분리 어려움 |
| 의존성 버전 통일 | CI/CD 설정이 복잡해질 수 있음 |

```
적합한 경우:
  - 프로젝트 간 관계가 긴밀할 때
  - 소규모 팀 / 개인 프로젝트
  - "학습 + 구현"처럼 함께 성장하는 구조
```

### 멀티레포 (Multi-repo)

프로젝트마다 별도 레포를 만든다.

```
recommendation-study/     ← 레포 1
music-recommendation/     ← 레포 2
```

| 장점 | 단점 |
|------|------|
| 관심사 완전 분리 | 코드 공유 시 패키지화 필요 |
| git 히스토리 깔끔 | 관리 포인트 여러 개 |
| 독립적 배포/공유 | 레포 간 참조가 번거로움 |
| 레포별 권한 설정 가능 | 의존성 버전 불일치 가능 |

```
적합한 경우:
  - 프로젝트 간 독립성이 높을 때
  - 팀/조직이 나뉘어 있을 때
  - 오픈소스 배포 목적
```

### 선택 기준

```
질문 1: 프로젝트 간에 코드/자료를 자주 참조하는가?
  Yes → 모노레포 유리
  No  → 멀티레포 유리

질문 2: 독립적으로 배포/공유할 필요가 있는가?
  Yes → 멀티레포 유리
  No  → 모노레포 유리

질문 3: 혼자 관리하는가?
  Yes → 모노레포가 간편
  No  → 멀티레포로 권한 분리
```

---

## 2. 브랜치 전략

### Git Flow

가장 체계적인 브랜치 전략. 릴리스 주기가 있는 프로젝트에 적합하다.

```
main (production)
  └── develop (개발 통합)
        ├── feature/add-cf-model (기능 개발)
        ├── feature/youtube-api (기능 개발)
        └── ...

릴리스 시:
  develop → release/v1.0 → main
  
긴급 수정:
  main → hotfix/fix-bug → main + develop
```

```
장점: 역할이 명확, 안정적
단점: 복잡, 소규모 프로젝트에는 과함
적합: 팀 프로젝트, 릴리스 주기가 있는 서비스
```

### GitHub Flow

단순화된 전략. main + feature 브랜치만 사용한다.

```
main (항상 배포 가능 상태)
  ├── feature/add-cf-model
  ├── feature/youtube-api
  └── fix/data-parsing

작업 흐름:
  1. main에서 브랜치 생성
  2. 작업 + 커밋
  3. PR(Pull Request) 생성
  4. 리뷰 후 main에 머지
```

```
장점: 단순, 이해하기 쉬움
단점: 릴리스 관리가 약함
적합: 지속 배포, 소규모 팀, 개인 프로젝트
```

### Trunk-Based Development

main(trunk)에 직접 커밋하거나, 매우 짧은 브랜치만 사용한다.

```
main
  ├── short-lived-branch (1~2일 내 머지)
  └── short-lived-branch

→ 브랜치 수명이 매우 짧음
→ Feature Flag로 미완성 기능 숨김
```

```
장점: 머지 충돌 최소화, 빠른 통합
단점: 미완성 코드가 main에 들어갈 수 있음
적합: 대규모 팀 (Google, Facebook 방식)
```

### 개인 프로젝트에서의 선택

```
혼자 작업하는 경우:

Git Flow     → 과함 (브랜치 관리 오버헤드)
GitHub Flow  → 적당 (main + feature 브랜치)
Trunk-Based  → 가능 (main에 바로 커밋)

추천:
  실험/학습 단계: main에 바로 커밋해도 무방
  기능 단위 작업: feature 브랜치 사용 (GitHub Flow)
  
  → 처음엔 단순하게, 필요할 때 체계화
```

---

## 3. 커밋 컨벤션

### Conventional Commits

가장 널리 쓰이는 커밋 메시지 규칙이다.

```
<type>(<scope>): <description>

<body>       ← 선택

<footer>     ← 선택
```

### Type 종류

```
feat:     새 기능 추가
fix:      버그 수정
docs:     문서 변경
style:    코드 포맷팅 (기능 변화 없음)
refactor: 리팩토링 (기능 변화 없음)
test:     테스트 추가/수정
chore:    빌드, 설정 등 기타 변경
data:     데이터 관련 변경 (커스텀)
study:    스터디 자료 관련 (커스텀)
```

### 예시

```
좋은 커밋 메시지:
  feat(cf): add item-based collaborative filtering
  fix(parser): handle missing artist name in YouTube data
  docs(study): add sequence-based recommendation notes
  data: add YouTube watch history export
  chore: add scikit-learn dependency

나쁜 커밋 메시지:
  update code
  fix
  WIP
  asdf
  여러가지 수정
```

### Scope 활용

프로젝트 구조에 맞게 scope를 정하면 히스토리가 더 명확해진다.

```
scope 예시:
  study    — 스터디 자료
  data     — 데이터 수집/처리
  model    — 모델 관련
  api      — API 연동
  notebook — 노트북/실험
```

```
feat(model): implement matrix factorization with ALS
docs(study): add repo management guide
feat(api): add YouTube history parser
feat(notebook): add EDA for listening patterns
```

---

## 4. .gitignore 설계

### 기본 원칙

```
추적해야 하는 것:
  - 소스 코드
  - 설정 파일 (pyproject.toml 등)
  - 문서, 스터디 자료
  - 노트북 (결과 포함 여부는 판단)

추적하면 안 되는 것:
  - 환경/의존성 (.venv/, node_modules/)
  - 빌드 산출물 (__pycache__/, dist/)
  - 개인 데이터 (API 키, 시청 기록)
  - 대용량 데이터 파일
  - IDE 설정 (.vscode/, .idea/)
```

### 추천 .gitignore

```gitignore
# Python
.venv/
__pycache__/
*.pyc
*.egg-info/
dist/
build/

# Jupyter
.ipynb_checkpoints/

# Data (개인 데이터, 대용량)
data/raw/
data/personal/
*.csv
*.json
!config.json

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Environment
.env
*.key
```

### 데이터 관리 전략

```
개인 데이터 (시청 기록 등):
  → .gitignore에 추가
  → 로컬에만 보관

샘플 데이터:
  → 소량이면 git에 포함 (재현성)
  → data/sample/ 에 저장

대용량 공개 데이터:
  → .gitignore에 추가
  → 다운로드 스크립트를 git에 포함
  → README에 다운로드 방법 문서화
```

---

## 5. 프로젝트 문서화

### README.md

```markdown
# 프로젝트명

## 개요
한 줄 설명

## 구조
폴더 구조 설명

## 설치 및 실행
uv sync
...

## 데이터
필요한 데이터와 준비 방법

## 로드맵
현재 진행 상황
```

### CHANGELOG

변경 이력을 기록한다. Conventional Commits를 쓰면 자동 생성도 가능하다.

```markdown
## [0.2.0] - 2026-04-15
### Added
- Item-based CF 구현
- YouTube API 연동

### Fixed
- 데이터 파싱 시 누락 처리

## [0.1.0] - 2026-04-11
### Added
- 프로젝트 초기 세팅
- 스터디 자료 Phase 1~4
```

---

## 6. 버전 관리 팁

### 실험 관리

데이터 사이언스/ML 프로젝트에서 실험 추적이 중요하다.

```
방법 1: 노트북으로 관리
  notebooks/
  ├── 01_eda.ipynb
  ├── 02_content_based_v1.ipynb
  ├── 03_content_based_v2.ipynb
  └── 04_cf_experiment.ipynb

방법 2: 브랜치로 관리
  experiment/content-based-tfidf
  experiment/content-based-embedding
  experiment/cf-svd

방법 3: 실험 추적 도구
  MLflow, Weights & Biases 등
  → 규모가 커지면 도입 고려
```

### 되돌리기

```
마지막 커밋 취소 (변경 사항 유지):
  git reset --soft HEAD~1

특정 파일만 되돌리기:
  git checkout HEAD -- path/to/file

실험 브랜치 버리기:
  git branch -d experiment/failed-idea

→ git을 잘 쓰면 자유롭게 실험할 수 있다
  "언제든 돌아갈 수 있다"는 안전망
```

---

## 정리

```
레포지토리 관리 = 프로젝트의 이력과 구조를 체계적으로 유지하는 것

모노레포 vs 멀티레포:
  관련성 높고 혼자 관리 → 모노레포
  독립적이고 배포 필요 → 멀티레포

브랜치 전략:
  개인 프로젝트 → GitHub Flow (main + feature) 또는 main 직접 커밋
  필요할 때 체계화

커밋 컨벤션:
  Conventional Commits: type(scope): description
  커스텀 type 추가 가능 (study, data 등)

.gitignore:
  개인 데이터, 환경, 빌드 산출물 제외
  샘플 데이터와 다운로드 스크립트는 포함

문서화:
  README, CHANGELOG로 프로젝트 상태 공유

→ 처음부터 완벽할 필요 없다
→ 단순하게 시작하고, 필요할 때 체계화
```