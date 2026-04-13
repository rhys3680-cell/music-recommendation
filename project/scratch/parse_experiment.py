"""
유튜브 시청 기록 HTML 파싱 실험.

IPython에서 다음과 같이 사용:
    %run project/scratch/parse_experiment.py
    soup = load_soup()
    cell = soup.find("div", class_="outer-cell")
    parse_one(cell)
"""

import re
from pathlib import Path

from bs4 import BeautifulSoup


DATE_PATTERN = re.compile(r"^\d{4}\.\s*\d{1,2}\.\s*\d{1,2}\..*KST$")


def load_soup(path: str | Path = "project/data/raw/my-activity.html") -> BeautifulSoup:
    """HTML 파일을 로드해서 BeautifulSoup 객체로 반환."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return BeautifulSoup(f, "lxml")


def parse_one(cell):
    """시청 기록 한 건(outer-cell)을 파싱해서 dict로 반환."""
    content = cell.find("div", class_="content-cell")

    links = content.find_all("a")

    # 시청 기록이 아니면 None 반환
    # (링크가 2개 미만이거나, 첫 링크가 watch URL이 아니면)
    if len(links) < 2 or "watch" not in links[0].get("href", ""):
        return None

    video_link = links[0]
    channel_link = links[1]

    # 날짜 패턴에 맞는 텍스트만 watched_at으로 인식
    watched_at = None
    for text in content.stripped_strings:
        if DATE_PATTERN.match(text):
            watched_at = text
            break

    return {
        "title": video_link.get_text(),
        "video_url": video_link.get("href"),
        "channel_name": channel_link.get_text(),
        "channel_url": channel_link.get("href"),
        "watched_at": watched_at,
    }