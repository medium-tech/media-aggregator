"""
OpenSearch indexing for articles.
"""

from datetime import datetime
from typing import List, Dict, Optional
from opensearchpy import OpenSearch, helpers
from mediaagg.clients import get_opensearch_client


def create_article_index(client: OpenSearch, index_name: str):
    """
    Create an article index with appropriate mappings.
    
    Args:
        client: OpenSearch client
        index_name: Name of the index to create
    """
    index_mapping = {
        "settings": {
            "number_of_shards": 2,
            "number_of_replicas": 1,
            "analysis": {
                "analyzer": {
                    "english_analyzer": {
                        "type": "english"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {"type": "text", "analyzer": "english_analyzer"},
                "description": {"type": "text", "analyzer": "english_analyzer"},
                "abstract": {"type": "text", "analyzer": "english_analyzer"},
                "content": {"type": "text", "analyzer": "english_analyzer"},
                "lead_paragraph": {"type": "text", "analyzer": "english_analyzer"},
                "url": {"type": "keyword"},
                "source": {"type": "keyword"},
                "author": {"type": "keyword"},
                "published_date": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "indexed_date": {"type": "date"},
                "category": {"type": "keyword"},
                "section": {"type": "keyword"},
                "keywords": {"type": "keyword"},
                "country": {"type": "keyword"},
                "language": {"type": "keyword"},
                "image": {"type": "keyword"},
            }
        }
    }
    
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name, body=index_mapping)


def index_articles(
    articles: List[Dict],
    source_name: str,
    client: Optional[OpenSearch] = None,
    index_prefix: str = "articles",
) -> Dict:
    """
    Index articles into OpenSearch.
    
    Args:
        articles: List of article dictionaries
        source_name: Source name for the index (e.g., 'nytimes', 'mediastack', 'gnews')
        client: OpenSearch client (if not provided, creates a new one)
        index_prefix: Prefix for the index name
    
    Returns:
        Dictionary with indexing results
    """
    if client is None:
        client = get_opensearch_client()
    
    # Create index name based on source (e.g., 'articles-nytimes')
    index_name = f"{index_prefix}-{source_name.lower().replace(' ', '-')}"
    
    # Ensure index exists
    create_article_index(client, index_name)
    
    # Prepare bulk actions
    actions = []
    for article in articles:
        doc = {
            **article,
            "indexed_date": datetime.now().isoformat(),
        }
        
        # Use URL as document ID to prevent duplicates
        doc_id = None
        if "url" in article and article["url"]:
            # Create a hash of the URL for document ID
            import hashlib
            doc_id = hashlib.md5(article["url"].encode()).hexdigest()
        
        action = {
            "_index": index_name,
            "_source": doc,
        }
        
        if doc_id:
            action["_id"] = doc_id
        
        actions.append(action)
    
    # Bulk index
    if actions:
        success, failed = helpers.bulk(client, actions, raise_on_error=False, stats_only=True)
        return {
            "success": success,
            "failed": failed,
            "index": index_name,
            "total": len(articles),
        }
    
    return {
        "success": 0,
        "failed": 0,
        "index": index_name,
        "total": 0,
    }
