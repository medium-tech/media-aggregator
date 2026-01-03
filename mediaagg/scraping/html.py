"""
HTML scraping module for downloading, rendering, and extracting text from web pages.
"""

import hashlib
from pathlib import Path
import requests
from html2image import Html2Image
import pytesseract


def scrape_html(url: str, source_name: str = "scraped") -> str:
    """
    Scrape a web page: download HTML, render to image, and extract text via OCR.
    
    Args:
        url: The URL to scrape
        source_name: Name of the data source (default: 'scraped')
    
    Returns:
        String path to the article folder containing all artifacts
    """
    from mediaagg.storage import get_source_dir
    
    # Generate unique article ID from URL
    article_id = hashlib.sha256(url.encode()).hexdigest()
    
    # Create article folder
    source_dir = get_source_dir(source_name)
    article_folder = source_dir / article_id
    article_folder.mkdir(parents=True, exist_ok=True)
    
    # Download HTML
    print(f"Downloading HTML from {url}...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    html_content = response.text
    
    # Save raw HTML
    html_path = article_folder / "raw.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved raw HTML to {html_path}")
    
    # Render HTML to image
    print("Rendering HTML to image...")
    hti = Html2Image(output_path=str(article_folder), custom_flags=['--no-sandbox'])
    image_filename = "rendered.png"
    hti.screenshot(html_str=html_content, save_as=image_filename)
    image_path = article_folder / image_filename
    print(f"Saved rendered image to {image_path}")
    
    # Extract text from image using OCR
    print("Extracting text from image via OCR...")
    extracted_text = pytesseract.image_to_string(str(image_path))
    
    # Save extracted text
    text_path = article_folder / "extracted_text.txt"
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)
    print(f"Saved extracted text to {text_path}")
    
    return str(article_folder)
