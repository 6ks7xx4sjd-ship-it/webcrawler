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