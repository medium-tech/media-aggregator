"""
CLI for socials module.
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from .fetchers import fetch_tweets
from .indexer import index_tweets


# Load environment variables
load_dotenv()


def tweets_command(args):
    """
    Fetch tweets from a Twitter/X user handle.
    
    Example: mediaagg-socials tweets elonmusk --max-results 50
    """
    try:
        print(f"Fetching tweets from @{args.username}...")
        # Use provided bearer token or fall back to environment variable
        bearer_token = args.bearer_token or os.getenv("TWITTER_BEARER_TOKEN")
        tweet_list = fetch_tweets(
            username=args.username,
            start_time=args.start_time,
            end_time=args.end_time,
            max_results=args.max_results,
            bearer_token=bearer_token,
        )
        
        print(f"Found {len(tweet_list)} tweets")
        
        if not args.no_index:
            print("Indexing tweets into OpenSearch...")
            result = index_tweets(tweet_list)
            print(f"Indexed {result['success']} tweets into '{result['index']}'")
            if result['failed'] > 0:
                print(f"Failed to index {result['failed']} tweets", file=sys.stderr)
        else:
            for i, tweet in enumerate(tweet_list, 1):
                print(f"\n{i}. @{tweet['username']} ({tweet['created_at']})")
                print(f"   {tweet['text']}")
                print(f"   Likes: {tweet['like_count']}, Retweets: {tweet['retweet_count']}")
                print(f"   URL: {tweet['url']}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cli():
    """Media Aggregator - Social media fetcher and indexer."""
    parser = argparse.ArgumentParser(
        description="Media Aggregator - Social media fetcher and indexer"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Tweets command
    tweets_parser = subparsers.add_parser(
        "tweets",
        help="Fetch tweets from a Twitter/X user handle"
    )
    tweets_parser.add_argument("username", help="Twitter handle (without @)")
    tweets_parser.add_argument("--start-time", help="Start time in ISO 8601 format (e.g., '2024-01-01T00:00:00Z')")
    tweets_parser.add_argument("--end-time", help="End time in ISO 8601 format")
    tweets_parser.add_argument("--max-results", type=int, default=100, help="Maximum number of tweets (10-100, default: 100)")
    tweets_parser.add_argument("--bearer-token", help="Twitter API bearer token (defaults to TWITTER_BEARER_TOKEN env var)")
    tweets_parser.add_argument("--no-index", action="store_true", help="Don't index results, just print them")
    tweets_parser.set_defaults(func=tweets_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    cli()
