# 초기 의존성 선정

## 상황

추천 알고리즘 프로젝트의 초기 환경을 구성한다.
데이터 처리, 분석, 모델링, 시각화, 노트북 환경이 필요하다.

## 선정한 패키지

```bash
uv add pandas numpy scikit-learn jupyter matplotlib seaborn
```

## 각 패키지의 역할

### pandas

- 표 형태 데이터 조작 (DataFrame)
- CSV/Parquet/JSON 읽고 쓰기
- 집계, 필터링, 조인
- 시청 기록 같은 시계열 데이터 다루기 좋음

### numpy

- 수치 계산의 기반
- 벡터/행렬 연산
- pandas, scikit-learn 등이 내부적으로 사용
- 직접 쓰는 일도 많음 (유사도 계산 등)

### scikit-learn

- 머신러닝 알고리즘 기본 세트
- TF-IDF, 코사인 유사도, SVD 등 추천에 쓰는 것들 포함
- Matrix Factorization도 가능
- 딥러닝 전까지는 이거 하나로 대부분 커버

### jupyter

- 노트북 환경 (.ipynb)
- 탐색적 분석, 중간 결과 확인
- 그래프 인라인 표시
- src/의 함수를 import해서 실험하는 용도

### matplotlib

- 파이썬의 표준 시각화 라이브러리
- 기본적인 그래프 (선, 막대, 히스토그램 등)
- 세밀한 커스터마이징 가능
- 다른 시각화 라이브러리의 기반

### seaborn

- matplotlib 위에 얹은 고수준 시각화
- 통계 그래프 (분포, 상관관계, 히트맵)
- 예쁜 기본 스타일
- pandas DataFrame과 궁합 좋음

## 선택 기준

1. **표준성** — 파이썬 데이터 스택의 de-facto 조합
2. **학습 목적에 적합** — 복잡한 도구 대신 널리 쓰이는 것
3. **CPU 환경 친화적** — GPU 없이도 돌아감
4. **상호 호환** — 이 6개는 서로 자연스럽게 연동됨

## 나중에 추가할 후보

```
beautifulsoup4, lxml   — HTML 파싱 (시청 기록 파싱 때 추가 예정)
google-api-python-client — YouTube Data API
spotipy                — Spotify API
implicit               — 암시적 피드백 MF (Cython, 빠름)
surprise               — 추천 전용 라이브러리 (SVD 등 바로 제공)
```

필요할 때 하나씩 추가하면서 이유를 TIL로 남긴다.

## 기록

초기에 모든 걸 설치하지 않고, 기본 세트만 깔았다.
"필요할 때 추가"가 원칙 — 의존성이 가벼울수록 좋다.