import sys
from crawl import crawl_site_async
import asyncio

async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    if len(sys.argv) == 2:
        print(f"starting crawl of: {sys.argv[1]}")
        page_info = await crawl_site_async(sys.argv[1])
        print(f"found {len(page_info)} pages in the crawl")

        for page in page_info.values():
            print(f"URL: {page['url']}")
            print(f"Heading: {page['heading']}")
            print(f"First Paragraph: {page['first_paragraph']}")
            print(f"Outgoing Links: {page['outgoing_links']}")
            print(f"Image URLs: {page['image_urls']}")

if __name__ == "__main__":
    asyncio.run(main())