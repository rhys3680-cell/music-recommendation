# 프로젝트 구조 결정

## 결정

모노레포로 study, project, til을 한 레포에서 관리한다.

```
recommendation-algorithm/
├── study/        ← 체계적 스터디 자료
├── project/      ← 프로젝트 코드 (uv)
│   ├── src/
│   ├── data/
│   └── notebooks/
├── til/          ← 날짜 폴더 + 주제 파일
│   └── 2026-04/
├── .gitignore
└── README.md
```

## 왜 모노레포인가

- 혼자 관리하므로 관리 포인트는 적을수록 좋다
- 스터디와 프로젝트가 함께 성장하는 구조 — 프로젝트 진행하면서 스터디도 추가될 예정
- 학습 목적 + 개인 사용이라 독립 배포할 필요가 없다
- 스터디 자료를 참고하면서 코드를 짤 때 같은 레포에 있으면 편하다

## 왜 3개 폴더를 분리하는가

- **study**: 체계적으로 정리한 이론 자료. 주제별 번호 매김.
- **project**: 실제 코드. uv로 의존성 관리. 여기만 Python 환경.
- **til**: 그날 알게 된 짧은 메모. study와 성격이 다름 (정리 vs 메모).

## 커밋 컨벤션

Conventional Commits 사용. 스터디/프로젝트/TIL 구분을 위해 커스텀 type 추가.

```
feat(model): implement content-based filtering
docs(study): add deep learning recommendation notes
til: project structure decision
data: add YouTube watch history
chore: update dependencies
```

## TIL 구조

날짜 폴더 + 주제 파일 방식.

```
til/
├── 2026-04/
│   ├── 11-project-structure-decision.md
│   └── 12-youtube-api-setup.md
├── 2026-05/
│   └── ...
```

월별로 정리되어 깔끔하고, 파일명에 날짜+주제가 있어 검색도 쉽다.