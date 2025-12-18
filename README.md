# Media Aggregator

A comprehensive media aggregation and analysis platform for scraping, indexing, and analyzing news articles and social media posts.

## Overview

This project provides tools and documentation for:
- Fetching news articles from various sources (APIs and web scraping)
- Indexing media content in OpenSearch
- Analyzing content using AI/NLP for topics, sentiment, bias, entities, and events

## Documentation

See [MEDIA_AGGREGATION_GUIDE.md](MEDIA_AGGREGATION_GUIDE.md) for detailed information on:

1. **News Aggregation APIs** - NewsAPI, The Guardian, New York Times, and more
   - Features comparison
   - Sign-up and API key processes
   - Sample code snippets

2. **Web Scraping Alternatives** - Reddit, Twitter/X, RSS feeds, and custom scrapers
   - Tools and libraries (BeautifulSoup, Newspaper3k, Playwright)
   - High-profile aggregator sources

3. **APIs vs Web Scraping** - Comparison and recommendations

4. **OpenSearch Integration** - Indexing and searching media content

5. **Python Libraries for AI/NLP** - spaCy, Transformers, NLTK, OpenAI GPT
   - Entity recognition
   - Sentiment analysis
   - Topic classification
   - Bias detection
   - Text summarization

6. **Example Workflows** - Complete pipelines and monitoring systems

## Getting Started

### Python Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/medium-tech/media-aggregator.git
   cd media-aggregator
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   # Using venv (Python 3.9+)
   python3 -m venv venv
   
   # Activate on Linux/macOS
   source venv/bin/activate
   
   # Activate on Windows
   venv\Scripts\activate
   ```

3. **Install the package:**
   ```bash
   pip install -e .
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

### Setting Up API Accounts and Keys

The media aggregator uses several APIs for fetching news articles and social media posts. You'll need to create accounts and obtain API keys for each service you want to use.

#### 1. New York Times API

