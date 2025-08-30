from seleniumbase import SB

url = "https://www.python.org/"

with SB(uc=True, test=True) as sb:
    sb.open(url)
    """
    When you want to hover over an element or dropdown menu,
    and then click an element that appears after that.
    """
    # hover_and_click(hover_selector, click_selector)
    sb.hover_and_click("li#downloads", "a[href='/downloads/']")
