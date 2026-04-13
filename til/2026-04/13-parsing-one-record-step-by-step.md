# 시청 기록 한 건 파싱 — 단계별 풀이

HTML에서 한 건의 시청 기록을 dict로 만드는 과정을 단계별로 풀어본 기록.

## 전체 목표

```
HTML 한 조각 → {"title": ..., "video_url": ..., "channel_name": ..., ...}
```

## 1. HTML 로드

```python
from pathlib import Path
from bs4 import BeautifulSoup

path = Path("project/data/raw/my-activity.html")
# type(path) → WindowsPath

with path.open("r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")
# type(soup) → bs4.BeautifulSoup
```

## 2. 활동 셀 전체 추출

```python
cells = soup.find_all("div", class_="outer-cell")

# type(cells)    → bs4.element.ResultSet  (list처럼 동작)
# len(cells)     → 105584
# type(cells[0]) → bs4.element.Tag
```

`class_=`는 HTML class 속성 지정. `class`는 파이썬 예약어라 언더스코어 붙임.

## 3. 한 건의 Tag 내부 구조

```python
cell = cells[0]

cell.name    # 'div'
cell.attrs   # {'class': ['outer-cell', 'mdl-cell', 'mdl-cell--12-col', ...]}
```

- `name` = 태그 이름
- `attrs` = 속성 dict
- HTML class는 리스트로 파싱됨 (BS4가 자동 분할)

## 4. content-cell만 뽑기

```python
content = cell.find("div", class_="content-cell")
# type(content) → bs4.element.Tag
```

- `find`는 첫 번째만 반환 (없으면 None)
- outer-cell 안에 content-cell이 여러 개지만, 첫 번째가 영상 정보 담긴 본문

## 5. 링크(a 태그) 추출

```python
links = content.find_all("a")
# type(links) → ResultSet
# len(links)  → 2

# links[0] = 영상 링크
# links[1] = 채널 링크
```

## 6. Tag에서 정보 꺼내기

```python
video_link = links[0]

video_link.name            # 'a'
video_link.attrs           # {'href': 'https://www.youtube.com/watch?v=...'}
video_link.get("href")     # 'https://www.youtube.com/watch?v=...'
video_link.get_text()      # '벤슨 분 - Mystical Magical ...'
```

### Tag 조회 패턴

```
태그 이름:   tag.name
속성 전체:   tag.attrs
특정 속성:   tag.get("속성명")
내부 텍스트: tag.get_text()
```

## 7. 시청 시간 텍스트 뽑기

시간은 `<a>` 태그가 아니라 평문 텍스트로 박혀 있음. `stripped_strings`로 content 내 텍스트 조각 전부를 확인:

```python
texts = list(content.stripped_strings)
# type(texts) → list
# len(texts)  → 4

# [
#   '영상 제목',
#   '을(를) 시청했습니다.',
#   '채널명',
#   '2026. 4. 11. 오후 6:00:59 KST'
# ]
```

## 8. 정규식으로 날짜 찾기

```python
import re

DATE_PATTERN = re.compile(r"^\d{4}\.\s*\d{1,2}\.\s*\d{1,2}\..*KST$")

for t in texts:
    if DATE_PATTERN.match(t):
        print("매칭:", t)
```

- `^\d{4}\.` — 시작부터 "2026."
- `.*KST$` — "KST"로 끝
- → 제목에 "ROCKSTAR"가 있어도 매칭 안 됨 (시작 조건에서 배제)

## 9. 한 건을 dict로 조립

```python
record = {
    "title": links[0].get_text(),
    "video_url": links[0].get("href"),
    "channel_name": links[1].get_text(),
    "channel_url": links[1].get("href"),
    "watched_at": next(t for t in texts if DATE_PATTERN.match(t)),
}
```

### 결과

```python
{
    "title": "벤슨 분 (Benson Boone) - Mystical Magical 가사 번역 뮤직비디오",
    "video_url": "https://www.youtube.com/watch?v=nXuiMm2I0wk",
    "channel_name": "워너뮤직코리아 (Warner Music Korea)",
    "channel_url": "https://www.youtube.com/channel/UCLvhr40dgoBcV4XBlOhauNw",
    "watched_at": "2026. 4. 11. 오후 6:00:59 KST",
}
```

## 10. 새로 본 문법: next() + 제너레이터 표현식

```python
next(t for t in texts if DATE_PATTERN.match(t))
```

### 풀어서 보면

```python
# 리스트 컴프리헨션: 전부 다 만듦
matches = [t for t in texts if DATE_PATTERN.match(t)]
watched_at = matches[0]

# 제너레이터 표현식: 하나씩 필요할 때만
gen = (t for t in texts if DATE_PATTERN.match(t))
watched_at = next(gen)
```

- 리스트: 메모리에 전부 쌓음
- 제너레이터: 요청할 때 하나씩 생성 (lazy)
- `next()`로 첫 번째 값만 필요하면 더 효율적

### 안전한 버전 (매칭 없을 때 None)

```python
next(
    (t for t in texts if DATE_PATTERN.match(t)),
    None
)
```

기본값이 없으면 매칭 실패 시 `StopIteration` 에러.

## 타입 흐름 정리

```
path (WindowsPath)
  ↓ open + BeautifulSoup(lxml)
soup (BeautifulSoup)
  ↓ find_all
cells (ResultSet of Tag)
  ↓ [0]
cell (Tag)
  ↓ find
content (Tag)
  ├── find_all("a") → links (ResultSet of Tag)
  │                      ↓ [i].get("href"), get_text()
  │                   str (URL, 제목, 채널명)
  │
  └── stripped_strings → texts (list of str)
                            ↓ next + DATE_PATTERN
                         str (watched_at)
  ↓ dict 조립
record (dict)
```

## 배운 것 요약

```
BeautifulSoup의 세 가지 핵심 타입:
  BeautifulSoup → 문서 전체
  Tag           → 태그 하나 (계속 중첩 탐색 가능)
  ResultSet     → Tag의 컬렉션 (list처럼 동작)

Tag 정보 추출:
  .name, .attrs, .get("..."), .get_text()

텍스트 조각 순회:
  .stripped_strings (iterator)

패턴 매칭:
  re.compile + pattern.match

간결한 문법:
  next(generator expression) — 조건 매칭 첫 결과
```