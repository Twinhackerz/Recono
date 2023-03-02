import pandas as pd
import whois
from tldextract import tldextract


def whois_info(url):
    tld_parts = tldextract.extract(url)
    top_level_domain = f"{tld_parts.domain}.{tld_parts.suffix}"
    domain = top_level_domain
    w = whois.whois(domain)

    # Extract the relevant information into a dictionary
    df = pd.DataFrame({
        "domain_name": [w.domain_name],
        "creation_date": [w.creation_date],
        "whois_server": [w.whois_server],
        "registrar": [w.registrar],
        "expiration_date": [w.expiration_date],
        "status": [w.status],
        "name": [w.name],
        "org": [w.org],
        "address": [w.address],
        "city": [w.city],
        "state": [w.state],
        "zipcode": [w.zipcode],
        "country": [w.country]
    })

    # Create a DataFrame from the dictionary
    return df
