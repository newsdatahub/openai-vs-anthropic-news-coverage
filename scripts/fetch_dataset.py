#!/usr/bin/env python3
"""
Fetch OpenAI vs Anthropic articles from NewsDataHub (NDH) and save to CSV using cursor pagination.

Auth: header `x-api-key: ...`

Pagination: use `next_cursor` from response as `cursor` query param.
"""

from __future__ import annotations

import csv
import os
import sys
import time
from typing import Dict, Any, List, Optional

import requests

API_URL = "https://api.newsdatahub.com/v1/news"


def fetch_all(
    api_key: str,
    params: Dict[str, Any],
    out_csv: str,
    per_page: int = 100,
    max_pages: Optional[int] = None,
    sleep_s: float = 0.2,
) -> int:
    headers = {"x-api-key": api_key}
    cursor: Optional[str] = None

    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)

    fieldnames = ["id", "title", "source_title", "article_link", "description", "pub_date"]
    rows_written = 0
    page = 0

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            page += 1
            query_params = dict(params)
            query_params["per_page"] = per_page
            if cursor:
                query_params["cursor"] = cursor

            resp = requests.get(API_URL, headers=headers, params=query_params, timeout=60)
            if resp.status_code != 200:
                raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:2000]}")

            payload: Dict[str, Any] = resp.json()
            data: List[Dict[str, Any]] = payload.get("data") or []

            for item in data:
                writer.writerow({k: item.get(k) for k in fieldnames})
                rows_written += 1

            cursor = payload.get("next_cursor")

            if not cursor:
                break
            if max_pages is not None and page >= max_pages:
                break

            time.sleep(sleep_s)

    return rows_written


def main() -> None:
    api_key = "PROVIDE YOUR NEWSDATAHUB API KEY HERE"
    if not api_key:
        print("Missing NEWSDATAHUB API KEY HERE", file=sys.stderr)
        sys.exit(1)

    params = {
        "language": "en",
        "search_in": "title,description",
        "sort_by": "date",
        "deduplicate": "true",
        "fields": "title,source_title,article_link,description,pub_date",
        "q": "OpenAI OR Anthropic",
        "start_date": "2025-06-30",
    }

    out_csv = "data/openai_anthropic_last6mo.csv"
    per_page = 100

    rows = fetch_all(api_key=api_key, params=params, out_csv=out_csv, per_page=per_page)
    print(f"Wrote {rows} rows to {out_csv}")


if __name__ == "__main__":
    main()
