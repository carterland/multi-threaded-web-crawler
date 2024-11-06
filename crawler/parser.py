from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_links(page_content, base_url):
    soup = BeautifulSoup(page_content, "html.parser")
    links = set()
    for anchor in soup.find_all("a", href=True):
        link = anchor['href']
        # Convert relative URLs to absolute URLs
        link = urljoin(base_url, link)
        links.add(link)
    return links

