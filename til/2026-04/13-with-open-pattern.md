# with 문으로 파일 열어 파싱하기

```python
with path.open("r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")
```

## 이 코드가 하는 일

```
1. context 열기 — 파일을 읽기 모드로 연다 (f = 파일 핸들)
2. 파일을 읽어서 BeautifulSoup으로 파싱 → 메모리에 soup 객체 구축
3. context 닫기 — 파일 핸들 반납 (블록 나가는 순간 자동)
```

## 핵심 포인트

- **파일 핸들은 빨리 반납**한다 — OS의 한정된 자원이므로
- **파싱 결과(soup)는 메모리에 남는다** — 블록 밖에서도 계속 사용 가능
- BeautifulSoup이 eager하게 읽기 때문에, 블록 안에서 파싱만 끝내면
  이후 파일을 닫아도 soup 사용에 문제 없다

## 구조

```
블록 안:    파일 핸들 + 파싱 결과
블록 밖:    파싱 결과만 (파일 핸들은 자동 반납)
```