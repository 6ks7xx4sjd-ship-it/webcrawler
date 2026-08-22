def normalize_url(url):
    """
    Normalize a URL by removing URI, scheme, and trailing slash.
    """
    # Remove the scheme (http:// or https://)
    if url.startswith("http://"):
        url = url[len("http://"):]
    elif url.startswith("https://"):
        url = url[len("https://"):]

    # Remove trailing slash if present
    if url.endswith("/"):
        url = url[:-1]

    return url

def get_heading_from_html(html: str) -> str:
    """
    Extract the first heading (h1) tag from the given HTML string or the (h2) tag as a fallback. Returns an empty string if no heading is found.
    """
    from bs4 import BeautifulSoup, Tag 

    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find("h1")
    if isinstance(heading, Tag):
        return heading.get_text(strip=True)
    heading = soup.find("h2")
    if isinstance(heading, Tag):
        return heading.get_text(strip=True)
    else:
        return ""

def get_first_paragraph_from_html(html: str) -> str:
    """
    Extract the first paragraph (p) tag from the given HTML string. Returns an empty string if no paragraph is found.
    """
    from bs4 import BeautifulSoup, Tag 

    soup = BeautifulSoup(html, "html.parser")
    paragraph = soup.find("main").find("p") if soup.find("main") else soup.find("p")
    if isinstance(paragraph, Tag):
        return paragraph.get_text(strip=True)
    else:
        return ""

def get_urls_from_html(html: str, base_url: str) -> list:
    """
    Extract all URLs from the given HTML string and return a list of absolute URLs.
    """
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            absolute_url = urljoin(base_url, href)
            urls.append(absolute_url)
    return urls

def get_images_from_html(html: str, base_url: str) -> list:
    """
    Extract all image URLs from the given HTML string and return a list of absolute image URLs.
    """
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    soup = BeautifulSoup(html, "html.parser")
    images = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            absolute_url = urljoin(base_url, src)
            images.append(absolute_url)
    return images

def extract_page_data(html: str, page_url: str) -> dict:
    """
    Extract the heading, first paragraph, URLs, and image URLs from the given HTML string.
    Returns a dictionary with the extracted data.
    """
    from typing import TypedDict

    class PageData(TypedDict):
        url: str
        heading: str
        first_paragraph: str
        outgoing_links: list[str]
        image_urls: list[str]

    heading = get_heading_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)
    outgoing_links = get_urls_from_html(html, page_url)
    image_urls = get_images_from_html(html, page_url)

    return {
        "url": page_url,
        "heading": heading,
        "first_paragraph": first_paragraph,
        "outgoing_links": outgoing_links,
        "image_urls": image_urls
    }

def get_html(url: str) -> str:
    """
    Fetch the HTML content of the given URL and return it as a string.
    """
    import requests

    response =requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})

    #raise an error for 400 level responses
    response.raise_for_status()

    #raise an error if response content type is not text/html
    if "text/html" not in response.headers.get("Content-Type", ""):
        raise ValueError(f"URL {url} did not return HTML content")

    #raise an error if response content is empty
    if not response.text:
        raise ValueError(f"URL {url} returned empty content")

    #raise an error if response content is too large (e.g., > 10 MB)
    if len(response.content) > 10 * 1024 * 1024:
        raise ValueError(f"URL {url} returned content that is too large")

    return response.text

def crawl_page(base_url: str, current_url=None, page_data: dict = None) -> dict:
    """
    Crawl a single page and return the extracted data.
    """
    if current_url is None:
        current_url = base_url
    from urllib.parse import urlparse
    if urlparse(current_url).netloc != urlparse(base_url).netloc:
        return page_data if page_data is not None else {}

    normalized_current_url = normalize_url(current_url)
    html = get_html(current_url)
    print(f"Crawling {current_url}...")

    #When get_html raises an error, catch it and print the error message, then return the page_data as is
    try:
        html = get_html(current_url)

        #Add normalized_current_url to page_data if not already present
        if page_data is None:
            page_data = {}
        if normalized_current_url not in page_data:
            page_data[normalized_current_url] = extract_page_data(html, current_url)

        #Get all urls from the current page and crawl them recursively
        urls = get_urls_from_html(html, current_url)
        for url in urls:
            normalized_url = normalize_url(url)
            if normalized_url not in page_data:
                crawl_page(base_url, url, page_data)

    except Exception as e:
        print(f"Error fetching {current_url}: {e}")
        return page_data if page_data is not None else {}

    return page_data