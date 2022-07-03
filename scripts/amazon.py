import unicodedata
from bs4 import BeautifulSoup as bs
import requests
from scripts.products import Product


def get_amazon_results_by_search(search_parameter: str, no_of_pages=2) -> dict:
    results = []
    product_names = set()
    for page in range(no_of_pages):
        link = f'https://www.amazon.in/s?k={search_parameter}&page={page}'

        page = requests.get(link, verify=False)

        soup = bs(page.content, 'html.parser')

        for d in soup.findAll('div', attrs={'class': 'a-section'}):
            name = d.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
            if name and name not in product_names:
                product = Product()
                product_names.add(name)
                price = d.find('span', attrs={'class': 'a-price-whole'})
                currency = d.find('span', attrs={'class': 'a-price-symbol'})
                rating = d.find('span', attrs={'class': 'a-icon-alt'})
                ratings_count = d.find('span', attrs={'class': 'a-size-base s-underline-text'})
                link = d.find_all('a')[0].get('href')
                try:
                    product.name = name.string
                    product.price = int(price.string.replace(',', ''))
                    product.rating = float(rating.string.split(' ')[0])
                    product.ratings_count = int(ratings_count.string.replace(',', ''))
                    product.url = None if link is None else 'https://amazon.in'+link
                    results.append(product.__dict__)
                except Exception as e:
                    pass
    return {
        'status': 'success',
        'error_msg': '',
        'data': results
    }


def get_amazon_product_info(url):
    page = requests.get(url, verify=False)
    soup = bs(page.content, features='lxml')
    req_soup = soup.find(id='centerCol')
    try:
        product = Product()
        product.name = req_soup.find(id='productTitle').get_text().strip()
        price_str = req_soup.find('span', attrs={'class': 'a-price a-text-price a-size-medium apexPriceToPay'}
                                  ).find('span', attrs={'class': 'a-offscreen'}).get_text()
        rating = req_soup.find('span', attrs={'class': 'a-icon-alt'})
        if rating is not None:
            rating = rating.get_text()
        ratings_count = req_soup.find(id='acrCustomerReviewText')
        if ratings_count is not None:
            ratings_count = ratings_count.get_text()
    except Exception as e:
        error_msg = f'exception in getting product info = {e}'
        return {
            'status': 'error',
            'error_msg': error_msg,
            'data': {}
        }

    try:
        product.availability_message = soup.select('#availability .a-color-success')[0].get_text().strip()
        product.availability = True
    except:
        try:
            product.availability_message = soup.select('#availability .a-color-price')[0].get_text().strip()
            product.availability = True
        except:
            product.availability_message = None
            product.availability = False

    try:
        price = unicodedata.normalize('NFKD', price_str)
        price = price.split('.')[0].replace(',', '').replace('₹', '')
        product.price = float(price)
        product.rating = float(rating.split(' ')[0])
        product.ratings_count = int(req_soup.find(id='acrCustomerReviewText').get_text().replace(',', '').split(' ')[0])
    except Exception as e:
        error_msg = f'exception in getting product info = {e}'
        return {
            'status': 'error',
            'error_msg': error_msg,
            'data': {}
        }

    data = product.__dict__
    return {
        'status': 'success',
        'error_msg': '',
        'data': data
    }


if __name__ == '__main__':
    data = get_amazon_results_by_search('ryzen 7', 1)
    print(data['data'])
