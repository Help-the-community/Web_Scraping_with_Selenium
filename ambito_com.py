"""
Web scraper for extracting navigation tab text from Ámbito's dollar page
using SeleniumBase with undetected-chromedriver support.

Author: Ajeet Verma
"""

from typing import List
from seleniumbase import SB


def get_navigation_tabs(url: str, timeout: int = 5) -> List[str]:
    """
    Launches a browser session with SeleniumBase, navigates to the given URL,
    handles potential CAPTCHA, and extracts navigation tab text.

    Args:
        url (str): Target webpage URL.
        timeout (int): Maximum wait time for locating elements (in seconds).

    Returns:
        List[str]: A list of navigation tab items as strings.
    """
    with SB(uc=True, page_load_strategy="eager", test=True) as sb:
        sb.maximize_window()
        sb.activate_cdp_mode(url)
        sb.uc_gui_click_captcha()  # handle potential CAPTCHA automatically

        nav_tab = sb.wait_for_element("nav.main-nav", timeout=timeout)
        return nav_tab.text.split()


def main(url: str) -> None:
    """
    Main execution function to fetch and display navigation tab text.
    """
    try:
        tabs = get_navigation_tabs(url)
        print("Navigation Tabs:", tabs)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    URL = "https://www.ambito.com/contenidos/dolar.html"
    main(URL)

"""
Stackoverflow:
P: https://stackoverflow.com/q/79750510/11179336
S: https://stackoverflow.com/a/79750572/11179336
"""