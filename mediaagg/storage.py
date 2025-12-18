"""
Storage utilities for saving and loading raw data to/from disk.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional


def get_data_root() -> Path:
    """
    Get the data root directory from environment variable or default.
    
    Returns:
        Path object for the data root directory
    """
    data_root = os.getenv("DATA_ROOT", "./data")
    return Path(data_root)


def get_source_dir(source_name: str) -> Path:
    """
    Get the directory for a specific data source.
    
    Args:
        source_name: Name of the data source (e.g., 'nytimes', 'mediastack', 'tweets')
    
    Returns:
        Path object for the source directory
    """
    data_root = get_data_root()
    source_dir = data_root / source_name
    source_dir.mkdir(parents=True, exist_ok=True)
    return source_dir


def generate_article_id(article: Dict) -> str:
    """
    Generate a unique ID for an article.
    Uses URL if available, otherwise creates hash from title and date.
    
    Args:
        article: Article dictionary
    
    Returns:
        Unique ID string suitable for filename
    """
    if "url" in article and article["url"]:
        # Use SHA-256 hash of URL for better collision resistance
        return hashlib.sha256(article["url"].encode()).hexdigest()
    
    # Fallback: hash of title + published_date
    title = article.get("title", "")
    pub_date = article.get("published_date", "")
    content = f"{title}{pub_date}"
    return hashlib.sha256(content.encode()).hexdigest()


def save_article(article: Dict, source_name: str) -> str:
    """
    Save an article to disk as JSON.
    
    Args:
        article: Article dictionary
        source_name: Name of the data source (e.g., 'nytimes', 'mediastack', 'gnews')
    
    Returns:
        Path to the saved file
    """
    source_dir = get_source_dir(source_name)
    article_id = generate_article_id(article)
    filename = f"{article_id}.json"
    filepath = source_dir / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(article, f, indent=2, ensure_ascii=False)
    
    return str(filepath)


def save_tweet(tweet: Dict, source_name: str = "tweets") -> str:
    """
    Save a tweet to disk as JSON.
    
    Args:
        tweet: Tweet dictionary
        source_name: Name of the data source (default: 'tweets')
    
    Returns:
        Path to the saved file
    
    Raises:
        KeyError: If tweet does not have an 'id' field
    """
    if "id" not in tweet:
        raise KeyError("Tweet dictionary must have an 'id' field")
    
    source_dir = get_source_dir(source_name)
    tweet_id = str(tweet["id"])
    filename = f"{tweet_id}.json"
    filepath = source_dir / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tweet, f, indent=2, ensure_ascii=False)
    
    return str(filepath)


def load_data_file(filepath: str) -> Dict:
    """
    Load a data file from disk.
    
    Args:
        filepath: Path to the JSON file
    
    Returns:
        Dictionary with the data
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def list_data_files(source_name: str) -> List[Path]:
    """
    List all data files for a specific source.
    
    Args:
        source_name: Name of the data source
    
    Returns:
        List of Path objects for JSON files
    """
    source_dir = get_source_dir(source_name)
    return sorted(source_dir.glob("*.json"))


def load_all_data(source_name: str) -> List[Dict]:
    """
    Load all data for a specific source.
    
    Args:
        source_name: Name of the data source
    
    Returns:
        List of data dictionaries
    """
    files = list_data_files(source_name)
    data = []
    for filepath in files:
        try:
            item = load_data_file(str(filepath))
            data.append(item)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load {filepath}: {e}", file=sys.stderr)
    return data
