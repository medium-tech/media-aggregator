"""
CLI for articles module.
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from .fetchers import fetch_nytimes, fetch_mediastack, fetch_gnews
from .indexer import index_articles


# Load environment variables
load_dotenv()


def nytimes_command(args):
    """Fetch articles from NY Times API."""
    try:
        print(f"Fetching articles from NY Times...")
        articles = fetch_nytimes(
            query=args.query,
            begin_date=args.begin_date,
            end_date=args.end_date,
            api_key=args.api_key,
        )
        
        print(f"Found {len(articles)} articles")
        
        if not args.no_index:
            print("Indexing articles into OpenSearch...")
            result = index_articles(articles, "nytimes")
            print(f"Indexed {result['success']} articles into '{result['index']}'")
            if result['failed'] > 0:
                print(f"Failed to index {result['failed']} articles", file=sys.stderr)
        else:
            for i, article in enumerate(articles, 1):
                print(f"\n{i}. {article['title']}")
                print(f"   URL: {article['url']}")
                print(f"   Published: {article['published_date']}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def mediastack_command(args):
    """Fetch articles from Mediastack API."""
    try:
        print(f"Fetching articles from Mediastack...")
        articles = fetch_mediastack(
            keywords=args.keywords,
            countries=args.countries,
            categories=args.categories,
            date_from=args.date_from,
            date_to=args.date_to,
            limit=args.limit,
            api_key=args.api_key,
        )
        
        print(f"Found {len(articles)} articles")
        
        if not args.no_index:
            print("Indexing articles into OpenSearch...")
            result = index_articles(articles, "mediastack")
            print(f"Indexed {result['success']} articles into '{result['index']}'")
            if result['failed'] > 0:
                print(f"Failed to index {result['failed']} articles", file=sys.stderr)
        else:
            for i, article in enumerate(articles, 1):
                print(f"\n{i}. {article['title']}")
                print(f"   URL: {article['url']}")
                print(f"   Published: {article['published_date']}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def gnews_command(args):
    """Fetch articles from Google News (GNews) API."""
    try:
        print(f"Fetching articles from Google News...")
        articles = fetch_gnews(
            query=args.query,
            category=args.category,
            lang=args.lang,
            country=args.country,
            max_results=args.max_results,
            from_date=args.from_date,
            to_date=args.to_date,
            api_key=args.api_key,
        )
        
        print(f"Found {len(articles)} articles")
        
        if not args.no_index:
            print("Indexing articles into OpenSearch...")
            result = index_articles(articles, "gnews")
            print(f"Indexed {result['success']} articles into '{result['index']}'")
            if result['failed'] > 0:
                print(f"Failed to index {result['failed']} articles", file=sys.stderr)
        else:
            for i, article in enumerate(articles, 1):
                print(f"\n{i}. {article['title']}")
                print(f"   URL: {article['url']}")
                print(f"   Published: {article['published_date']}")
    
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
    nytimes_parser = subparsers.add_parser("nytimes", help="Fetch articles from NY Times API")
    nytimes_parser.add_argument("-q", "--query", help="Search query")
    nytimes_parser.add_argument("--begin-date", help="Begin date (YYYYMMDD format)")
    nytimes_parser.add_argument("--end-date", help="End date (YYYYMMDD format)")
    nytimes_parser.add_argument("--api-key", default=os.getenv("NYTIMES_API_KEY"), help="NY Times API key")
    nytimes_parser.add_argument("--no-index", action="store_true", help="Don't index results, just print them")
    nytimes_parser.set_defaults(func=nytimes_command)
    
    # Mediastack command
    mediastack_parser = subparsers.add_parser("mediastack", help="Fetch articles from Mediastack API")
    mediastack_parser.add_argument("-k", "--keywords", help="Keywords to search for")
    mediastack_parser.add_argument("--countries", help="Comma-separated country codes (e.g., 'us,gb')")
    mediastack_parser.add_argument("-c", "--categories", help="Comma-separated categories")
    mediastack_parser.add_argument("--date-from", help="Start date (YYYY-MM-DD format)")
    mediastack_parser.add_argument("--date-to", help="End date (YYYY-MM-DD format)")
    mediastack_parser.add_argument("--limit", type=int, default=100, help="Maximum number of results")
    mediastack_parser.add_argument("--api-key", default=os.getenv("MEDIASTACK_API_KEY"), help="Mediastack API key")
    mediastack_parser.add_argument("--no-index", action="store_true", help="Don't index results, just print them")
    mediastack_parser.set_defaults(func=mediastack_command)
    
    # GNews command
    gnews_parser = subparsers.add_parser("gnews", help="Fetch articles from Google News (GNews) API")
    gnews_parser.add_argument("-q", "--query", help="Search query")
    gnews_parser.add_argument("--category", help="News category (e.g., 'technology', 'business')")
    gnews_parser.add_argument("--lang", default="en", help="Language code (default: en)")
    gnews_parser.add_argument("--country", default="us", help="Country code (default: us)")
    gnews_parser.add_argument("--max-results", type=int, default=10, help="Maximum number of results")
    gnews_parser.add_argument("--from-date", help="Start date (ISO format)")
    gnews_parser.add_argument("--to-date", help="End date (ISO format)")
    gnews_parser.add_argument("--api-key", default=os.getenv("GNEWS_API_KEY"), help="GNews API key")
    gnews_parser.add_argument("--no-index", action="store_true", help="Don't index results, just print them")
    gnews_parser.set_defaults(func=gnews_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    cli()
