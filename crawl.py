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