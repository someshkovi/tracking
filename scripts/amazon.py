import unicodedata
from bs4 import BeautifulSoup as bs
import requests


def get_amazon_results_by_search(search_parameter, no_of_pages=20):
    results = []
    for page in range(no_of_pages):
        link = f'https://www.amazon.in/s?k={search_parameter}&page={page}'

        print(link, '\n')
        page = requests.get(link, verify=False)

        soup = bs(page.content, 'html.parser')

        for d in soup.findAll('div', attrs={'class': 'a-section'}):
            name = d.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
            price = d.find('span', attrs={'class': 'a-price-whole'})
            currency = d.find('span', attrs={'class': 'a-price-symbol'})
            rating = d.find('span', attrs={'class': 'a-icon-alt'})
            # ratings_count = d.find('span', attrs={'class':'a-size-base s-light-weight-text'})
            if name:
                try:
                    results.append({
                        'name': name.string,
                        'price': int(price.string.replace(',', '')),
                        'currency': currency.string,
                        'rating': float(rating.string.split(' ')[0]),
                        # 'ratings_count':ratings_count.string,
                    })
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
    try:
        name = soup.find(id='productTitle').get_text().strip()
        price_str = soup.find(id='tp_price_block_total_price_ww').get_text()
    except Exception as e:
        error_msg = f'exception in getting product info = {e}'
        return {
            'status': 'error',
            'error_msg': error_msg,
            'data': {}
        }

    try:
        availability_message = soup.select('#availability .a-color-success')[0].get_text().strip()
        available = True
    except:
        try:
            availability_message = soup.select('#availability .a-color-price')[0].get_text().strip()
            available = True
        except:
            availability_message = None
            available = False

    try:
        price = unicodedata.normalize('NFKD', price_str)
        price = price.split('.')[0].replace(',', '').replace('₹', '')
        price = float(price)
    except Exception as e:
        error_msg = f'exception in getting product info = {e}'
        return {
            'status': 'error',
            'error_msg': error_msg,
            'data': {}
        }

    data = {
        'name': name,
        'price': price,
        'availability': available,
        'availability_message': availability_message
    }
    return {
        'status': 'success',
        'error_msg': '',
        'data': data
    }
