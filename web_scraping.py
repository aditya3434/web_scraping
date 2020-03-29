from bs4 import BeautifulSoup
from requests import get
from contextlib import closing
from requests.exceptions import RequestException

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, it  returns the
    text content, otherwise it returns None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """ 
    This function logs and prints error
    """
    print(e)

def spaces(string):
    s=""
    for i in string:
        if (i.isalpha()):
            s=s+i
    return s

for i in range(1,51):
    '''
    Accesses the html file and extracts details like title, price and rating
    '''
    url="http://books.toscrape.com/catalogue/page-"+str(i)+".html"
    raw_html=simple_get(url)
    html=BeautifulSoup(raw_html,'html.parser')
    for article in html.find_all('article',class_="product_pod"):
        s1=article.h3.a.get("title")
        s2=article.p.get("class")
        s3=article.find('div',class_="product_price").p.text
        s4=article.find('p',class_="instock availability").text
        print(s1,"\t","Star Rating : ",s2[1],"\t",s3,"\t",spaces(s4))

