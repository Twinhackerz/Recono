import requests
import pandas as pd

def headers(url):
    response = requests.get(url)
    if 'X-Frame-Options' in response.headers:
        clickjacking_protection = f"Clickjacking protection enabled: {response.headers['X-Frame-Options']}"
    else:
        clickjacking_protection = "No clickjacking protection detected."

    # Check for XSS protection
    if 'X-XSS-Protection' in response.headers:
        xss_protection = f"XSS protection enabled: {response.headers['X-XSS-Protection']}"
    else:
        xss_protection = "No XSS protection detected."

    if 'strict-transport-security' in response.headers:
        htst = f'HSTS is enabled: {response.headers["strict-transport-security"]}'
    else:
        htst = 'HSTS is not enabled'

    # Export the header information to an Excel file
    headers = response.headers
    df_headers = pd.DataFrame.from_dict(headers, orient='index', columns=['Value'])

    # Add clickjacking and XSS protection information to the same dataframe
    df_headers.loc['Clickjacking Protection'] = clickjacking_protection
    df_headers.loc['XSS Protection'] = xss_protection
    df_headers.loc['HSTS'] = htst
    #print("headers")
    return df_headers

