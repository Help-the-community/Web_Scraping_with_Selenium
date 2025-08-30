from seleniumbase import SB


# The browser exits automatically after the "with" block ends.
with SB(uc=True, test=True) as sb:

    sb.open("https://www.google.com")

    # -------------------------------------------------------------------------------
    # sb.type(input box selector, "search query + Enter(\n)")
    sb.type("textarea[name='q']", "SeleniumBase\n")
    # -------------------------------------------------------------------------------

    sb.wait_for_element("h3")  # wait for results

    results = sb.find_elements("h3")
    for r in results[:5]:
        print("Result:", r.text)
