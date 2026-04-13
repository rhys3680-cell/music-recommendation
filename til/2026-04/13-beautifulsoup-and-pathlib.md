# BeautifulSoup과 pathlib 정리

유튜브 시청 기록 HTML을 파싱하면서 두 라이브러리의 기본 사용법을 정리한다.

## BeautifulSoup (bs4)

HTML/XML을 파싱해서 파이썬 객체로 다루게 해주는 라이브러리.

### 기본 사용

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_text, "lxml")
```

- `soup` = 파싱된 문서 전체 객체
- 파서 엔진: `"lxml"` (빠름), `"html.parser"` (표준), `"html5lib"` (관대)

### 주요 객체 타입

```
BeautifulSoup   — 문서 전체
Tag             — <div>, <a> 같은 태그 하나
NavigableString — 태그 안의 순수 텍스트
```

### 요소 찾기

#### 하나만

```python
soup.title                  # 첫 번째 <title>
soup.find("div")            # 첫 번째 <div>
soup.find("a", href=True)   # href 속성 있는 첫 <a>
```

#### 여러 개

```python
soup.find_all("a")
soup.find_all("div", class_="outer-cell")  # class는 예약어라 class_
```

#### CSS Selector

```python
soup.select("div.outer-cell")   # 클래스 매칭
soup.select("a[href]")          # 속성 있는 태그
soup.select_one("div.content")  # 첫 번째만
```

### 태그에서 정보 추출

```python
tag.name               # 태그명
tag.get_text()         # 내부 텍스트
tag.get("href")        # 속성 값 (없으면 None)
tag["href"]            # 같은 동작이지만 없으면 KeyError
tag.attrs              # 모든 속성 dict
```

### 텍스트 추출

```python
tag.string                # 단일 텍스트 (자식 있으면 None)
tag.get_text()            # 모든 자손의 텍스트 연결
tag.get_text(strip=True)  # 양쪽 공백 제거
tag.stripped_strings      # 공백 제거된 텍스트 iterator
```

### 트리 탐색

```python
tag.parent          # 부모
tag.children        # 직계 자식
tag.descendants     # 모든 자손
tag.next_sibling    # 다음 형제
tag.find_next("a")  # 다음 <a>
```

### 실제 사용 패턴

```python
# 1. 로드
soup = BeautifulSoup(html, "lxml")

# 2. 반복 대상 찾기
cells = soup.select("div.outer-cell")

# 3. 각 요소에서 정보 추출
for cell in cells:
    link = cell.find("a")
    if link:
        print(link.get("href"), link.get_text())
```

---

## pathlib.Path

파일 경로를 문자열이 아니라 **객체로** 다루는 표준 라이브러리.

### 왜 쓰는가

```python
# 옛날 방식
import os
path = os.path.join("data", "raw", "file.html")
os.path.exists(path)

# pathlib
from pathlib import Path
path = Path("data") / "raw" / "file.html"
path.exists()
```

- OS 무관 (Windows/Linux 경로 구분자 자동)
- 객체 메서드로 깔끔한 조작
- 표준 라이브러리 (설치 불필요)

### 생성

```python
Path("project/data/raw/file.html")
Path("/absolute/path")
Path.cwd()    # 현재 작업 디렉토리
Path.home()   # 홈 디렉토리
```

### 경로 속성

```python
p = Path("project/data/raw/my-activity.html")

p.name      # "my-activity.html"
p.stem      # "my-activity"
p.suffix    # ".html"
p.parent    # Path("project/data/raw")
p.parts     # ("project", "data", "raw", "my-activity.html")
```

### 경로 조합

```python
root = Path("project")
file = root / "data" / "raw" / "my-activity.html"
```

### 파일 읽기/쓰기

```python
p.exists()
p.is_file()
p.is_dir()

p.read_text(encoding="utf-8")           # 텍스트 읽기
p.write_text("내용", encoding="utf-8")  # 텍스트 쓰기
p.read_bytes()
p.write_bytes(data)

# context manager 방식
with p.open("r", encoding="utf-8") as f:
    data = f.read()
```

### 디렉토리

```python
p.mkdir(parents=True, exist_ok=True)  # 중간 경로도 만들고 있어도 OK

p.iterdir()         # 하위 항목
p.glob("*.html")    # 패턴 매칭
p.rglob("*.html")   # 재귀적 매칭
```

### 절대/상대 경로

```python
p.resolve()               # 절대 경로 변환
p.relative_to("project")  # 기준 경로로 상대화
```

---

## 정리

```
BeautifulSoup:
  - HTML 파싱
  - soup.select() 또는 find_all()로 요소 탐색
  - tag.get_text() / tag.get() 로 정보 추출

pathlib.Path:
  - 경로를 객체로
  - / 연산자로 조합
  - .exists(), .open(), .read_text() 등 메서드 풍부
```

두 라이브러리 모두 문자열/dict 기반 옛 방식보다
**객체 지향적이고 안전한 인터페이스**를 제공한다.