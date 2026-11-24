#!/usr/bin/env python3
"""Generate the checked-in UTF-8 quote files for GitHub Pages."""
from argparse import ArgumentParser
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse
import json

ROOT = Path(__file__).resolve().parent
START = date(2026, 11, 24)
CATEGORIES = ("中国古代", "外国古典", "中国近现代", "外国近现代")


def feed(catalog):
    groups = defaultdict(list)
    ids, texts = set(), set()
    for quote in catalog["quotes"]:
        source = catalog["sources"][quote["source"]]
        text = quote["text"]
        assert quote["id"] not in ids and text not in texts, quote["id"]
        assert len(text) <= 46 and text == text.strip() and "\n" not in text and "\r" not in text
        assert any("\u3400" <= char <= "\u9fff" for char in text), quote["id"]
        assert quote["original"].strip() and source["rights"].strip()
        assert urlparse(source["url"]).scheme == "https"
        ids.add(quote["id"])
        texts.add(text)
        groups[quote["category"]].append((quote, source))

    assert set(groups) == set(CATEGORIES)
    assert len({len(group) for group in groups.values()}) == 1
    for offset, (quote, source) in enumerate(
        pair for round_ in zip(*(groups[category] for category in CATEGORIES)) for pair in round_
    ):
        day = (START + timedelta(days=offset)).isoformat()
        credit = f'{source["author"]}《{source["work"]}》'
        if quote["source"] in {"lunyu", "mengzi"}:
            credit = f'《{source["work"]}》'
        if quote["source"] == "contemporary_yolo":
            credit = source["author"]
        assert len(credit) <= 36
        payload = {"date": day, "text": quote["text"], "credit": credit}
        if quote["source"] == "contemporary_yolo":
            payload.update(source=source["url"], license="https://creativecommons.org/licenses/by/4.0/",
                           adaptation="摘录，调整句末标点")
        yield day, json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify the published files without writing")
    args = parser.parse_args()
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    output = ROOT / "docs" / "daily"
    if not args.check:
        output.mkdir(parents=True, exist_ok=True)
    dates = set()
    for day, expected in feed(catalog):
        dates.add(day)
        path = output / (day + ".json")
        if args.check:
            assert path.read_text(encoding="utf-8") == expected, path
        else:
            path.write_text(expected, encoding="utf-8")
    assert {path.stem for path in output.glob("*.json")} == dates
    print(f"{len(dates)} daily quotes: {min(dates)} to {max(dates)}")


if __name__ == "__main__":
    main()
