import os
import requests
import tldextract as tldextract
import pandas as pd

def find_subdomains(url):
    subdomains = []
    tld_parts = tldextract.extract(url)
    top_level_domain = f"{tld_parts.domain}.{tld_parts.suffix}"
    base_folder = os.path.dirname(__file__)
    wordlist = os.path.join(base_folder, '../src/files/subdomains.txt')
    with open(wordlist, "r") as wordlist_file:
        for line in wordlist_file:
            subdomain = line.strip() + "." + top_level_domain
            urls = ["https://" + subdomain]
            for url in urls:
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        server_header = response.headers.get('Server')
                        if server_header:
                            subdomains.append((subdomain, server_header))
                        else:
                            subdomains.append((subdomain, None))
                except requests.exceptions.RequestException:
                    pass
    return subdomains


