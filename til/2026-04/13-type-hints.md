# 타입 힌트 (Type Hints)

## 왜 쓰는가

```python
def inspect_cell(cell):
    content = cell.find(...)    # cell이 뭔지 IDE가 모름 → 자동완성 X
```

IDE/타입 체커가 타입을 모르면:
- 자동완성이 안 뜸
- 잘못된 타입 전달해도 경고 없음
- 코드 읽을 때도 무엇을 받는 함수인지 불명확

```python
from bs4 import Tag

def inspect_cell(cell: Tag):
    content = cell.find(...)    # cell.find, cell.find_all 자동완성 O
```

## 기본 문법

### 변수

```python
name: str = "Alice"
age: int = 20
price: float = 9.99
active: bool = True
```

### 함수 인자와 반환

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def add(a: int, b: int) -> int:
    return a + b

def log(msg: str) -> None:      # 반환 없음
    print(msg)
```

### 컬렉션

```python
from typing import List, Dict, Tuple, Set

# 구버전
def process(items: List[int]) -> Dict[str, int]:
    ...

# Python 3.9+ (최신)
def process(items: list[int]) -> dict[str, int]:
    ...
```

### Optional (None 가능)

```python
# 구버전
from typing import Optional
def find(key: str) -> Optional[str]:
    ...

# Python 3.10+
def find(key: str) -> str | None:
    ...
```

### Union (여러 타입)

```python
# 구버전
from typing import Union
def parse(x: Union[str, int]) -> int:
    ...

# Python 3.10+
def parse(x: str | int) -> int:
    ...
```

## from __future__ import annotations

```python
from __future__ import annotations

def func(x: str | None) -> list[int]:
    ...
```

### 효과

- 모든 타입 힌트를 **문자열로 지연 평가**
- 구버전 파이썬(3.7~3.9)에서도 최신 문법(`str | None`, `list[int]`) 사용 가능
- 순환 참조 문제 완화
- 관용적으로 파일 최상단에 추가

## 런타임 영향

```python
def add(a: int, b: int) -> int:
    return a + b

add("hello", "world")   # "helloworld"   ← 에러 안 남!
```

- 타입 힌트는 **런타임에 검사되지 않음**
- 진짜 검사하려면 pydantic, typeguard 등의 도구 필요
- 보통은 IDE/정적 분석(mypy, pyright)이 체크

## 타입 힌트의 실제 가치

### 1. IDE 자동완성

```python
def parse(cell: Tag):
    cell.        # ← 여기서 Tag의 메서드들이 제안됨
```

### 2. 에러 조기 발견

```python
def add(a: int, b: int) -> int:
    return a + b

add("hello", 1)   # ← mypy/pyright가 경고
```

### 3. 문서화

```python
# 타입 힌트 없음
def process(data):
    ...

# 타입 힌트 있음 — 훨씬 명확
def process(data: list[dict[str, int]]) -> pd.DataFrame:
    ...
```

## 흔히 쓰는 타입

### 기본

```python
int, float, bool, str, bytes
list, tuple, dict, set
None
```

### typing 모듈에서 (예전)

```python
from typing import List, Dict, Tuple, Set
from typing import Optional, Union, Any
from typing import Callable, Iterator, Iterable
```

### Python 3.9+에서는 기본 제공

```python
list[int], dict[str, int], tuple[int, ...]
```

### Callable (함수 타입)

```python
from typing import Callable

def apply(fn: Callable[[int], int], x: int) -> int:
    return fn(x)

# Callable[[인자_타입들], 반환_타입]
```

### Any (아무 타입)

```python
from typing import Any

def debug(x: Any) -> None:
    print(x)
```

- 타입 체크를 사실상 끄는 것 → 남용 주의

## 외부 라이브러리 타입 활용

```python
from bs4 import BeautifulSoup, Tag
import pandas as pd

def parse_html(html: str) -> BeautifulSoup:
    ...

def get_records(soup: BeautifulSoup) -> list[Tag]:
    return soup.find_all("div")

def to_df(records: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(records)
```

- 라이브러리가 제공하는 타입을 그대로 import해서 사용

## 실전 예 (우리 프로젝트)

```python
from __future__ import annotations

from bs4 import Tag


def inspect_cell(cell: Tag) -> dict:
    content = cell.find("div", class_="content-cell")
    links = content.find_all("a") if content else []
    ...
    return {...}


def show(info: dict, keys: list[str] | None = None) -> None:
    if keys is None:
        keys = [...]
    for key in keys:
        ...
```

- `Tag`로 cell이 BeautifulSoup 태그임을 명시
- `dict` 반환으로 dict 반환을 명시 (더 세밀하게 `TypedDict` 사용도 가능)
- `list[str] | None`으로 기본값 None 가능 표현

## 더 세밀한 타입: TypedDict

dict의 키/값 타입까지 지정하고 싶다면:

```python
from typing import TypedDict

class CellInfo(TypedDict):
    cell: Tag
    links: list
    link_count: int
    texts: list[str]

def inspect_cell(cell: Tag) -> CellInfo:
    return {...}
```

- IDE가 `info["link_count"]` 접근 시 int로 추론
- 과하게 복잡해질 수 있으므로 필요할 때만

## 정리

```
타입 힌트 = 변수/인자/반환의 타입을 명시

효과:
  - IDE 자동완성
  - 정적 분석 도구의 에러 탐지
  - 코드 문서화

런타임 영향 없음 → 성능/동작에 영향 X
단, pydantic 등은 런타임 검증 추가 가능

관례:
  - from __future__ import annotations (상단)
  - list[int], dict[str, int] (Python 3.9+)
  - str | None (Python 3.10+)
  - 외부 라이브러리 타입도 import해서 활용
```