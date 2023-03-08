import requests
import pandas as pd
def cookie(url):
    response = requests.get(url)
    cookies = response.cookies
    cookies_info = []
    for cookie in cookies:
        cookie_dict = {
            "Name": cookie.name,
            "Secure": cookie.secure,
            "HttpOnly": cookie.has_nonstandard_attr("HttpOnly"),
        }
        try:
            cookie_dict["SameSite"] = cookie.same_site
        except AttributeError:
            cookie_dict["SameSite"] = "N/A"
        if cookie.expires is not None:
            cookie_dict["Max-Age"] = cookie.expires - cookie.expires
        else:
            cookie_dict["Max-Age"] = "N/A"
        cookies_info.append(cookie_dict)
    df_cookies = pd.DataFrame(cookies_info)
    return df_cookies


