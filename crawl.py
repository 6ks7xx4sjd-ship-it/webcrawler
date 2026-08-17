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