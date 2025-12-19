"""
Fetchers for news articles from various APIs.
"""

import os
import requests

from datetime import datetime
from typing import List, Dict, Optional
from mediaagg.storage import save_article


def fetch_nytimes(
    query: Optional[str] = None,
    begin_date: Optional[str] = None,
    end_date: Optional[str] = None,
    api_key: Optional[str] = None,
    save_to_disk: bool = True,
) -> List[Dict]:
    """
    Fetch articles from New York Times API.
    
    Args:
        query: Search query string
        begin_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format
        api_key: NY Times API key (if not provided, reads from env)
        save_to_disk: If True, saves articles to disk; if False, returns them
    
    Returns:
        List of article dictionaries (empty if save_to_disk is True)
    """
    if api_key is None:
        api_key = os.getenv("NYTIMES_API_KEY")
    
    if not api_key:
        raise ValueError("NY Times API key not provided")
    
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        "api-key": api_key,
        "sort": "relevance",
    }
    
    if query:
        params["q"] = query
    if begin_date:
        params["begin_date"] = begin_date
    if end_date:
        params["end_date"] = end_date
    
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    articles = []
    
    for doc in data.get("response", {}).get("docs", []):
        article = {
            "title": doc.get("headline", {}).get("main", ""),
            "abstract": doc.get("abstract", ""),
            "lead_paragraph": doc.get("lead_paragraph", ""),
            "url": doc.get("web_url", ""),
            "source": "NY Times",
            "published_date": doc.get("pub_date", ""),
            "keywords": [kw.get("value") for kw in doc.get("keywords", [])],
            "section": doc.get("section_name", ""),
            "author": doc.get("byline", {}).get("original", ""),
        }
        articles.append(article)
        
        if save_to_disk:
            save_article(article, "nytimes")
    
    return articles if not save_to_disk else []


def fetch_mediastack(
    keywords: Optional[str] = None,
    countries: Optional[str] = None,
    categories: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = 100,
    api_key: Optional[str] = None,
    save_to_disk: bool = True,
) -> List[Dict]:
    """
    Fetch articles from Mediastack API.
    
    Args:
        keywords: Keywords to search for
        countries: Comma-separated country codes (e.g., 'us,gb')
        categories: Comma-separated categories
        date_from: Start date in YYYY-MM-DD format
        date_to: End date in YYYY-MM-DD format
        limit: Maximum number of results
        api_key: Mediastack API key (if not provided, reads from env)
        save_to_disk: If True, saves articles to disk; if False, returns them
    
    Returns:
        List of article dictionaries (empty if save_to_disk is True)
    """
    if api_key is None:
        api_key = os.getenv("MEDIASTACK_API_KEY")
    
    if not api_key:
        raise ValueError("Mediastack API key not provided")
    
    url = "http://api.mediastack.com/v1/news"
    params = {
        "access_key": api_key,
        "limit": limit,
        "sort": "published_desc",
        "languages": "en",
    }
    
    if keywords:
        params["keywords"] = keywords
    if countries:
        params["countries"] = countries
    if categories:
        params["categories"] = categories
    if date_from:
        params["date"] = f"{date_from},{date_to or datetime.now().strftime('%Y-%m-%d')}"
    
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    articles = []
    
    for item in data.get("data", []):
        article = {
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "url": item.get("url", ""),
            "source": item.get("source", "Mediastack"),
            "published_date": item.get("published_at", ""),
            "category": item.get("category", ""),
            "country": item.get("country", ""),
            "language": item.get("language", ""),
            "author": item.get("author", ""),
            "image": item.get("image", ""),
        }
        articles.append(article)
        
        if save_to_disk:
            save_article(article, "mediastack")
    
    return articles if not save_to_disk else []


def fetch_gnews(
    query: Optional[str] = None,
    category: Optional[str] = None,
    lang: str = "en",
    country: str = "us",
    max_results: int = 10,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    api_key: Optional[str] = None,
    save_to_disk: bool = True,
) -> List[Dict]:
    """
    Fetch articles from GNews (Google News) API.
    
    Args:
        query: Search query string
        category: News category (e.g., 'technology', 'business')
        lang: Language code (default: 'en')
        country: Country code (default: 'us')
        max_results: Maximum number of results
        from_date: Start date in ISO format
        to_date: End date in ISO format
        api_key: GNews API key (if not provided, reads from env)
        save_to_disk: If True, saves articles to disk; if False, returns them
    
    Returns:
        List of article dictionaries (empty if save_to_disk is True)
    """
    if api_key is None:
        api_key = os.getenv("GNEWS_API_KEY")
    
    if not api_key:
        raise ValueError("GNews API key not provided")
    
    # Use search endpoint if query provided, otherwise top-headlines
    if query:
        url = "https://gnews.io/api/v4/search"
        params = {
            "q": query,
            "lang": lang,
            "country": country,
            "max": max_results,
            "apikey": api_key,
        }
        
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
    else:
        url = "https://gnews.io/api/v4/top-headlines"
        params = {
            "lang": lang,
            "country": country,
            "max": max_results,
            "apikey": api_key,
        }
        
        if category:
            params["topic"] = category
    
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    articles = []
    
    for item in data.get("articles", []):
        article = {
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "content": item.get("content", ""),
            "url": item.get("url", ""),
            "source": item.get("source", {}).get("name", "Google News"),
            "published_date": item.get("publishedAt", ""),
            "image": item.get("image", ""),
        }
        articles.append(article)
        
        if save_to_disk:
            save_article(article, "gnews")
    
    return articles if not save_to_disk else []
