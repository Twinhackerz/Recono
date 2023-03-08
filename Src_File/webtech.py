import pandas as pd
from Wappalyzer import WebPage, Wappalyzer
import warnings
def web_tech(url):
    warnings.filterwarnings("ignore", message="""Caught 'unbalanced parenthesis at position 119' compiling regex""",
                            category=UserWarning)

    webpage = WebPage.new_from_url(url)
    wappalyzer = Wappalyzer.latest()
    technologies = wappalyzer.analyze(webpage)

    technologies_dict = dict.fromkeys(technologies, '')
    df_tech = pd.DataFrame(list(technologies_dict.items()), columns=['Technology', 'Version'])
    #print("webtechnology")
    return df_tech