**Sign-up Process:**
1. Visit [https://developer.nytimes.com/accounts/create](https://developer.nytimes.com/accounts/create)
2. Create an account with your email
3. Verify your email address
4. Create an app in the developer portal
5. Enable the Article Search API
6. Copy your API key and add it to `.env` as `NYTIMES_API_KEY`

**API Documentation:** [https://developer.nytimes.com/docs/articlesearch-product/1/overview](https://developer.nytimes.com/docs/articlesearch-product/1/overview)

**Rate Limits:** 4,000 requests/day, 500 requests/minute

**Licensing:** Free for non-commercial use. Review [Terms of Service](https://developer.nytimes.com/terms) for commercial use.

#### 2. Mediastack API

**Sign-up Process:**
1. Visit [https://mediastack.com/product](https://mediastack.com/product)
2. Sign up for a free account
3. Receive API key immediately
4. Add it to `.env` as `MEDIASTACK_API_KEY`

**API Documentation:** [https://mediastack.com/documentation](https://mediastack.com/documentation)

**Rate Limits:**
- Free: 500 requests/month
- Basic: 10,000 requests/month ($9.99/month)
- Professional: 100,000 requests/month ($49.99/month)

**Licensing:** Review [Terms of Use](https://mediastack.com/terms) for usage guidelines.

#### 3. GNews (Google News) API

**Sign-up Process:**
1. Visit [https://gnews.io/](https://gnews.io/)
2. Register with your email
3. Receive API key instantly
4. Add it to `.env` as `GNEWS_API_KEY`

**API Documentation:** [https://gnews.io/docs/v4](https://gnews.io/docs/v4)

**Rate Limits:**
- Free: 100 requests/day
- Basic: 10,000 requests/month ($9/month)
- Pro: 50,000 requests/month ($29/month)

**Licensing:** Review [Terms of Service](https://gnews.io/terms) for usage restrictions.

#### 4. Twitter/X API

**Sign-up Process:**
1. Visit [https://developer.twitter.com/](https://developer.twitter.com/)
2. Apply for a developer account
3. Create a new app in the developer portal
4. Generate a Bearer Token
5. Add it to `.env` as `TWITTER_BEARER_TOKEN`

**API Documentation:** [https://developer.twitter.com/en/docs/twitter-api](https://developer.twitter.com/en/docs/twitter-api)

**Rate Limits:**
- Free tier: 1,500 tweets/month (Essential access)
- Basic: $100/month for 10,000 tweets/month
- Pro: Custom pricing

**Licensing:** Review [Twitter Developer Agreement](https://developer.twitter.com/en/developer-terms/agreement) for usage terms.

#### 5. OpenSearch Setup

**For local development:**

1. **Using Docker (recommended):**
   ```bash
   docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" \
     -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=Admin123!" \
     opensearchproject/opensearch:latest
   ```

2. **Configure in `.env`:**
   ```
   OPENSEARCH_HOST=localhost
   OPENSEARCH_PORT=9200
   OPENSEARCH_USERNAME=admin
   OPENSEARCH_PASSWORD=Admin123!
   OPENSEARCH_USE_SSL=false
   ```

**OpenSearch Documentation:** [https://opensearch.org/docs/latest/](https://opensearch.org/docs/latest/)

### Usage

#### Fetching News Articles

The package provides CLI commands for fetching articles from different sources:

**NY Times:**
```bash
# Fetch articles by query
mediaagg-articles nytimes --query "artificial intelligence"

# With date filtering (YYYYMMDD format)
mediaagg-articles nytimes --query "climate change" --begin-date 20240101 --end-date 20241231

# Print without indexing
mediaagg-articles nytimes --query "technology" --no-index
```

**Mediastack:**
```bash
# Fetch by keywords
mediaagg-articles mediastack --keywords "technology"

# With country and category filters
mediaagg-articles mediastack --keywords "election" --countries "us" --categories "politics"

# With date range (YYYY-MM-DD format)
mediaagg-articles mediastack --keywords "AI" --date-from 2024-01-01 --date-to 2024-12-31
```

**Google News (GNews):**
```bash
# Fetch by query
mediaagg-articles gnews --query "machine learning"

# Fetch by category
mediaagg-articles gnews --category "technology" --max-results 50

# With language and country
mediaagg-articles gnews --query "sports" --lang "en" --country "us"
```

#### Fetching Social Media Posts

**Twitter/X:**
```bash
# Fetch tweets from a user
mediaagg-socials tweets elonmusk --max-results 50

# With date filtering (ISO 8601 format)
mediaagg-socials tweets nytimes --start-time "2024-01-01T00:00:00Z" --end-time "2024-12-31T23:59:59Z"

# Print without indexing
mediaagg-socials tweets nasa --no-index
```

### Python API Usage

You can also use the package programmatically:

```python
from mediaagg.articles import fetch_nytimes, fetch_mediastack, fetch_gnews, index_articles
from mediaagg.socials import fetch_tweets, index_tweets

# Fetch articles
articles = fetch_nytimes(query="technology", begin_date="20240101")
index_articles(articles, source_name="nytimes")

# Fetch tweets
tweets = fetch_tweets(username="elonmusk", max_results=100)
index_tweets(tweets)
```

### OpenSearch Indices

Articles are automatically indexed into source-specific indices:
- `articles-nytimes` - NY Times articles
- `articles-mediastack` - Mediastack articles
- `articles-gnews` - Google News articles
- `tweets` - Twitter/X posts

### Additional Resources

For more detailed information about news aggregation, web scraping, and AI/NLP processing:
- See [MEDIA_AGGREGATION_GUIDE.md](MEDIA_AGGREGATION_GUIDE.md) for comprehensive documentation
- Includes API comparisons, sample code, and complete pipeline examples

## License

See [LICENSE](LICENSE) for details.
