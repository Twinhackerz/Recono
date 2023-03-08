import requests
import pandas as pd



def http_methods(url):
    methods = ['PUT', 'TRACE', 'POST', 'GET', 'OPTIONS', 'DELETE']
    results = []
    for method in methods:
        req = requests.request(method, url)
        results.append({'Method': method, 'Status Code': req.status_code, 'Reason': req.reason})

        # Check if TRACE method is possible and append the result to the same list
        if method == 'TRACE':
            if req.status_code == 200:
                results.append(
                    {'Method': 'XST', 'Status Code': 'Possible', 'Reason': 'Cross-Site Tracing Vulnerability'})

    df_methods = pd.DataFrame(results)
    #print("http_method")

    return df_methods

