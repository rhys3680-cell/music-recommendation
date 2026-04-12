# HTML 파싱 라이브러리 선정

## 상황

Google Takeout에서 내보낸 유튜브 시청 기록이 HTML로 제공된다.
이걸 파싱해서 구조화된 데이터(DataFrame)로 변환해야 한다.

## 후보

### 1. BeautifulSoup (bs4)

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
items = soup.select('div.content-cell')
```

- 사용이 직관적 (CSS selector, find 등)
- 깨진 HTML도 관대하게 처리
- 파이썬에서 HTML 파싱의 사실상 표준
- 속도는 보통 (백엔드로 lxml 붙이면 빨라짐)

### 2. lxml (단독)

```python
from lxml import html as lxml_html
tree = lxml_html.fromstring(html)
items = tree.xpath('//div[@class="content-cell"]')
```

- 매우 빠름
- XPath 지원
- BeautifulSoup보다 API가 덜 친화적
- 깨진 HTML에 더 엄격

### 3. 정규식

```python
import re
matches = re.findall(r'<a href="(https://www\.youtube\.com/watch\?v=[^"]+)">([^<]+)</a>', html)
```

- 외부 의존성 없음
- 매우 빠름
- HTML 구조가 조금만 바뀌어도 깨짐
- 복잡한 구조는 유지보수 지옥

## 선택

**BeautifulSoup + lxml 백엔드**

```bash
uv add beautifulsoup4 lxml
```

## 이유

1. **HTML 구조가 복잡하지 않음** — 성능이 극단적으로 중요하진 않음
2. **안정성 > 속도** — 개인 데이터 파싱은 일회성에 가까움
3. **가독성** — 나중에 다시 봤을 때 이해하기 쉬움
4. **lxml 백엔드** — BeautifulSoup을 쓰되 lxml을 엔진으로 써서 속도도 확보

## 기록

정규식은 처음에 유혹적이지만 유튜브의 HTML 포맷이 바뀌면 바로 깨진다.
BeautifulSoup은 "제목 다음에 있는 채널 링크" 같은 구조적 탐색이 쉽다.