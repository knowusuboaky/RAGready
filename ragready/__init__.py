"""
ragready
========
Unified text & metadata extractors for Retrieval-Augmented Generation (RAG)
pipelines.

Main public API
---------------
git_repo_iter    -- Stream every text/config file from a GitHub / GitLab repo
confluence_iter  -- Stream pages from Confluence spaces
website_iter     -- Breadth-first crawl of a website (within-domain)
local_iter       -- Recursively convert local files to Markdown via MarkItDown
DocumentRecord   -- Normalised dataclass each iterator yields
"""

from importlib.metadata import PackageNotFoundError, version

# ----------------------------------------------------------------------
# Version
# ----------------------------------------------------------------------
try:
    __version__: str = version("ragready")  # name as published on PyPI
except PackageNotFoundError:                # running from source tree
    __version__ = "0.1.2"

# ----------------------------------------------------------------------
# Public re-exports
# ----------------------------------------------------------------------
from .extractors import (
    DocumentRecord,
    git_repo_iter,
    confluence_iter,
    website_iter,
    local_iter,
)

__all__: list[str] = [
    # Dataclass
    "DocumentRecord",
    # Iterators
    "git_repo_iter",
    "confluence_iter",
    "website_iter",
    "local_iter",
    # Metadata
    "__version__",
]
