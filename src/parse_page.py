from bs4 import BeautifulSoup
from parse_soup_stsci import parse_soup_stsci

def parse_page(content):
    soup = BeautifulSoup(content, "html.parser")
    return parse_soup_stsci(soup)

