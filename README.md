# ragready

> **Unified text + metadata extractors for Retrieval-Augmented Generation (RAG) pipelines**  
> Version 0.1.2 · MIT-licensed

[![PyPI](https://img.shields.io/pypi/v/ragready?color=blue)](https://pypi.org/project/ragready/)
[![Downloads](https://img.shields.io/pypi/dm/ragready.svg?label=Downloads&color=brightgreen)](https://pypi.org/project/ragready/#files)

---

## ✨ Why ragready?

A high-quality RAG knowledge base starts with **clean, consistent documents**—no matter where they live.  
ragready streams Markdown-normalised content from:

| Source type              | Iterator            | Notes |
|--------------------------|---------------------|-------|
| GitHub / GitLab repos    | `git_repo_iter`     | Auth tokens supported |
| Atlassian Confluence     | `confluence_iter`   | Cloud & Data Center |
| Public websites          | `website_iter`      | BFS crawl within domain |
| Local files & folders    | `local_iter`        | PDFs, DOCX, PPTX, XLSX, CSV, images (OCR), audio, ZIPs, EPUB… |

Each iterator yields a single dataclass—**`DocumentRecord`**—so downstream code never worries about source-specific quirks.

---

## 🚀 Installation

```bash
pip install ragready
```

> Requires **Python ≥ 3.9** and a working `git` executable for repo extraction.
> The package bundles `markitdown[all]`, so DOCX/PDF/PPTX/XLSX and OCR support work out-of-the-box.

---

## ⚡ Quick start

```python
import ragready as rr
from pprint import pprint

# Crawl python.org two links deep
records = rr.website_iter(["https://www.python.org"], crawl_depth=2)

# Collect into a DataFrame (optional)
import pandas as pd
df = pd.DataFrame(r.to_dict() for r in records)
print(df[["filename", "content"]].head())
```

---

## 🍱 Example snippets

### 1. Local files

```python
import ragready as rr
import pandas as pd

# Optional LLM client (leave None for pure local parsing)
client = None
llm_model = None               

# Run the iterator and capture records
docs = [
    rec.to_dict()              
    for rec in rr.local_iter(
        ["./data"],           
        llm_client=client,
        llm_model=llm_model
    )
]

# Convert to a DataFrame (optional)
df = pd.DataFrame(docs)
print(df.head())               # quick peek
```

### 2. Git repo with private access

```python
# 1) Imports
import os
import pandas as pd
import ragready as rr

# Optional token for private repos
token = os.getenv("GITHUB_TOKEN")   # set in your shell, or leave None for public

# Pick the repos you want to scan
urls = [
    "https://github.com/pandas-dev/pandas.git",
    "https://gitlab.com/your-group/your-project.git",
]

# Run the iterator(s) and collect to dicts
git_records = [
    rec.to_dict()
    for url in urls
    for rec in rr.git_repo_iter(url, token=token)
]

# Build a DataFrame (optional)
git_df = pd.DataFrame(git_records)

# Inspect or save
print("\nGit repos preview:")
print(git_df[["source", "filename", "author", "url"]].head()) # quick peek
```

### 3. Confluence (plain-text)

```python
import os
import pandas as pd
import ragready as rr

# Stream the pages
conf_rows = [
    rec.to_dict()
    for rec in rr.confluence_iter(
        base_url=os.getenv("CONF_URL"),       # e.g. "https://your-domain.atlassian.net/wiki"
        username=os.getenv("CONF_USER"),      # your Atlassian email / user
        api_token=os.getenv("CONFLUENCE_TOKEN"),
        space_keys=["ENG", "DS"],             # any number of spaces
        plain_text=True,                      # strip HTML tags
        limit=500                             # max pages
    )
]

# Build a DataFrame
conf_df = pd.DataFrame(conf_rows)

# 3Preview key columns
print("\nConfluence preview:")
print(conf_df[["filename", "author", "url"]].head()) # quick peek
```

### 4. Website

```python
import pandas as pd
import ragready as rr

# Website crawl → DataFrame preview
web_rows = [
    rec.to_dict()
    for rec in rr.website_iter(
        roots=[
            "https://www.python.org",      # add more starting URLs as needed
            # "https://docs.rust-lang.org",
        ],
        crawl_depth=1                      # how deep to follow links (None = unlimited)
    )
]

web_df = pd.DataFrame(web_rows)

print("\nWebsite preview:")
print(web_df[["source", "title", "url"]].head())  # quick peek
```
---

## 🛠️ Public API

| Symbol            | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `DocumentRecord`  | Normalised dataclass each iterator yields            |
| `git_repo_iter`   | Stream files from GitHub / GitLab repos              |
| `confluence_iter` | Stream pages from Confluence spaces                  |
| `website_iter`    | Breadth-first crawl within a domain                  |
| `local_iter`      | Recursively convert local files via MarkItDown & OCR |

All iterators are **lazy streams**—process millions of docs without filling memory.

---

## 🔑 Environment variables

| Purpose    | Variable(s)                                 |
| ---------- | ------------------------------------------- |
| GitHub     | `GITHUB_TOKEN`                              |
| GitLab     | `GITLAB_TOKEN`                              |
| Confluence | `CONF_USER`, `CONFLUENCE_TOKEN`, `CONF_URL` |

---

## 📄 License

[MIT](LICENSE) © 2025 Kwadwo Daddy Nyame Owusu-Boakye

---

## 🤝 Contributing

1. Fork & branch off **`main`**
2. `pip install -e .[dev]`
3. Run `pytest` + `ruff check` before PRs

All contributions welcome — new extractors, bug fixes, or docs!

---

## 🙏 Acknowledgements

Built on the shoulders of:

* **[MarkItDown](https://pypi.org/project/markitdown/)** – universal document-to-Markdown converter
* **GitPython**, **BeautifulSoup 4**, **pdfplumber**, **python-pptx**, and the wider open-source community.

---

*Happy extracting — your RAG pipeline will thank you!* 🦾

---
