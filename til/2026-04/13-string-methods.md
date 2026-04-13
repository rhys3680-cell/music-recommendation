# 파이썬 문자열 메서드

오늘 사용한 것들 중심으로 정리.

## 공백/문자 제거

### strip / lstrip / rstrip

```python
s = "  hello  "
s.strip()       # "hello"      양쪽 공백 제거
s.lstrip()      # "hello  "    왼쪽만
s.rstrip()      # "  hello"    오른쪽만
```

### 특정 문자 제거도 가능

인자를 주면 **그 문자들**을 양쪽에서 제거한다.

```python
"xxhelloxx".strip("x")        # "hello"
"2026-4-11.".rstrip(".")      # "2026-4-11"
"...test...".strip(".")       # "test"
```

주의: 인자는 **문자 집합**이지 문자열이 아니다.

```python
"abcXYZcba".strip("abc")      # "XYZ"  (a, b, c 중 하나라도 해당되면 제거)
"abcXYZabc".strip("abc")      # "XYZ"  (끝의 cba도 a, b, c니까 제거)
```

---

## 검색

### in 연산자

```python
"KST" in "2026. 4. 11. KST"   # True
"xyz" in "hello"               # False
```

- 포함 여부만 확인, 가장 단순
- 단점: "ROCKSTAR"에 "KST"도 True → 주의

### startswith / endswith

```python
"hello.py".endswith(".py")     # True
"hello.py".startswith("he")    # True

# 튜플로 여러 개 검사 가능
"hello.py".endswith((".py", ".txt"))   # True
```

### find / index

```python
"hello".find("l")        # 2 (첫 위치)
"hello".find("xyz")      # -1 (없음)
"hello".index("l")       # 2
"hello".index("xyz")     # ValueError (없으면 에러)
```

---

## 치환

### replace

```python
"hello world".replace("world", "python")   # "hello python"
"aaa".replace("a", "b")                    # "bbb"
"aaa".replace("a", "b", 1)                 # "baa"  (최대 1회만)
```

- 정규식 아님 (파이썬 str 메서드)
- 모든 매칭을 치환 (기본값)

### 오늘 사용한 체이닝

```python
s.replace("오전", "AM")
 .replace("오후", "PM")
 .replace("KST", "")
 .strip()
 .replace(". ", "-")
 .rstrip(".")
```

- 각 메서드가 새 문자열을 반환 → 연속 호출 가능
- 단계별로 문자열을 다듬음

---

## 분할 / 결합

### split

```python
"a,b,c".split(",")         # ["a", "b", "c"]
"a  b   c".split()          # ["a", "b", "c"]  (공백 여러 개도 하나로)
"a,b,c".split(",", 1)      # ["a", "b,c"]      (최대 1회 분할)
```

### join

```python
",".join(["a", "b", "c"])   # "a,b,c"
"".join(["a", "b", "c"])    # "abc"
"\n".join(["a", "b", "c"])  # "a\nb\nc"
```

- **구분자 문자열의 메서드**임에 주의 (`",".join(...)`)

### splitlines

```python
"line1\nline2\nline3".splitlines()   # ["line1", "line2", "line3"]
```

---

## 대소문자

```python
"Hello".lower()        # "hello"
"Hello".upper()        # "HELLO"
"hello world".title()  # "Hello World"
"Hello".swapcase()     # "hELLO"
"Hello".casefold()     # "hello"  (다국어 안전 버전)
```

---

## 검사 메서드

```python
"123".isdigit()      # True   (숫자만)
"abc".isalpha()      # True   (알파벳만)
"abc123".isalnum()   # True   (알파벳+숫자)
"   ".isspace()      # True   (공백만)
"Hello".startswith("H")   # True
"Hello".endswith("o")     # True
```

- 빈 문자열에 대해서는 대부분 False

---

## 포맷팅

### f-string (추천)

```python
name = "World"
f"Hello {name}"              # "Hello World"
f"{3.14:.2f}"                # "3.14"       (소수점 2자리)
f"{100:,}"                   # "100"        (천 단위 콤마)
f"{42:>10}"                  # "        42" (오른쪽 정렬, 10칸)
f"{'hi':*^10}"               # "****hi****" (가운데, *로 채움)
```

### format 메서드 (옛 방식)

```python
"Hello {}".format("World")           # "Hello World"
"{name} is {age}".format(name="A", age=20)
```

### % 스타일 (더 옛 방식)

```python
"Hello %s" % "World"         # "Hello World"
"Pi is %.2f" % 3.14159       # "Pi is 3.14"
```

현대 파이썬(3.6+)에서는 **f-string이 표준**.

---

## 반복

```python
"ab" * 3          # "ababab"
"-" * 20          # "--------------------"
```

---

## 길이

```python
len("hello")      # 5
len("한글")       # 2  (문자 단위)
```

---

## pandas의 .str 접근자

문자열 Series에 똑같은 메서드를 적용할 때 `.str.` 접두사 사용.

```python
df["title"].str.strip()
df["title"].str.lower()
df["title"].str.contains("KST")
df["title"].str.replace("KST", "", regex=False)
df["title"].str.startswith("https")
df["title"].str.len()
df["title"].str.split(",")
```

주의:
- `.str.contains`, `.str.replace`는 **기본이 정규식 모드**
- 리터럴 치환은 `regex=False` 명시

---

## 오늘의 실전 예

### 한국어 날짜를 pandas가 파싱 가능한 형식으로 변환

```python
s = "2026. 4. 11. 오후 6:00:59 KST"

s = (
    s.replace("오전", "AM")
     .replace("오후", "PM")
     .replace("KST", "")
     .strip()
     .replace(". ", "-")
     .rstrip(".")
)
# "2026-4-11-PM 6:00:59"
```

### 각 단계가 하는 일

```
"오전" → "AM"            언어를 영어로
"오후" → "PM"
"KST"  → ""              시간대 문자 제거
strip()                  양쪽 공백 정리
". " → "-"               날짜 구분자를 하이픈으로
rstrip(".")              마지막 점 제거
```

---

## 정리

```
제거:    strip, lstrip, rstrip
검색:    in, startswith, endswith, find, index
치환:    replace
분할:    split, splitlines
결합:    join
대소문자: lower, upper, title
검사:    isdigit, isalpha, isalnum
포맷:    f-string
반복:    * 연산자
길이:    len()

pandas: df["col"].str.메서드
```

체이닝(메서드 연결 호출)으로 여러 단계를 깔끔하게 표현할 수 있다.