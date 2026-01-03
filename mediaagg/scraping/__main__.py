"""
CLI for scraping module.
"""

import sys
import argparse
from .html import scrape_html


def scrape_command(args):
    """Scrape a web page and save all artifacts."""
    try:
        print(f"Scraping URL: {args.url}")
        article_folder = scrape_html(args.url, source_name=args.source)
        print(f"\nArticle folder: {article_folder}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cli():
    """Media Aggregator - Web scraping tool."""
    parser = argparse.ArgumentParser(
        description="Media Aggregator - Web scraping tool"
    )
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument(
        "-s", "--source",
        default="scraped",
        help="Source name for organizing scraped content (default: scraped)"
    )
    
    args = parser.parse_args()
    scrape_command(args)


if __name__ == "__main__":
    cli()
