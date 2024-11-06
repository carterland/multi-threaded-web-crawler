# crawler.py

from crawler.logger import log_info, log_warning, log_error
from crawler.fetcher import fetch_page
from crawler.parser import extract_links, extract_title
from crawler.storage import save_page
from crawler.scheduler import Scheduler

def crawl(start_url):
    log_info(f"Starting crawl at {start_url}")
    
    # Initialize the URL queue and scheduler with a delay
    scheduler = Scheduler(delay=1)  # 1 second delay between requests
    scheduler.add_url(start_url)
    
    # Start crawling
    while not scheduler.queue.empty():
        current_url = scheduler.get_next_url()
        log_info(f"Crawling {current_url}")
        
        try:
            # Fetch the page content
            page_content = fetch_page(current_url)
            
            # Optionally, save the raw HTML to a file
            save_page(current_url, page_content)
            
            # Extract links from the page
            links = extract_links(page_content)
            log_info(f"Found {len(links)} links on {current_url}")
            
            # Optionally, extract the page title
            title = extract_title(page_content)
            log_info(f"Title of {current_url}: {title}")
            
            # Add the found links to the scheduler (queue them to be crawled)
            for link in links:
                scheduler.add_url(link)
            
        except Exception as e:
            log_error(f"Error while crawling {current_url}: {e}")

if __name__ == "__main__":
    start_url = "http://example.com"
    crawl(start_url)

