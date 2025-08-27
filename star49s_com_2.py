import json
import re
import logging
from typing import List, Any
import requests
from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def get_teatime_results(url: str) -> List[Any]:
    """
    Scrape the 'sortedTea' results from the given URL.

    Parameters
    ----------
    url : str
        URL of the page containing 'sortedTea' JSON data inside a <script> tag.

    Returns
    -------
    list
        Parsed list of tea results. Empty if not found or parsing fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find_all("script")[-1]

    if not script_tag:
        logging.info("No script tag is not found")
        return []

    # parse the embedded escaped json data using regex
    match = re.search(r'\\"sortedTea\\":(\[.*\])}\]\]', script_tag.get_text(), re.DOTALL)
    if not match:
        logging.info("The target script tag is not found")
        return []
    try:
        # First, unescape the string using json.loads
        escaped_json = match.group(1)
        logging.info(f"Found 'sortedTea' in script tag")
        unescaped_json = json.loads(f'"{escaped_json}"')  # decode escaped quotes
        # Then parse it as JSON
        results = json.loads(unescaped_json)
        return results
    except json.JSONDecoder:
        logging.warning(f"JSON decoding failed in script tag")
        return []


if __name__ == "__main__":
    url = "https://star49s.com/results/teatime"
    results = get_teatime_results(url)
    print(results)


"""
StackOverflow:
P: https://stackoverflow.com/q/79747874/11179336
S: https://stackoverflow.com/a/79747941/11179336
"""
