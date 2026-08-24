import sys
from crawl import crawl_site_async
import asyncio
from json_report import write_json_report

async def main():
    if len(sys.argv) < 4:
        print("too few arguments provided")
        sys.exit(1)
    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)
    if len(sys.argv) == 4:
        try:
            max_concurrency = int(sys.argv[2])
        except ValueError:
            print("max_concurrency must be an integer")
            sys.exit(1)
        try:
            max_pages = int(sys.argv[3])
        except ValueError:
            print("max_pages must be an integer")
            sys.exit(1)
        print(f"starting crawl of: {sys.argv[1]} with max_concurrency={max_concurrency} and max_pages={max_pages}")
        page_info = await crawl_site_async(sys.argv[1], max_concurrency=max_concurrency, max_pages=max_pages)
        print(f"found {len(page_info)} pages in the crawl")

        write_json_report(page_info)

        #for page in page_info.values():
            #if page is not None:
                #print(f"URL: {page['url']}")
                #print(f"Heading: {page['heading']}")
                #print(f"First Paragraph: {page['first_paragraph']}")
                #print(f"Outgoing Links: {page['outgoing_links']}")
                #print(f"Image URLs: {page['image_urls']}")

if __name__ == "__main__":
    asyncio.run(main())