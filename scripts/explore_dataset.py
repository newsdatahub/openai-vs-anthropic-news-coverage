#!/usr/bin/env python3
"""
Explore the OpenAI vs Anthropic dataset CSV and produce artifacts for a demo:
- Weekly counts (mentions in title+description)
- Top sources
- Example rows for each brand
"""

from __future__ import annotations

import os
import re

import pandas as pd
import matplotlib.pyplot as plt

OPENAI_RE = re.compile(r"\bopenai\b", re.IGNORECASE)
ANTHROPIC_RE = re.compile(r"\banthropic\b", re.IGNORECASE)


def main() -> None:
    in_csv = os.getenv("IN_CSV", "data/openai_anthropic_last6mo.csv")
    out_dir = os.getenv("OUT_DIR", "outputs")
    os.makedirs(out_dir, exist_ok=True)

    df = pd.read_csv(in_csv)
    if df.empty:
        raise RuntimeError("CSV is empty. Run fetch_dataset.py first.")

    df["title"] = df["title"].fillna("").astype(str)
    df["description"] = df["description"].fillna("").astype(str)
    df["text"] = (df["title"] + " " + df["description"]).str.strip()

    df["mentions_openai"] = df["text"].apply(lambda x: bool(OPENAI_RE.search(x)))
    df["mentions_anthropic"] = df["text"].apply(lambda x: bool(ANTHROPIC_RE.search(x)))

    df["pub_dt"] = pd.to_datetime(df["pub_date"], utc=True, errors="coerce")
    df = df.dropna(subset=["pub_dt"])

    weekly = (
        df.assign(week=df["pub_dt"].dt.to_period("W").dt.start_time)
        .groupby("week")[["mentions_openai", "mentions_anthropic"]]
        .sum()
        .reset_index()
        .sort_values("week")
    )
    weekly.to_csv(os.path.join(out_dir, "weekly_counts.csv"), index=False)

    plt.figure()
    plt.plot(weekly["week"], weekly["mentions_openai"], label="OpenAI")
    plt.plot(weekly["week"], weekly["mentions_anthropic"], label="Anthropic")
    plt.xlabel("Week")
    plt.ylabel("Articles (mentions)")
    plt.title("Weekly mentions in title+description")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "weekly_counts.png"), dpi=200)
    plt.close()

    top_sources = (
        df.groupby("source_title")["id"]
        .count()
        .sort_values(ascending=False)
        .head(30)
        .reset_index()
        .rename(columns={"id": "article_count"})
    )
    top_sources.to_csv(os.path.join(out_dir, "top_sources.csv"), index=False)

    df.loc[df["mentions_openai"], ["pub_date", "source_title", "title", "article_link"]].head(50)\
      .to_csv(os.path.join(out_dir, "examples_openai.csv"), index=False)
    df.loc[df["mentions_anthropic"], ["pub_date", "source_title", "title", "article_link"]].head(50)\
      .to_csv(os.path.join(out_dir, "examples_anthropic.csv"), index=False)

    print(f"Saved outputs to {out_dir}/")


if __name__ == "__main__":
    main()
