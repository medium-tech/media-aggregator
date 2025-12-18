"""
Fetchers for social media posts.
"""

import os
import tweepy
from typing import List, Dict, Optional


def fetch_tweets(
    username: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    max_results: int = 100,
    bearer_token: Optional[str] = None,
) -> List[Dict]:
    """
    Fetch tweets from a Twitter/X user.
    
    Args:
        username: Twitter handle (without @)
        start_time: Start time in ISO 8601 format (e.g., '2024-01-01T00:00:00Z')
        end_time: End time in ISO 8601 format
        max_results: Maximum number of tweets to fetch (10-100, default: 100)
        bearer_token: Twitter API bearer token (if not provided, reads from env)
    
    Returns:
        List of tweet dictionaries
    """
    if bearer_token is None:
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    
    if not bearer_token:
        raise ValueError("Twitter bearer token not provided")
    
    # Initialize Tweepy client
    client = tweepy.Client(bearer_token=bearer_token)
    
    # Get user ID from username
    user = client.get_user(username=username)
    if not user.data:
        raise ValueError(f"User '{username}' not found")
    
    user_id = user.data.id
    
    # Fetch tweets
    tweet_fields = [
        "created_at",
        "public_metrics",
        "entities",
        "referenced_tweets",
        "context_annotations",
    ]
    
    params = {
        "max_results": min(max_results, 100),
        "tweet_fields": tweet_fields,
    }
    
    if start_time:
        params["start_time"] = start_time
    if end_time:
        params["end_time"] = end_time
    
    tweets = client.get_users_tweets(user_id, **params)
    
    if not tweets.data:
        return []
    
    # Convert tweets to dictionaries
    tweet_list = []
    for tweet in tweets.data:
        tweet_dict = {
            "id": tweet.id,
            "text": tweet.text,
            "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
            "username": username,
            "user_id": user_id,
            "url": f"https://twitter.com/{username}/status/{tweet.id}",
            "retweet_count": tweet.public_metrics.get("retweet_count", 0) if tweet.public_metrics else 0,
            "reply_count": tweet.public_metrics.get("reply_count", 0) if tweet.public_metrics else 0,
            "like_count": tweet.public_metrics.get("like_count", 0) if tweet.public_metrics else 0,
            "quote_count": tweet.public_metrics.get("quote_count", 0) if tweet.public_metrics else 0,
        }
        
        # Add entities if available
        if hasattr(tweet, "entities") and tweet.entities:
            tweet_dict["hashtags"] = [
                tag["tag"] for tag in tweet.entities.get("hashtags", [])
            ]
            tweet_dict["mentions"] = [
                mention["username"] for mention in tweet.entities.get("mentions", [])
            ]
            tweet_dict["urls"] = [
                url["expanded_url"] for url in tweet.entities.get("urls", [])
            ]
        
        # Add context annotations (topics/entities)
        if hasattr(tweet, "context_annotations") and tweet.context_annotations:
            tweet_dict["topics"] = [
                annotation["domain"]["name"]
                for annotation in tweet.context_annotations
                if "domain" in annotation
            ]
            tweet_dict["entities"] = [
                annotation["entity"]["name"]
                for annotation in tweet.context_annotations
                if "entity" in annotation
            ]
        
        tweet_list.append(tweet_dict)
    
    return tweet_list
