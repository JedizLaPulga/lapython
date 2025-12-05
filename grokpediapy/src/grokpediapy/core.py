"""
Core logic for grokpediapy.
Handles secure HTTP requests and HTML parsing.
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from typing import Optional, Dict

# Security: Define a proper User-Agent so we are not blocked as a generic bot.
HEADERS: Dict[str, str] = {
    "User-Agent": "GrokpediaPy/0.1.0 (Educational; +https://github.com/example/grokpediapy)"
}

# Security: Always enforce timeouts to prevent hanging processes.
TIMEOUT_SECONDS: int = 10

class ContentRetrievalError(Exception):
    """Custom exception for retrieval failures."""
    pass

def fetch_article(topic: str) -> str:
    """
    Fetches article content from Grokpedia securely.

    Args:
        topic (str): The topic to search for.

    Returns:
        str: The clean text content of the article.

    Raises:
        ContentRetrievalError: If network fails or page is not found.
    """
    # Security: URL Encode the topic to prevent URL injection or malformed paths
    safe_topic = quote(topic.strip())
    
    # Construct the URL
    # Note: Assuming the structure provided in prompt: grokpedia.com/pages/{topic}
    url = f"https://grokpedia.com/pages/{safe_topic}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS)
        
        # Raise error for 4xx or 5xx status codes
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ContentRetrievalError(f"Topic '{topic}' not found on Grokpedia.")
        raise ContentRetrievalError(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        raise ContentRetrievalError(f"Network Connection Error: {e}")

    return _parse_html(response.text)

def _parse_html(html_content: str) -> str:
    """
    Parses HTML and extracts readable text.
    
    Args:
        html_content (str): Raw HTML.
        
    Returns:
        str: Cleaned text.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Implementation Detail:
    # Since Grokpedia is hypothetical, we look for common content containers.
    # In a real scenario, we would inspect the specific DOM of the target site.
    content_div = (
        soup.find("main") 
        or soup.find("div", {"id": "content"}) 
        or soup.find("div", {"class": "mw-parser-output"}) # Wikipedia style fallback
        or soup.body
    )

    if not content_div:
        return "No readable content found on the page."

    # Extract text, stripping excessive whitespace
    text = content_div.get_text(separator="\n", strip=True)
    return text