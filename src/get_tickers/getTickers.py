import requests
from bs4 import BeautifulSoup



def get_wikipedia_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print("Error fetching page:", e)
        return None

def getSPFhundered():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    portfolioList = []
    wikipedia_html = get_wikipedia_html(url)

    if wikipedia_html:
        data = wikipedia_html.find(id="constituents")
        data = data.find_all(rel="nofollow")
        for _i, header in enumerate(data):
            if('.B' not in header.contents[0] and _i > 150 ):
                portfolioList.append(header.contents[0])

    return portfolioList