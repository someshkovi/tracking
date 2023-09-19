import traceback

import httpx
from bs4 import BeautifulSoup as bs

# from scripts.products import Product

def get_text(bs_attr, default=None):
    return default if bs_attr is None else bs_attr.text

def get_myntra_product_info(url):
    # product = Product()
    page = httpx.get(url)
    soup = bs(page.content, 'html.parser')
    data = soup.find('div', {'class': 'pdp-price-info'})
    title = get_text(data.find('h1', attrs={'class': 'pdp-title'}))
    name = get_text(data.find('h1', attrs={'class': 'pdp-name'}))
    price = get_text(data.find('h1', attrs={'class': 'pdp-price'}))
    # title = get_text(data.find('h1', attrs={'class': 'pdp-title'}))
    # title = get_text(data.find('h1', attrs={'class': 'pdp-title'}))
    print(title, name)
    print(price)
    return price


if __name__ == '__main__':
    try:
        value = get_myntra_product_info(
            'https://www.myntra.com/18838824'
        )
        print(value)
    except Exception:
        error_msg = traceback.format_exc()
        print(error_msg)
