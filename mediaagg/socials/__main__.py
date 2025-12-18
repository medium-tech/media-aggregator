"""
CLI for socials module.
"""

import os
import click
from dotenv import load_dotenv
from .fetchers import fetch_tweets
from .indexer import index_tweets


# Load environment variables
load_dotenv()


@click.group()
def cli():
    """Media Aggregator - Social media fetcher and indexer."""
    pass


@cli.command()
@click.argument("username")
@click.option("--start-time", help="Start time in ISO 8601 format (e.g., '2024-01-01T00:00:00Z')")
@click.option("--end-time", help="End time in ISO 8601 format")
@click.option("--max-results", default=100, help="Maximum number of tweets (10-100, default: 100)")
@click.option("--bearer-token", envvar="TWITTER_BEARER_TOKEN", help="Twitter API bearer token")
@click.option("--no-index", is_flag=True, help="Don't index results, just print them")
def tweets(username, start_time, end_time, max_results, bearer_token, no_index):
    """
    Fetch tweets from a Twitter/X user handle.
    
    USERNAME is the Twitter handle (without @).
    
    Example: mediaagg-socials tweets elonmusk --max-results 50
    """
    try:
        click.echo(f"Fetching tweets from @{username}...")
        tweet_list = fetch_tweets(
            username=username,
            start_time=start_time,
            end_time=end_time,
            max_results=max_results,
            bearer_token=bearer_token,
        )
        
        click.echo(f"Found {len(tweet_list)} tweets")
        
        if not no_index:
            click.echo("Indexing tweets into OpenSearch...")
            result = index_tweets(tweet_list)
            click.echo(f"Indexed {result['success']} tweets into '{result['index']}'")
            if result['failed'] > 0:
                click.echo(f"Failed to index {result['failed']} tweets", err=True)
        else:
            for i, tweet in enumerate(tweet_list, 1):
                click.echo(f"\n{i}. @{tweet['username']} ({tweet['created_at']})")
                click.echo(f"   {tweet['text']}")
                click.echo(f"   Likes: {tweet['like_count']}, Retweets: {tweet['retweet_count']}")
                click.echo(f"   URL: {tweet['url']}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
