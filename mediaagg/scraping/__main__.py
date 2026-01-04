"""
CLI for scraping module.
"""

import sys
import argparse
from .html import scrape_html


def scrape_command(args):
    """Scrape a web page and save all artifacts."""

    print(f"Scraping URL: {args.url}")
    article_folder = scrape_html(args.url, source_name=args.source, screenshot=args.screenshot)
    print(f"\nArticle folder: {article_folder}")


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
    parser.add_argument(
        "--no-screenshot",
        "-ns",
        action="store_false",
        dest="screenshot",
        help="Disable screenshot rendering and OCR extraction"
    )
    
    args = parser.parse_args()
    scrape_command(args)


if __name__ == "__main__":
    cli()
