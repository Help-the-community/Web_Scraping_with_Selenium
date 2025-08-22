from seleniumbase import SB
from typing import List, Dict


def extract_region_data(url: str, container_selector: str = "#facetUE") -> List[Dict[str, str]]:
    """
    Extract data from anchor links under a container using SeleniumBase.

    Args:
        url (str): Target URL to scrape.
        container_selector (str): CSS selector of the container to extract data from.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing data-val, count text, and region.
    """
    data: List[Dict[str, str]] = []

    with SB(uc=True, test=True) as sb:
        sb.maximize_window()
        sb.activate_cdp_mode(url)
        sb.uc_gui_click_captcha()  # handles potential CAPTCHA

        # Accept cookies if available
        try:
            sb.find_element("#CybotCookiebotDialogBodyButtonAccept").click()
        except Exception:
            pass  # If no cookie popup, continue

        # Ensure container exists
        sb.find_element(container_selector)
        links = sb.find_elements(f"{container_selector}>li>a")

        # Extract information
        for link in links:
            text_parts = link.text.split()
            data_dict = {
                "data_val": link['data-val'],
                "cnt_text": text_parts[0] if len(text_parts) > 0 else "",
                "region": text_parts[1] if len(text_parts) > 1 else ""
            }
            data.append(data_dict)

    return data


# -------------------- Example usage -------------------- #
if __name__ == "__main__":
    url = "https://www.nepremicnine.net/oglasi-prodaja/gorenjska/stanovanje/"
    region_data = extract_region_data(url)
    print(region_data)

"""
P: https://stackoverflow.com/q/79743063/11179336
S: https://stackoverflow.com/a/79743257/11179336
"""