"""
CLI for articles module.
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from .fetchers import fetch_nytimes, fetch_mediastack, fetch_gnews
from .indexer import index_articles
from mediaagg.storage import load_all_data, get_source_dir


# Load environment variables
load_dotenv()


def nytimes_command(args):
    """Fetch articles from NY Times API and save to disk."""
    try:
        print(f"Fetching articles from NY Times...")
        # Use provided API key or fall back to environment variable
        api_key = args.api_key or os.getenv("NYTIMES_API_KEY")
        fetch_nytimes(
            query=args.query,
            begin_date=args.begin_date,
            end_date=args.end_date,
            api_key=api_key,
            save_to_disk=True,
        )
        
        # Count saved files
        source_dir = get_source_dir("nytimes")
        saved_count = len(list(source_dir.glob("*.json")))
        print(f"Saved {saved_count} articles to {source_dir}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def mediastack_command(args):
    """Fetch articles from Mediastack API and save to disk."""
    try:
        print(f"Fetching articles from Mediastack...")
        # Use provided API key or fall back to environment variable
        api_key = args.api_key or os.getenv("MEDIASTACK_API_KEY")
        fetch_mediastack(
            keywords=args.keywords,
            countries=args.countries,
            categories=args.categories,
            date_from=args.date_from,
            date_to=args.date_to,
            limit=args.limit,
            api_key=api_key,
            save_to_disk=True,
        )
        
        # Count saved files
        source_dir = get_source_dir("mediastack")
        saved_count = len(list(source_dir.glob("*.json")))
        print(f"Saved {saved_count} articles to {source_dir}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def gnews_command(args):
    """Fetch articles from Google News (GNews) API and save to disk."""
    try:
        print(f"Fetching articles from Google News...")
        # Use provided API key or fall back to environment variable
        api_key = args.api_key or os.getenv("GNEWS_API_KEY")
        fetch_gnews(
            query=args.query,
            category=args.category,
            lang=args.lang,
            country=args.country,
            max_results=args.max_results,
            from_date=args.from_date,
            to_date=args.to_date,
            api_key=api_key,
            save_to_disk=True,
        )
        
        # Count saved files
        source_dir = get_source_dir("gnews")
        saved_count = len(list(source_dir.glob("*.json")))
        print(f"Saved {saved_count} articles to {source_dir}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def index_command(args):
    """Index articles from disk into OpenSearch."""
    try:
        source_name = args.source
        print(f"Loading articles from disk for source: {source_name}...")
        
        articles = load_all_data(source_name)
        if not articles:
            print(f"No articles found for source: {source_name}")
            sys.exit(1)
        
        print(f"Loaded {len(articles)} articles")
        print("Indexing articles into OpenSearch...")
        
        result = index_articles(articles, source_name)
        print(f"Indexed {result['success']} articles into '{result['index']}'")
        if result['failed'] > 0:
            print(f"Failed to index {result['failed']} articles", file=sys.stderr)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cli():
    """Media Aggregator - Articles fetcher and indexer."""
    parser = argparse.ArgumentParser(
        description="Media Aggregator - Articles fetcher and indexer"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # NY Times command
    nytimes_parser = subparsers.add_parser("nytimes", help="Fetch articles from NY Times API and save to disk")
    nytimes_parser.add_argument("-q", "--query", help="Search query")
    nytimes_parser.add_argument("--begin-date", help="Begin date (YYYYMMDD format)")
    nytimes_parser.add_argument("--end-date", help="End date (YYYYMMDD format)")
    nytimes_parser.add_argument("--api-key", help="NY Times API key (defaults to NYTIMES_API_KEY env var)")
    nytimes_parser.set_defaults(func=nytimes_command)
    
    # Mediastack command
    mediastack_parser = subparsers.add_parser("mediastack", help="Fetch articles from Mediastack API and save to disk")
    mediastack_parser.add_argument("-k", "--keywords", help="Keywords to search for")
    mediastack_parser.add_argument("--countries", help="Comma-separated country codes (e.g., 'us,gb')")
    mediastack_parser.add_argument("-c", "--categories", help="Comma-separated categories")
    mediastack_parser.add_argument("--date-from", help="Start date (YYYY-MM-DD format)")
    mediastack_parser.add_argument("--date-to", help="End date (YYYY-MM-DD format)")
    mediastack_parser.add_argument("--limit", type=int, default=100, help="Maximum number of results")
    mediastack_parser.add_argument("--api-key", help="Mediastack API key (defaults to MEDIASTACK_API_KEY env var)")
    mediastack_parser.set_defaults(func=mediastack_command)
    
    # GNews command
    gnews_parser = subparsers.add_parser("gnews", help="Fetch articles from Google News (GNews) API and save to disk")
    gnews_parser.add_argument("-q", "--query", help="Search query")
    gnews_parser.add_argument("--category", help="News category (e.g., 'technology', 'business')")
    gnews_parser.add_argument("--lang", default="en", help="Language code (default: en)")
    gnews_parser.add_argument("--country", default="us", help="Country code (default: us)")
    gnews_parser.add_argument("--max-results", type=int, default=10, help="Maximum number of results")
    gnews_parser.add_argument("--from-date", help="Start date (ISO format)")
    gnews_parser.add_argument("--to-date", help="End date (ISO format)")
    gnews_parser.add_argument("--api-key", help="GNews API key (defaults to GNEWS_API_KEY env var)")
    gnews_parser.set_defaults(func=gnews_command)
    
    # Index command
    index_parser = subparsers.add_parser("index", help="Index articles from disk into OpenSearch")
    index_parser.add_argument("source", help="Source name (e.g., 'nytimes', 'mediastack', 'gnews')")
    index_parser.set_defaults(func=index_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    cli()
