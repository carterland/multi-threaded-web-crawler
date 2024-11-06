import threading
import time
from queue import Queue
from .fetcher import fetch_page
from crawler.parser import extract_links
from crawler.config import visited_urls

def crawler_worker(url_queue, semaphore):
    while True:
        url = url_queue.get()
        if url is None:
            break

        # Skip already visited URLs
        if url in visited_urls:
            url_queue.task_done()
            continue

        visited_urls.add(url)

        # Fetch and parse the page
        page_content = fetch_page(url)
        if page_content:
            new_links = extract_links(page_content, url)
            for link in new_links:
                if link not in visited_urls:
                    url_queue.put(link)

        url_queue.task_done()

def start_crawler(start_url, num_threads=10):
    url_queue = Queue()
    url_queue.put(start_url)

    # Create a semaphore to limit concurrent threads
    semaphore = threading.Semaphore(num_threads)

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=crawler_worker, args=(url_queue, semaphore))
        t.start()
        threads.append(t)

    url_queue.join()

    # Stop the threads
    for _ in range(num_threads):
        url_queue.put(None)
    for t in threads:
        t.join()

    print("Crawling finished!")

