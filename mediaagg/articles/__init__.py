"""
Articles module for fetching and indexing news articles from various sources.
"""

from .fetchers import fetch_nytimes, fetch_mediastack, fetch_gnews
from .indexer import index_articles

__all__ = ["fetch_nytimes", "fetch_mediastack", "fetch_gnews", "index_articles"]
