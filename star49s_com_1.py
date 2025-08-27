import json
import logging
from typing import List, Any
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def get_teatime_results(url: str) -> List[Any]:
    """
    Scrape 'itemListElement' from JSON-LD data on a page.

    Parameters
    ----------
    url : str
        URL of the page containing JSON-LD data.

    Returns
    -------
    list
        List of items in 'itemListElement', empty if not found.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", {"type": "application/ld+json"})

    if not script_tag:
        logging.warning("No JSON-LD script tag found")
        return []

    try:
        data = json.loads(script_tag.string)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON-LD: {e}")
        return []

    results = []
    # Get the itemListElement
    for node in data.get("@graph", []):
        if node.get("@type") == "WebPage":
            main_entity = node.get("mainEntity", {})
            if main_entity.get("@type") == "ItemList":
                results = main_entity.get("itemListElement", [])
                logging.info(f"Found {len(results)} items in 'itemListElement'")
                break

    if not results:
        logging.warning("No 'itemListElement' found in JSON-LD data")

    return results


if __name__ == "__main__":
    url = "https://star49s.com/results/teatime"
    results = get_teatime_results(url)
    print(results)

"""
StackOverflow:
P: https://stackoverflow.com/q/79747874/11179336
S: https://stackoverflow.com/a/79747941/11179336
"""