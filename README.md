# OpenAI vs Anthropic — News Coverage Dataset (2025–2026)

This repository contains a reproducible dataset and simple analysis comparing **media coverage of OpenAI and Anthropic** over a six-month period.

Articles are included if **“OpenAI” or “Anthropic” appears in the article title or description**. The dataset is intended for coverage and trend analysis, not sentiment or opinion.

## Time range

Start date: 2025-06-30
End date: 2026-01-28

## What’s included

### Data

* `data/openai_anthropic_last6mo.csv`
  Article-level dataset containing titles, descriptions, publication dates, sources, and boolean mention flags.

* `data/weekly_counts.csv`
  Weekly aggregation of article counts for OpenAI and Anthropic.

### Outputs

* `outputs/weekly_counts.png`
  Line chart showing weekly coverage trends.

### Scripts

* `scripts/fetch_dataset.py`
  Fetches the dataset from the NewsDataHub API using cursor-based pagination.

* `scripts/explore_dataset.py`
  Generates weekly counts, plots, and summary tables.

## Methodology

* Articles are matched using **case-insensitive keyword search** on title and description.
* No entity resolution, fuzzy matching, or sentiment analysis is applied.
* Deduplication is applied at the API level, though syndicated content may still appear.
* Weekly counts are derived directly from article-level mention flags.

This dataset is a **static snapshot** and is not continuously updated.

## Example usage

```python
import pandas as pd

df = pd.read_csv("data/weekly_counts.csv")
df.plot(x="week", y=["mentions_openai", "mentions_anthropic"])
```

## Intended use

Suitable for:

* Media coverage trend analysis
* Time-series exploration and visualization
* NLP demos and benchmarking
* Teaching and dashboard examples

Not intended for:

* Sentiment or bias analysis
* Measuring public opinion
* Evaluating company performance

## License

CC-BY-4.0
This repository contains **article metadata only** and links to original sources.

## Source

Data collected via the **NewsDataHub API**
[https://newsdatahub.com](https://newsdatahub.com/?utm_source=github&utm_medium=repo&utm_campaign=openai_vs_anthropic)

## Hugging Face

The same dataset is available on Hugging Face:
[https://huggingface.co/datasets/newsdatahub/openai-vs-anthropic-news-coverage](https://huggingface.co/datasets/newsdatahub/openai-vs-anthropic-news-coverage)

## Contact

[support@newsdatahub.com](mailto:support@newsdatahub.com)
