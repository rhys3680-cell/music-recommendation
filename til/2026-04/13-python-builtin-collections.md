# 파이썬 기본 자료구조

파이썬에는 네 가지 내장 컬렉션 자료구조가 있다: `list`, `tuple`, `dict`, `set`.

## 요약

| 타입 | 순서 | 중복 | 수정 | 리터럴 | 용도 |
|------|------|------|------|--------|------|
| list | O | O | 가능 (mutable) | `[1, 2, 3]` | 순서 있는 여러 값 |
| tuple | O | O | 불가 (immutable) | `(1, 2, 3)` | 고정된 묶음 |
| dict | O (3.7+) | 키는 X | 가능 | `{"k": 1}` | key-value 매핑 |
| set | X | X | 가능 | `{1, 2, 3}` | 고유값 집합 |

---

## 1. list (리스트)

**순서가 있고 변경 가능한** 시퀀스.

### 생성

```python
empty = []
nums = [1, 2, 3]
mixed = [1, "hi", True, None]
from_iter = list(range(5))         # [0, 1, 2, 3, 4]
```

### 주요 메서드

```python
lst = [1, 2, 3]

# 추가
lst.append(4)           # [1, 2, 3, 4]
lst.insert(0, 0)        # [0, 1, 2, 3, 4]
lst.extend([5, 6])      # [0, 1, 2, 3, 4, 5, 6]

# 제거
lst.remove(3)           # 값 3 제거
lst.pop()               # 마지막 제거 + 반환
lst.pop(0)              # 첫 번째 제거 + 반환
lst.clear()             # 전부 제거

# 검색
lst.index(2)            # 값 2의 첫 위치
lst.count(2)            # 값 2의 개수
3 in lst                # 포함 여부

# 정렬
lst.sort()              # 제자리 정렬
lst.sort(reverse=True)  # 내림차순
sorted(lst)             # 새 리스트 반환 (원본 유지)
lst.reverse()           # 제자리 역순
```

### 인덱싱 / 슬라이싱

```python
lst = [0, 1, 2, 3, 4]

lst[0]        # 0
lst[-1]       # 4 (뒤에서 첫 번째)
lst[1:3]      # [1, 2]
lst[:3]       # [0, 1, 2]
lst[::2]      # [0, 2, 4] (스텝 2)
lst[::-1]     # [4, 3, 2, 1, 0] (역순)
```

### 리스트 컴프리헨션

```python
squares = [x**2 for x in range(5)]
# [0, 1, 4, 9, 16]

evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]
```

---

## 2. tuple (튜플)

**순서가 있고 변경 불가능한** 시퀀스.

### 생성

```python
empty = ()
single = (1,)           # 쉼표 필수 (없으면 그냥 괄호)
pair = (1, 2)
without_parens = 1, 2   # 괄호 없어도 튜플

from_list = tuple([1, 2, 3])
```

### 특징

```python
t = (1, 2, 3)

t[0]           # 인덱싱 가능
t[1:3]         # 슬라이싱 가능
1 in t         # 포함 검사

t[0] = 10      # TypeError! 수정 불가
```

### 언패킹

```python
# 여러 변수에 한번에 할당
a, b, c = (1, 2, 3)

# 함수가 여러 값 반환할 때
def min_max(nums):
    return min(nums), max(nums)

lo, hi = min_max([3, 1, 4, 1, 5])

# * 로 나머지 받기
first, *rest = [1, 2, 3, 4]
# first = 1, rest = [2, 3, 4]
```

### 언제 쓰는가

```
- 변하지 않는 데이터 묶음 (좌표, RGB 등)
- 함수의 여러 반환값
- dict의 키로 사용 (list는 키로 못 씀)
- 성능/메모리 (list보다 약간 가벼움)
```

---

## 3. dict (딕셔너리)

**key-value 매핑**. Python 3.7+부터 삽입 순서 보장.

### 생성

```python
empty = {}
d = {"name": "Alice", "age": 20}
from_pairs = dict([("a", 1), ("b", 2)])
from_kwargs = dict(a=1, b=2)
```

### 주요 연산

```python
d = {"name": "Alice", "age": 20}

# 접근
d["name"]              # "Alice"
d["missing"]           # KeyError
d.get("name")          # "Alice"
d.get("missing")       # None
d.get("missing", 0)    # 0 (기본값)

# 추가/수정
d["city"] = "Seoul"    # 새 키 추가
d["age"] = 21          # 기존 키 수정

# 제거
del d["age"]
d.pop("city")          # 값 반환
d.clear()

# 포함 검사 (키 기준)
"name" in d            # True
```

### 순회

```python
d = {"a": 1, "b": 2, "c": 3}

for k in d:                    # 키만
    print(k)

for k in d.keys():             # 키
    print(k)

for v in d.values():           # 값
    print(v)

for k, v in d.items():         # 키와 값
    print(k, v)
```

### 딕셔너리 컴프리헨션

