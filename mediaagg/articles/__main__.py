"""
CLI for articles module.
"""

import os
import click
from dotenv import load_dotenv
from .fetchers import fetch_nytimes, fetch_mediastack, fetch_gnews
from .indexer import index_articles


# Load environment variables
load_dotenv()


@click.group()
def cli():
    """Media Aggregator - Articles fetcher and indexer."""
    pass


@cli.command()
@click.option("--query", "-q", help="Search query")
@click.option("--begin-date", help="Begin date (YYYYMMDD format)")
@click.option("--end-date", help="End date (YYYYMMDD format)")
@click.option("--api-key", envvar="NYTIMES_API_KEY", help="NY Times API key")
@click.option("--no-index", is_flag=True, help="Don't index results, just print them")
def nytimes(query, begin_date, end_date, api_key, no_index):
    """Fetch articles from NY Times API."""
    try:
        click.echo(f"Fetching articles from NY Times...")
        articles = fetch_nytimes(
            query=query,
            begin_date=begin_date,
            end_date=end_date,
            api_key=api_key,
        )
        
        click.echo(f"Found {len(articles)} articles")
        
        if not no_index:
            click.echo("Indexing articles into OpenSearch...")
            result = index_articles(articles, "nytimes")
            click.echo(f"Indexed {result['success']} articles into '{result['index']}'")
            if result['failed'] > 0:
                click.echo(f"Failed to index {result['failed']} articles", err=True)
        else:
            for i, article in enumerate(articles, 1):
                click.echo(f"\n{i}. {article['title']}")
                click.echo(f"   URL: {article['url']}")
                click.echo(f"   Published: {article['published_date']}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--keywords", "-k", help="Keywords to search for")
@click.option("--countries", help="Comma-separated country codes (e.g., 'us,gb')")
@click.option("--categories", "-c", help="Comma-separated categories")
@click.option("--date-from", help="Start date (YYYY-MM-DD format)")
@click.option("--date-to", help="End date (YYYY-MM-DD format)")
@click.option("--limit", default=100, help="Maximum number of results")
@click.option("--api-key", envvar="MEDIASTACK_API_KEY", help="Mediastack API key")
@click.option("--no-index", is_flag=True, help="Don't index results, just print them")
def mediastack(keywords, countries, categories, date_from, date_to, limit, api_key, no_index):
    """Fetch articles from Mediastack API."""
    try:
        click.echo(f"Fetching articles from Mediastack...")
        articles = fetch_mediastack(
            keywords=keywords,
            countries=countries,
            categories=categories,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            api_key=api_key,
        )
        
        click.echo(f"Found {len(articles)} articles")
        
        if not no_index:
            click.echo("Indexing articles into OpenSearch...")
            result = index_articles(articles, "mediastack")
            click.echo(f"Indexed {result['success']} articles into '{result['index']}'")
            if result['failed'] > 0:
                click.echo(f"Failed to index {result['failed']} articles", err=True)
        else:
            for i, article in enumerate(articles, 1):
                click.echo(f"\n{i}. {article['title']}")
                click.echo(f"   URL: {article['url']}")
                click.echo(f"   Published: {article['published_date']}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--query", "-q", help="Search query")
@click.option("--category", help="News category (e.g., 'technology', 'business')")
@click.option("--lang", default="en", help="Language code (default: en)")
@click.option("--country", default="us", help="Country code (default: us)")
@click.option("--max-results", default=10, help="Maximum number of results")
@click.option("--from-date", help="Start date (ISO format)")
@click.option("--to-date", help="End date (ISO format)")
@click.option("--api-key", envvar="GNEWS_API_KEY", help="GNews API key")
@click.option("--no-index", is_flag=True, help="Don't index results, just print them")
def gnews(query, category, lang, country, max_results, from_date, to_date, api_key, no_index):
    """Fetch articles from Google News (GNews) API."""
    try:
        click.echo(f"Fetching articles from Google News...")
        articles = fetch_gnews(
            query=query,
            category=category,
            lang=lang,
            country=country,
            max_results=max_results,
            from_date=from_date,
            to_date=to_date,
            api_key=api_key,
        )
        
        click.echo(f"Found {len(articles)} articles")
        
        if not no_index:
            click.echo("Indexing articles into OpenSearch...")
            result = index_articles(articles, "gnews")
            click.echo(f"Indexed {result['success']} articles into '{result['index']}'")
            if result['failed'] > 0:
                click.echo(f"Failed to index {result['failed']} articles", err=True)
        else:
            for i, article in enumerate(articles, 1):
                click.echo(f"\n{i}. {article['title']}")
                click.echo(f"   URL: {article['url']}")
                click.echo(f"   Published: {article['published_date']}")
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
