"""
OpenSearch indexing for social media posts.
"""

from datetime import datetime
from typing import List, Dict, Optional
from opensearchpy import OpenSearch, helpers
from mediaagg.clients import get_opensearch_client


def create_tweets_index(client: OpenSearch, index_name: str):
    """
    Create a tweets index with appropriate mappings.
    
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
                    "tweet_analyzer": {
                        "type": "standard",
                        "stopwords": "_english_"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "text": {"type": "text", "analyzer": "tweet_analyzer"},
                "username": {"type": "keyword"},
                "user_id": {"type": "keyword"},
                "url": {"type": "keyword"},
                "created_at": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                "indexed_date": {"type": "date"},
                "retweet_count": {"type": "integer"},
                "reply_count": {"type": "integer"},
                "like_count": {"type": "integer"},
                "quote_count": {"type": "integer"},
                "hashtags": {"type": "keyword"},
                "mentions": {"type": "keyword"},
                "urls": {"type": "keyword"},
                "topics": {"type": "keyword"},
                "entities": {"type": "keyword"},
            }
        }
    }
    
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name, body=index_mapping)


def index_tweets(
    tweets: List[Dict],
    client: Optional[OpenSearch] = None,
    index_name: str = "tweets",
) -> Dict:
    """
    Index tweets into OpenSearch.
    
    Args:
        tweets: List of tweet dictionaries
        client: OpenSearch client (if not provided, creates a new one)
        index_name: Name of the index (default: 'tweets')
    
    Returns:
        Dictionary with indexing results
    """
    if client is None:
        client = get_opensearch_client()
    
    # Ensure index exists
    create_tweets_index(client, index_name)
    
    # Prepare bulk actions
    actions = []
    for tweet in tweets:
        doc = {
            **tweet,
            "indexed_date": datetime.now().isoformat(),
        }
        
        action = {
            "_index": index_name,
            "_id": tweet["id"],  # Use tweet ID to avoid duplicates
            "_source": doc,
        }
        actions.append(action)
    
    # Bulk index
    if actions:
        success, failed = helpers.bulk(client, actions, raise_on_error=False, stats_only=True)
        return {
            "success": success,
            "failed": failed,
            "index": index_name,
            "total": len(tweets),
        }
    
    return {
        "success": 0,
        "failed": 0,
        "index": index_name,
        "total": 0,
    }
