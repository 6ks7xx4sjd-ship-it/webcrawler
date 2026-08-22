import sys
from crawl import get_html, crawl_page

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    if len(sys.argv) == 2:
        print(f"starting crawl of: {sys.argv[1]}")
        page_info = crawl_page(sys.argv[1])
        print(f"found {len(page_info)} pages in the crawl")

if __name__ == "__main__":
    main()