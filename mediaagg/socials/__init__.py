"""
Socials module for fetching and indexing social media posts.
"""

from .fetchers import fetch_tweets
from .indexer import index_tweets

__all__ = ["fetch_tweets", "index_tweets"]