```python
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 필터링
filtered = {k: v for k, v in d.items() if v > 1}
```

### 병합

```python
a = {"x": 1, "y": 2}
b = {"y": 20, "z": 30}

# Python 3.9+
merged = a | b                # {"x": 1, "y": 20, "z": 30}
a |= b                        # in-place

# Python 3.5+
merged = {**a, **b}

# update 메서드
a.update(b)                   # a에 반영
```

### 주의

```python
# 키가 될 수 있는 것: immutable (hashable)
{"key": 1}          # OK
{1: "one"}          # OK
{(1, 2): "tuple ok"}  # OK (tuple은 immutable)
{[1, 2]: "list"}    # TypeError (list는 mutable)
```

---

## 4. set (집합)

**고유한 값들의 순서 없는 집합**.

### 생성

```python
empty = set()          # {}는 빈 dict! 주의
s = {1, 2, 3}
from_list = set([1, 2, 2, 3, 3, 3])   # {1, 2, 3}
```

### 주요 연산

```python
s = {1, 2, 3}

# 추가/제거
s.add(4)               # {1, 2, 3, 4}
s.discard(2)           # 없어도 에러 안 남
s.remove(3)            # 없으면 KeyError
s.pop()                # 임의의 값 제거 + 반환
s.clear()

# 포함 검사 (O(1))
1 in s                 # True
```

### 집합 연산

```python
a = {1, 2, 3}
b = {3, 4, 5}

a | b           # 합집합 {1, 2, 3, 4, 5}
a & b           # 교집합 {3}
a - b           # 차집합 {1, 2}
a ^ b           # 대칭차 {1, 2, 4, 5}

# 메서드 방식
a.union(b)
a.intersection(b)
a.difference(b)
a.symmetric_difference(b)

# 부분집합
{1, 2}.issubset({1, 2, 3})     # True
{1, 2, 3}.issuperset({1, 2})   # True
```

### 언제 쓰는가

```
- 중복 제거: set(list) → 고유값만
- 빠른 포함 검사: 1 in set (O(1), list는 O(n))
- 집합 연산 필요할 때
```

### 주의

```python
# set의 원소도 hashable이어야 함
{1, 2, 3}          # OK
{"a", "b"}         # OK
{(1, 2), (3, 4)}   # OK
{[1, 2], [3, 4]}   # TypeError
```

---

## Mutable vs Immutable

### Mutable (변경 가능)

```python
list, dict, set
```

- 내용을 바꿀 수 있음
- dict 키나 set 원소로 쓸 수 없음
- 함수 인자로 전달 시 주의 (같은 객체 공유)

### Immutable (변경 불가)

```python
tuple, str, int, float, bool, frozenset
```

- 한 번 만들면 내용 변경 불가
- dict 키, set 원소로 사용 가능
- 안전하지만 매번 새 객체 생성

### 주의: mutable 기본 인자 함정

```python
# 나쁜 예
def append_to(item, lst=[]):
    lst.append(item)
    return lst

append_to(1)      # [1]
append_to(2)      # [1, 2] ← !! 같은 list 공유
append_to(3)      # [1, 2, 3]

# 올바른 방법
def append_to(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

---

## 언제 뭘 쓰나

### list
```
순서 있는 여러 값
추가/제거가 빈번
인덱스로 접근
```

### tuple
```
고정된 값들의 묶음
함수 여러 반환값
dict 키로 사용 필요 시
```

### dict
```
key-value 매핑
이름으로 값 찾기
JSON 같은 구조
```

### set
```
중복 제거
빠른 포함 검사
집합 연산
```

---

## 변환

```python
list("hello")              # ['h', 'e', 'l', 'l', 'o']
tuple([1, 2, 3])           # (1, 2, 3)
set([1, 1, 2, 2])          # {1, 2}
list({1: "a", 2: "b"})     # [1, 2] (키만)
dict([("a", 1), ("b", 2)]) # {"a": 1, "b": 2}
```

---

## 관련 고급 타입 (collections 모듈)

```python
from collections import Counter, defaultdict, OrderedDict, deque

# 개수 세기
Counter("hello")                    # {"h": 1, "e": 1, "l": 2, "o": 1}

# 기본값 있는 dict
dd = defaultdict(list)
dd["a"].append(1)                   # 키 없으면 자동 생성

# 양쪽 끝 빠른 큐
dq = deque([1, 2, 3])
dq.appendleft(0)                    # [0, 1, 2, 3]
dq.popleft()                        # 0
```

---

## 정리

```
list:  [1, 2, 3]     순서 O, 변경 O
tuple: (1, 2, 3)     순서 O, 변경 X
dict:  {"k": 1}      매핑, 키는 immutable
set:   {1, 2, 3}     고유값, 순서 X

공통 사용 가능:
  - len(x), x in y, for x in y
  - 리스트/딕셔너리 컴프리헨션
  - 생성자로 서로 변환

mutable/immutable 구분은 dict 키나 함수 기본 인자에서 중요
```