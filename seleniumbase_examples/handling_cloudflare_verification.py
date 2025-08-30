from seleniumbase import SB

url = "https://www.nepremicnine.net/"


with SB(uc=True, test=True) as sb:
    # -----------------------------------------------------
    sb.maximize_window()
    sb.activate_cdp_mode(url)
    sb.uc_gui_click_captcha()  # handles potential CAPTCHA
    # -----------------------------------------------------

    # Accept cookies if available
    try:
        sb.find_element("#CybotCookiebotDialogBodyButtonAccept").click()
    except Exception:
        pass  # If no cookie popup, continue
