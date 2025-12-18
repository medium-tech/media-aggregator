# Media Aggregation and Analysis Guide

This guide provides comprehensive information about news aggregation APIs, web scraping alternatives, and AI/NLP processing techniques for analyzing media content.

## Table of Contents
1. [News Aggregation APIs](#news-aggregation-apis)
2. [Web Scraping Alternatives](#web-scraping-alternatives)
3. [APIs vs Web Scraping Comparison](#apis-vs-web-scraping-comparison)
4. [OpenSearch Integration](#opensearch-integration)
5. [Python Libraries for AI/NLP Processing](#python-libraries-for-ainlp-processing)
6. [Example Workflows](#example-workflows)

---

## News Aggregation APIs

### 1. NewsAPI.org

**Overview:**
NewsAPI provides access to news articles from over 80,000 sources worldwide, including major publications and blogs.

**Features:**
- Search news articles by keyword, phrase, or source
- Filter by date, language, country, and category
- Access headlines and full article text
- Historical data available (with paid plans)
- Support for 14 languages
- Returns article title, description, content snippet, URL, images, and metadata

**Content Delivery:**
- Provides article title, description, and a content snippet (~200 characters)
- **Note:** Full article text is NOT provided; you'll need to scrape the source URL for complete content
- Returns clean metadata including author, publish date, source name, and URL

**Sign-up Process:**
1. Visit https://newsapi.org/register
2. Create a free account with email
3. Verify email address
4. Navigate to your account dashboard
5. Copy your API key from the dashboard

**Pricing:**
- Free: 100 requests/day, limited to developer testing
- Business: $449/month for production use
- Mega: Custom pricing for enterprise needs

**Sample Code:**

```python
import requests
from datetime import datetime, timedelta

API_KEY = 'your_api_key_here'
BASE_URL = 'https://newsapi.org/v2'

# Get top headlines
def get_top_headlines(country='us', category=None):
    url = f'{BASE_URL}/top-headlines'
    params = {
        'apiKey': API_KEY,
        'country': country,
        'pageSize': 100
    }
    if category:
        params['category'] = category
    
    response = requests.get(url, params=params)
    return response.json()

# Search articles by keyword
def search_articles(query, from_date=None, sort_by='relevancy'):
    url = f'{BASE_URL}/everything'
    
    if not from_date:
        from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    params = {
        'apiKey': API_KEY,
        'q': query,
        'from': from_date,
        'sortBy': sort_by,
        'language': 'en',
        'pageSize': 100
    }
    
    response = requests.get(url, params=params)
    return response.json()

# Example usage
if __name__ == '__main__':
    # Get tech headlines
    headlines = get_top_headlines(category='technology')
    
    for article in headlines.get('articles', []):
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']['name']}")
        print(f"URL: {article['url']}")
        print(f"Published: {article['publishedAt']}")
        print(f"Description: {article['description']}")
        print('-' * 80)
    
    # Search for specific topics
    results = search_articles('artificial intelligence')
    print(f"Found {results['totalResults']} articles")
```

---

### 2. The Guardian API

**Overview:**
The Guardian's open platform provides access to all articles from 1999 to present from The Guardian newspaper.

**Features:**
- Access to over 2.3 million pieces of content
- Search by keyword, section, tag, and date
- Free for non-commercial use
- Returns full article body text (in blocks/paragraphs)
- Excellent metadata and tagging system
- No rate limits for most use cases (12 calls per second, 5000 per day for developers)

**Content Delivery:**
- **Provides full article text** when using the `show-fields=bodyText` parameter
- Also provides structured content blocks with `show-blocks=all`
- Excellent for getting complete articles without additional scraping

**Sign-up Process:**
1. Visit https://open-platform.theguardian.com/access/
2. Register with email
3. Receive API key instantly via email
4. No credit card required

**Pricing:**
- Free: 5,000 requests/day (sufficient for most projects)
- Commercial: Contact for licensing

**Sample Code:**

```python
import requests

API_KEY = 'your_guardian_api_key'
BASE_URL = 'https://content.guardianapis.com'

def search_guardian(query, from_date=None, page_size=50):
    url = f'{BASE_URL}/search'
    params = {
        'api-key': API_KEY,
        'q': query,
        'page-size': page_size,
        'show-fields': 'bodyText,headline,thumbnail,byline',
        'show-tags': 'keyword',
        'order-by': 'relevance'
    }
    
    if from_date:
        params['from-date'] = from_date
    
    response = requests.get(url, params=params)
    return response.json()

# Get full article content
def get_article(article_id):
    url = f'{BASE_URL}/{article_id}'
    params = {
        'api-key': API_KEY,
        'show-fields': 'bodyText,headline,thumbnail,byline',
        'show-blocks': 'all'
    }
    
    response = requests.get(url, params=params)
    return response.json()

# Example usage
if __name__ == '__main__':
    results = search_guardian('climate change', from_date='2024-01-01')
    
    for result in results['response']['results']:
        print(f"Title: {result['webTitle']}")
        print(f"URL: {result['webUrl']}")
        print(f"Published: {result['webPublicationDate']}")
        
        # Full article text is in fields
        if 'fields' in result and 'bodyText' in result['fields']:
            text = result['fields']['bodyText']
            print(f"Article length: {len(text)} characters")
            print(f"Preview: {text[:200]}...")
        
        print('-' * 80)
```

---

### 3. New York Times API

**Overview:**
The New York Times offers multiple APIs for accessing their content, including articles, best sellers, movie reviews, and more.

**Features:**
- Article Search API with archive from 1851
- Top Stories API for current headlines
- Most Popular API
- Rich metadata including keywords, people, organizations
- Semantic API for categorized content
- 4,000 requests per day (500 per minute rate limit)

**Content Delivery:**
- Provides lead paragraph and snippet
- **Full article text NOT provided** - must visit URL
- Excellent metadata and tagging

**Sign-up Process:**
1. Visit https://developer.nytimes.com/accounts/create
2. Create account with email
3. Verify email
4. Create an app in the developer portal
5. Enable desired APIs
6. Copy API key for each enabled API

**Pricing:**
- Free: 4,000 requests/day per API
- All APIs are currently free with rate limits

**Sample Code:**

```python
import requests
from datetime import datetime

API_KEY = 'your_nyt_api_key'

# Article Search API
def search_nyt_articles(query, begin_date=None, end_date=None):
    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    params = {
        'api-key': API_KEY,
        'q': query,
        'sort': 'relevance'
    }
    
    if begin_date:
        params['begin_date'] = begin_date  # Format: YYYYMMDD
    if end_date:
        params['end_date'] = end_date
    
    response = requests.get(url, params=params)
    return response.json()

# Top Stories API
def get_top_stories(section='home'):
    url = f'https://api.nytimes.com/svc/topstories/v2/{section}.json'
    params = {'api-key': API_KEY}
    
    response = requests.get(url, params=params)
    return response.json()

# Example usage
if __name__ == '__main__':
    # Search articles
    results = search_nyt_articles('artificial intelligence', begin_date='20240101')
    
    for doc in results['response']['docs']:
        print(f"Headline: {doc['headline']['main']}")
        print(f"Lead Paragraph: {doc['lead_paragraph']}")
        print(f"URL: {doc['web_url']}")
        print(f"Published: {doc['pub_date']}")
        print(f"Keywords: {[kw['value'] for kw in doc.get('keywords', [])]}")
        print('-' * 80)
    
    # Get top stories
    stories = get_top_stories('technology')
    for story in stories['results']:
        print(f"Title: {story['title']}")
        print(f"Abstract: {story['abstract']}")
        print(f"URL: {story['url']}")
```

---

### 4. Mediastack API

**Overview:**
Mediastack provides real-time news data from over 75,000 sources worldwide with simple REST API access.

**Features:**
- Global news coverage from 50+ countries
- Historical news data
- 50+ languages supported
- Filter by source, country, category, sentiment
- News sources include major publications and blogs

**Content Delivery:**
- Provides article descriptions
- **Full text NOT included** - need to scrape source URL
- Good metadata coverage

**Sign-up Process:**
1. Visit https://mediastack.com/product
2. Sign up for free account
3. Receive API key immediately
4. No credit card required for free tier

**Pricing:**
- Free: 500 requests/month
- Basic: $9.99/month for 10,000 requests
- Professional: $49.99/month for 100,000 requests

**Sample Code:**

```python
import requests

API_KEY = 'your_mediastack_api_key'
BASE_URL = 'http://api.mediastack.com/v1'

def get_news(keywords=None, countries=None, categories=None, limit=100):
    url = f'{BASE_URL}/news'
    params = {
        'access_key': API_KEY,
        'limit': limit,
        'sort': 'published_desc',
        'languages': 'en'
    }
    
    if keywords:
        params['keywords'] = keywords
    if countries:
        params['countries'] = countries
    if categories:
        params['categories'] = categories
    
    response = requests.get(url, params=params)
    return response.json()

# Example usage
if __name__ == '__main__':
    news = get_news(keywords='technology', countries='us', categories='technology')
    
    for article in news['data']:
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Published: {article['published_at']}")
        print(f"URL: {article['url']}")
        print(f"Description: {article.get('description', 'N/A')}")
        print('-' * 80)
```

---

### 5. GNews API

**Overview:**
GNews aggregates articles from Google News with simple API access.

**Features:**
- Real-time news from Google News
- 60,000 sources worldwide
- Search by keyword, topic, language, country
- Fast response times
- Clean, structured data

**Content Delivery:**
- Provides title, description, and content snippet
- **Limited content provided** - full text requires scraping
- Focuses on metadata and headlines

**Sign-up Process:**
1. Visit https://gnews.io/
2. Register with email
3. Receive API key instantly
4. No credit card for free tier

**Pricing:**
- Free: 100 requests/day
- Basic: $9/month for 10,000 requests
- Pro: $29/month for 50,000 requests

**Sample Code:**

```python
import requests

API_KEY = 'your_gnews_api_key'
BASE_URL = 'https://gnews.io/api/v4'

def search_gnews(query, lang='en', country='us', max_results=10):
    url = f'{BASE_URL}/search'
    params = {
        'q': query,
        'lang': lang,
        'country': country,
        'max': max_results,
        'apikey': API_KEY
    }
    
    response = requests.get(url, params=params)
    return response.json()

def get_top_headlines(category=None, lang='en', country='us'):
    url = f'{BASE_URL}/top-headlines'
    params = {
        'lang': lang,
        'country': country,
        'apikey': API_KEY
    }
    
    if category:
        params['topic'] = category  # Options: breaking-news, world, nation, business, technology, entertainment, sports, science, health
    
    response = requests.get(url, params=params)
    return response.json()

# Example usage
if __name__ == '__main__':
    results = search_gnews('machine learning', max_results=20)
    
    for article in results['articles']:
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']['name']}")
        print(f"Published: {article['publishedAt']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}")
        print('-' * 80)
```

---

## Web Scraping Alternatives

### High-Profile News Aggregators to Consider

#### 1. **Google News**
- URL: https://news.google.com
- Aggregates from thousands of sources
- Organized by topics and regions
- **Challenges:** Dynamic JavaScript rendering, frequent structure changes, potential legal issues
- **Better Alternative:** Use GNews API instead

#### 2. **Reddit (News Subreddits)**
- URLs: r/news, r/worldnews, r/technology, etc.
- Community-curated news with discussions
- **Advantages:** PRAW API available, easy to access
- **Use Case:** Social media perspective on news

```python
import praw

# Reddit API (PRAW - Python Reddit API Wrapper)
reddit = praw.Reddit(
    client_id='your_client_id',
    client_secret='your_client_secret',
    user_agent='your_user_agent'
)

# Get posts from news subreddit
subreddit = reddit.subreddit('news')
for post in subreddit.hot(limit=100):
    print(f"Title: {post.title}")
    print(f"URL: {post.url}")
    print(f"Score: {post.score}")
    print(f"Comments: {post.num_comments}")
    print('-' * 80)
```

#### 3. **Twitter/X (News Accounts)**
- Follow major news outlets and journalists
- Real-time breaking news
- **Access:** Twitter API v2 (requires approval)
- **Use Case:** Real-time updates and trending topics

```python
import tweepy

# Twitter API v2
client = tweepy.Client(bearer_token='your_bearer_token')

# Search recent tweets
query = 'from:CNN OR from:BBCNews OR from:Reuters'
tweets = client.search_recent_tweets(query=query, max_results=100, 
                                     tweet_fields=['created_at', 'public_metrics'])

for tweet in tweets.data:
    print(f"Text: {tweet.text}")
    print(f"Created: {tweet.created_at}")
    print(f"Likes: {tweet.public_metrics['like_count']}")
```

#### 4. **RSS Feeds**
- Most news sites provide RSS feeds
- Simple XML parsing
- No API key required
- **Advantages:** Legal, reliable, standardized format

```python
import feedparser

# Parse RSS feeds
feeds = [
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'http://feeds.bbci.co.uk/news/rss.xml',
    'https://www.theguardian.com/world/rss',
    'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
]

def fetch_rss_feed(feed_url):
    feed = feedparser.parse(feed_url)
    
    articles = []
    for entry in feed.entries:
        articles.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.get('published', ''),
            'summary': entry.get('summary', '')
        })
    
    return articles

# Fetch from all feeds
all_articles = []
for feed_url in feeds:
    articles = fetch_rss_feed(feed_url)
    all_articles.extend(articles)
    print(f"Fetched {len(articles)} articles from {feed_url}")
```

### Web Scraping Tools and Libraries

When you need to scrape full article text from URLs (since most APIs don't provide it):

#### BeautifulSoup + Requests
```python
import requests
from bs4 import BeautifulSoup

def scrape_article(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Generic article extraction (adjust selectors per site)
    title = soup.find('h1').text if soup.find('h1') else ''
    
    # Try common article body containers
    article_body = (soup.find('article') or 
                   soup.find('div', class_='article-body') or
                   soup.find('div', class_='story-body'))
    
    if article_body:
        paragraphs = article_body.find_all('p')
        text = '\n'.join([p.text for p in paragraphs])
    else:
        text = ''
    
    return {'title': title, 'text': text, 'url': url}
```

#### Newspaper3k (Specialized for News)
```python
from newspaper import Article

def extract_article(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()  # Performs keyword extraction and summarization
    
    return {
        'title': article.title,
        'authors': article.authors,
        'publish_date': article.publish_date,
        'text': article.text,
        'top_image': article.top_image,
        'keywords': article.keywords,
        'summary': article.summary
    }

# Usage
url = 'https://www.example.com/news/article'
article_data = extract_article(url)
print(f"Title: {article_data['title']}")
print(f"Text length: {len(article_data['text'])} characters")
```

#### Playwright (For JavaScript-Heavy Sites)
```python
from playwright.sync_api import sync_playwright

def scrape_with_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        
        # Wait for content to load
        page.wait_for_selector('article', timeout=5000)
        
        # Extract content
        title = page.query_selector('h1').inner_text()
        article_text = page.query_selector('article').inner_text()
        
        browser.close()
        
        return {'title': title, 'text': article_text}
```

---

## APIs vs Web Scraping Comparison

| Aspect | News APIs | Web Scraping |
|--------|-----------|--------------|
| **Ease of Use** | Very easy - structured JSON responses | Requires parsing HTML, handling changes |
| **Reliability** | High - stable endpoints | Low - sites change structure frequently |
| **Legal Issues** | None - official access | Potential ToS violations, legal grey area |
| **Full Article Text** | Usually NO (except Guardian) | YES - can get full content |
| **Rate Limits** | Yes - typically 100-5000/day free | Only limited by your politeness/IP blocking |
| **Data Quality** | Clean, structured metadata | Raw HTML - requires cleaning |
| **Historical Data** | Often available (varies by API) | Must crawl/archive yourself |
| **Maintenance** | Minimal - API handles changes | High - adapt to site changes |
| **Cost** | Free tiers then paid | Free (but computing/proxy costs) |

**Recommendation:** 
- **Use APIs first** for metadata, headlines, and source URLs
- **Use web scraping** only when you need full article text that APIs don't provide
- **Best approach:** Combine both - get URLs from APIs, then scrape full content as needed

---

## OpenSearch Integration

### Setting Up OpenSearch for Media Indexing

```python
from opensearchpy import OpenSearch, helpers
from datetime import datetime
import json

# Initialize OpenSearch client
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_auth=('admin', 'admin'),
    use_ssl=False,
    verify_certs=False
)

# Create index with mapping
index_name = 'news-articles'

index_mapping = {
    'settings': {
        'number_of_shards': 2,
        'number_of_replicas': 1,
        'analysis': {
            'analyzer': {
                'english_analyzer': {
                    'type': 'english'
                }
            }
        }
    },
    'mappings': {
        'properties': {
            'title': {'type': 'text', 'analyzer': 'english_analyzer'},
            'content': {'type': 'text', 'analyzer': 'english_analyzer'},
            'summary': {'type': 'text', 'analyzer': 'english_analyzer'},
            'url': {'type': 'keyword'},
            'source': {'type': 'keyword'},
            'author': {'type': 'keyword'},
            'published_date': {'type': 'date'},
            'scraped_date': {'type': 'date'},
            'category': {'type': 'keyword'},
            'keywords': {'type': 'keyword'},
            'entities': {
                'type': 'nested',
                'properties': {
                    'text': {'type': 'keyword'},
                    'type': {'type': 'keyword'},
                    'sentiment': {'type': 'float'}
                }
            },
            'sentiment_score': {'type': 'float'},
            'bias_score': {'type': 'float'},
            'topics': {'type': 'keyword'}
        }
    }
}

# Create index
if not client.indices.exists(index=index_name):
    client.indices.create(index=index_name, body=index_mapping)

# Index a document
def index_article(article_data):
    doc = {
        'title': article_data['title'],
        'content': article_data['text'],
        'url': article_data['url'],
        'source': article_data['source'],
        'author': article_data.get('author', ''),
        'published_date': article_data['published_date'],
        'scraped_date': datetime.now().isoformat(),
        'category': article_data.get('category', ''),
        'keywords': article_data.get('keywords', [])
    }
    
    response = client.index(
        index=index_name,
        body=doc,
        refresh=True
    )
    return response

# Bulk indexing
def bulk_index_articles(articles):
    actions = []
    for article in articles:
        action = {
            '_index': index_name,
            '_source': {
                'title': article['title'],
                'content': article.get('text', ''),
                'url': article['url'],
                'source': article['source'],
                'published_date': article['published_date'],
                'scraped_date': datetime.now().isoformat()
            }
        }
        actions.append(action)
    
    helpers.bulk(client, actions)

# Search articles
def search_articles(query, size=10):
    search_body = {
        'query': {
            'multi_match': {
                'query': query,
                'fields': ['title^3', 'content', 'summary^2'],
                'type': 'best_fields'
            }
        },
        'highlight': {
            'fields': {
                'title': {},
                'content': {'fragment_size': 150}
            }
        },
        'size': size
    }
    
    results = client.search(index=index_name, body=search_body)
    return results['hits']['hits']

# Advanced search with filters
def advanced_search(query, source=None, date_from=None, topics=None):
    must_clauses = [
        {
            'multi_match': {
                'query': query,
                'fields': ['title', 'content']
            }
        }
    ]
    
    filter_clauses = []
    
    if source:
        filter_clauses.append({'term': {'source': source}})
    
    if date_from:
        filter_clauses.append({
            'range': {
                'published_date': {'gte': date_from}
            }
        })
    
    if topics:
        filter_clauses.append({'terms': {'topics': topics}})
    
    search_body = {
        'query': {
            'bool': {
                'must': must_clauses,
                'filter': filter_clauses
            }
        }
    }
    
    results = client.search(index=index_name, body=search_body)
    return results['hits']['hits']
```

---

## Python Libraries for AI/NLP Processing

### 1. spaCy - Industrial-Strength NLP

**Installation:**
```bash
pip install spacy
python -m spacy download en_core_web_sm  # Small model
python -m spacy download en_core_web_lg  # Large model with word vectors
```

**Features:**
- Named Entity Recognition (NER)
- Part-of-speech tagging
- Dependency parsing
- Word vectors and similarity
- Fast and production-ready

**Example - Entity Recognition and Topic Extraction:**
```python
import spacy
from collections import Counter

# Load model
nlp = spacy.load('en_core_web_lg')

def extract_entities(text):
    doc = nlp(text)
    
    entities = {
        'persons': [],
        'organizations': [],
        'locations': [],
        'dates': [],
        'events': []
    }
    
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            entities['persons'].append(ent.text)
        elif ent.label_ == 'ORG':
            entities['organizations'].append(ent.text)
        elif ent.label_ in ['GPE', 'LOC']:
            entities['locations'].append(ent.text)
        elif ent.label_ == 'DATE':
            entities['dates'].append(ent.text)
        elif ent.label_ == 'EVENT':
            entities['events'].append(ent.text)
    
    return entities

def extract_key_phrases(text, n=10):
    doc = nlp(text)
    
    # Extract noun chunks as key phrases
    phrases = [chunk.text for chunk in doc.noun_chunks]
    
    # Count frequency
    phrase_freq = Counter(phrases)
    
    return phrase_freq.most_common(n)

# Example usage
article_text = """
President Biden announced new climate policies on Monday.
The White House said the Environmental Protection Agency will 
implement stricter regulations. Microsoft and Google have pledged 
support for renewable energy initiatives.
"""

entities = extract_entities(article_text)
print("Entities found:")
print(f"People: {entities['persons']}")
print(f"Organizations: {entities['organizations']}")
print(f"Locations: {entities['locations']}")

key_phrases = extract_key_phrases(article_text)
print(f"\nKey phrases: {key_phrases}")
```

---

### 2. Hugging Face Transformers - State-of-the-Art Models

**Installation:**
```bash
pip install transformers torch
```

**Features:**
- Pre-trained models for various NLP tasks
- Sentiment analysis
- Text classification
- Question answering
- Summarization
- Zero-shot classification

**Example - Sentiment Analysis:**
```python
from transformers import pipeline

# Initialize sentiment analyzer
sentiment_analyzer = pipeline('sentiment-analysis', 
                             model='distilbert-base-uncased-finetuned-sst-2-english')

def analyze_sentiment(text):
    # Split into chunks if text is long (transformers have token limits)
    max_length = 512
    chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    
    results = []
    for chunk in chunks:
        if chunk.strip():
            result = sentiment_analyzer(chunk)[0]
            results.append(result)
    
    # Average sentiment across chunks
    if results:
        positive_scores = [r['score'] for r in results if r['label'] == 'POSITIVE']
        negative_scores = [r['score'] for r in results if r['label'] == 'NEGATIVE']
        
        if positive_scores:
            avg_positive = sum(positive_scores) / len(positive_scores)
        else:
            avg_positive = 0
            
        if negative_scores:
            avg_negative = sum(negative_scores) / len(negative_scores)
        else:
            avg_negative = 0
        
        return {
            'positive_score': avg_positive,
            'negative_score': avg_negative,
            'overall': 'POSITIVE' if avg_positive > avg_negative else 'NEGATIVE'
        }
    
    return None

# Example
article = "The new policy has been widely praised by experts and shows great promise."
sentiment = analyze_sentiment(article)
print(f"Sentiment: {sentiment}")
```

**Example - Zero-Shot Classification (Topic Detection):**
```python
from transformers import pipeline

# Zero-shot classification doesn't require training data
classifier = pipeline('zero-shot-classification', 
                     model='facebook/bart-large-mnli')

def classify_topics(text, candidate_labels):
    result = classifier(text, candidate_labels, multi_label=True)
    
    # Return topics with scores
    topics = []
    for label, score in zip(result['labels'], result['scores']):
        if score > 0.5:  # Threshold for relevance
            topics.append({'topic': label, 'confidence': score})
    
    return topics

# Example
article_text = """
Scientists have discovered a new method for detecting cancer early 
using artificial intelligence. The breakthrough could save millions 
of lives by enabling earlier treatment.
"""

topics = classify_topics(
    article_text,
    candidate_labels=['healthcare', 'technology', 'politics', 'sports', 
                     'science', 'business', 'entertainment']
)

print("Detected topics:")
for topic in topics:
    print(f"  {topic['topic']}: {topic['confidence']:.2f}")
```

**Example - Text Summarization:**
```python
from transformers import pipeline

summarizer = pipeline('summarization', model='facebook/bart-large-cnn')

def summarize_article(text, max_length=150, min_length=50):
    # BART has a max token limit, split if needed
    max_chunk = 1024
    
    if len(text) > max_chunk:
        # Summarize first chunk as a basic approach
        text = text[:max_chunk]
    
    summary = summarizer(text, max_length=max_length, 
                        min_length=min_length, do_sample=False)
    
    return summary[0]['summary_text']

# Example
long_article = """
[Long article text here...]
"""

summary = summarize_article(long_article)
print(f"Summary: {summary}")
```

---

### 3. NLTK - Natural Language Toolkit

**Installation:**
```bash
pip install nltk
```

**Setup:**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
```

**Example - Basic Text Analysis:**
```python
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
import string

def analyze_text(text):
    # Tokenize
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    filtered_words = [w for w in words 
                     if w not in stop_words and w not in string.punctuation]
    
    # Get most common words
    word_freq = Counter(filtered_words)
    
    # POS tagging
    pos_tags = pos_tag(words)
    
    # Extract nouns (potential topics)
    nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
    
    return {
        'sentence_count': len(sentences),
        'word_count': len(words),
        'unique_words': len(set(filtered_words)),
        'most_common_words': word_freq.most_common(10),
        'top_nouns': Counter(nouns).most_common(10)
    }

# Sentiment analysis with VADER
sia = SentimentIntensityAnalyzer()

def get_sentiment_vader(text):
    scores = sia.polarity_scores(text)
    return scores

# Example
article = """
The technology sector continues to innovate at a rapid pace.
Companies are investing heavily in artificial intelligence and
machine learning to stay competitive.
"""

analysis = analyze_text(article)
sentiment = get_sentiment_vader(article)

print("Text Analysis:")
print(f"Sentences: {analysis['sentence_count']}")
print(f"Words: {analysis['word_count']}")
print(f"Top words: {analysis['most_common_words']}")
print(f"\nSentiment: {sentiment}")
```

---

### 4. Bias Detection

**Using Transformers for Bias Detection:**
```python
from transformers import pipeline

# Use a model fine-tuned for bias detection or use zero-shot
bias_classifier = pipeline('zero-shot-classification',
                          model='facebook/bart-large-mnli')

def detect_bias(text):
    bias_types = [
        'politically neutral',
        'politically left-leaning',
        'politically right-leaning',
        'sensationalist',
        'factual and objective'
    ]
    
    result = bias_classifier(text, bias_types, multi_label=True)
    
    bias_scores = {}
    for label, score in zip(result['labels'], result['scores']):
        bias_scores[label] = score
    
    return bias_scores

# Example
article = """
The controversial new policy has sparked heated debate among citizens.
"""

bias = detect_bias(article)
print("Bias Analysis:")
for bias_type, score in bias.items():
    print(f"  {bias_type}: {score:.3f}")
```

**Media Bias Detection with Custom Features:**
```python
import spacy
from textblob import TextBlob

nlp = spacy.load('en_core_web_lg')

def advanced_bias_detection(text):
    doc = nlp(text)
    blob = TextBlob(text)
    
    # Sentiment subjectivity (0 = objective, 1 = subjective)
    subjectivity = blob.sentiment.subjectivity
    
    # Emotional words count
    emotional_words = ['shocking', 'outrageous', 'incredible', 'amazing', 
                      'terrible', 'horrible', 'devastating', 'alarming']
    emotional_count = sum(1 for token in doc if token.text.lower() in emotional_words)
    
    # Hedging words (may indicate caution/objectivity)
    hedging_words = ['may', 'might', 'could', 'possibly', 'perhaps', 
                    'allegedly', 'reportedly']
    hedging_count = sum(1 for token in doc if token.text.lower() in hedging_words)
    
    # Extreme adjectives
    extreme_adj = ['extreme', 'radical', 'insane', 'crazy', 'unprecedented']
    extreme_count = sum(1 for token in doc if token.text.lower() in extreme_adj)
    
    # Calculate bias score (0 = objective, 1 = highly biased)
    bias_score = (
        subjectivity * 0.4 +
        min(emotional_count / 10, 1) * 0.3 +
        min(extreme_count / 5, 1) * 0.2 -
        min(hedging_count / 5, 0.5) * 0.1
    )
    
    return {
        'bias_score': min(max(bias_score, 0), 1),
        'subjectivity': subjectivity,
        'emotional_word_count': emotional_count,
        'hedging_word_count': hedging_count,
        'extreme_adjective_count': extreme_count,
        'classification': 'objective' if bias_score < 0.3 
                         else 'slightly biased' if bias_score < 0.6 
                         else 'highly biased'
    }

# Example
text = "This absolutely shocking revelation shows the outrageous behavior..."
bias_analysis = advanced_bias_detection(text)
print(bias_analysis)
```

---

### 5. OpenAI GPT Models (Advanced Analysis)

**Installation:**
```bash
pip install openai
```

**Example - Using GPT for Complex Analysis:**
```python
from openai import OpenAI

# Initialize client (uses OPENAI_API_KEY environment variable by default)
client = OpenAI(api_key='your_openai_api_key')

def analyze_with_gpt(article_text, analysis_type='summary'):
    prompts = {
        'summary': f"Summarize the following news article in 2-3 sentences:\n\n{article_text}",
        
        'bias': f"Analyze the following article for political bias. Rate it as left-leaning, right-leaning, or neutral, and explain why:\n\n{article_text}",
        
        'topics': f"Extract the main topics and themes from this article. List them as bullet points:\n\n{article_text}",
        
        'entities': f"Extract all important people, organizations, locations, and events mentioned in this article:\n\n{article_text}",
        
        'fact_check': f"Identify claims in this article that should be fact-checked:\n\n{article_text}"
    }
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes news articles."},
            {"role": "user", "content": prompts.get(analysis_type, prompts['summary'])}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content

# Example usage
article = """
[Article text here...]
"""

summary = analyze_with_gpt(article, 'summary')
bias_analysis = analyze_with_gpt(article, 'bias')
topics = analyze_with_gpt(article, 'topics')

print(f"Summary: {summary}\n")
print(f"Bias Analysis: {bias_analysis}\n")
print(f"Topics: {topics}")
```

---

## Example Workflows

### Complete Pipeline: Fetch, Process, and Index

```python
import requests
from newspaper import Article
from transformers import pipeline
import spacy
from opensearchpy import OpenSearch
from datetime import datetime

# Initialize models
nlp = spacy.load('en_core_web_lg')
sentiment_analyzer = pipeline('sentiment-analysis')
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
topic_classifier = pipeline('zero-shot-classification', 
                            model='facebook/bart-large-mnli')

# Initialize OpenSearch
opensearch_client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_auth=('admin', 'admin'),
    use_ssl=False
)

def complete_article_pipeline(url, source_name):
    """
    Complete pipeline: fetch, extract, analyze, and index article
    """
    # Step 1: Fetch and extract article
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    
    # Step 2: Extract entities with spaCy
    doc = nlp(article.text)
    entities = {
        'persons': list(set([ent.text for ent in doc.ents if ent.label_ == 'PERSON'])),
        'organizations': list(set([ent.text for ent in doc.ents if ent.label_ == 'ORG'])),
        'locations': list(set([ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]))
    }
    
    # Step 3: Sentiment analysis
    try:
        sentiment = sentiment_analyzer(article.text[:512])[0]
        sentiment_score = sentiment['score'] if sentiment['label'] == 'POSITIVE' else -sentiment['score']
    except:
        sentiment_score = 0.0
    
    # Step 4: Topic classification
    candidate_topics = ['politics', 'technology', 'business', 'health', 
                       'science', 'sports', 'entertainment', 'world news']
    try:
        topics_result = topic_classifier(article.text[:512], candidate_topics, multi_label=True)
        topics = [label for label, score in zip(topics_result['labels'], topics_result['scores']) 
                 if score > 0.3]
    except:
        topics = []
    
    # Step 5: Create document for OpenSearch
    document = {
        'title': article.title,
        'content': article.text,
        'summary': article.summary if article.summary else '',
        'url': url,
        'source': source_name,
        'authors': article.authors,
        'published_date': article.publish_date.isoformat() if article.publish_date else None,
        'scraped_date': datetime.now().isoformat(),
        'keywords': article.keywords,
        'top_image': article.top_image,
        'entities': entities,
        'sentiment_score': sentiment_score,
        'topics': topics
    }
    
    # Step 6: Index in OpenSearch
    response = opensearch_client.index(
        index='news-articles',
        body=document,
        refresh=True
    )
    
    return document

# Example: Process articles from NewsAPI
def process_newsapi_results(api_key, query):
    # Fetch from NewsAPI
    url = 'https://newsapi.org/v2/everything'
    params = {
        'apiKey': api_key,
        'q': query,
        'pageSize': 10,
        'language': 'en'
    }
    
    response = requests.get(url, params=params)
    articles = response.json().get('articles', [])
    
    # Process each article
    processed = []
    for article in articles:
        try:
            result = complete_article_pipeline(
                article['url'],
                article['source']['name']
            )
            processed.append(result)
            print(f"Processed: {result['title']}")
        except Exception as e:
            print(f"Error processing {article['url']}: {e}")
    
    return processed

# Run the pipeline
# processed_articles = process_newsapi_results('your_api_key', 'artificial intelligence')
```

### Real-time Monitoring Pipeline

```python
import time
import schedule
from datetime import datetime, timedelta

def monitor_news_sources(api_keys, queries, interval_minutes=30):
    """
    Continuously monitor news sources and process new articles
    """
    def fetch_and_process():
        print(f"[{datetime.now()}] Fetching news...")
        
        # NewsAPI
        for query in queries:
            try:
                processed = process_newsapi_results(api_keys['newsapi'], query)
                print(f"Processed {len(processed)} articles for '{query}'")
            except Exception as e:
                print(f"Error with query '{query}': {e}")
        
        print(f"[{datetime.now()}] Fetch complete. Next run in {interval_minutes} minutes.")
    
    # Run immediately
    fetch_and_process()
    
    # Schedule periodic runs
    schedule.every(interval_minutes).minutes.do(fetch_and_process)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# Example usage
# api_keys = {'newsapi': 'your_newsapi_key'}
# queries = ['technology', 'artificial intelligence', 'climate change']
# monitor_news_sources(api_keys, queries, interval_minutes=30)
```

---

## Additional Resources

### Documentation Links
- **NewsAPI:** https://newsapi.org/docs
- **The Guardian API:** https://open-platform.theguardian.com/documentation/
- **New York Times API:** https://developer.nytimes.com/docs
- **spaCy:** https://spacy.io/usage
- **Hugging Face:** https://huggingface.co/docs/transformers
- **OpenSearch:** https://opensearch.org/docs/latest/
- **NLTK:** https://www.nltk.org/

### Recommended Reading
- "Speech and Language Processing" by Jurafsky & Martin
- "Natural Language Processing with Python" by Bird, Klein & Loper
- "Hands-On Machine Learning" by Géron

### Useful Tools
- **Postman:** Test API endpoints
- **Jupyter Notebooks:** Interactive development
- **Docker:** Container for OpenSearch
- **Git:** Version control for scrapers

---

## Summary

This guide covers:

1. **News APIs:** Multiple options with varying features, pricing, and content delivery
   - Most provide metadata but NOT full article text (Guardian is the exception)
   - Free tiers available for development and testing
   - Easy to get started with API keys

2. **Web Scraping:** Alternative or complementary approach
   - Necessary for full article text in most cases
   - Use newspaper3k for news-specific extraction
   - Consider legal and ethical implications

3. **Best Approach:** Hybrid strategy
   - Use APIs for discovering articles and getting metadata
   - Use web scraping for full article content when needed
   - RSS feeds are a reliable, legal alternative

4. **AI/NLP Processing:** Multiple powerful Python libraries
   - spaCy: Fast entity recognition and linguistic features
   - Transformers: State-of-the-art models for sentiment, topics, summarization
   - NLTK: Traditional NLP toolkit
   - OpenAI GPT: Advanced analysis with natural language prompts

5. **OpenSearch:** Powerful indexing and search capabilities
   - Store articles with rich metadata
   - Full-text search with highlighting
   - Support for complex queries and aggregations

Start with APIs for rapid prototyping, add web scraping as needed for full content, and use NLP libraries to extract insights from the collected data.
