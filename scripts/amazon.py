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
    req_soup = soup.find(id='centerCol')
    try:
        name = req_soup.find(id='productTitle').get_text().strip()
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
        rating = float(rating.split(' ')[0])
        ratings_count = int(req_soup.find(id='acrCustomerReviewText').get_text().replace(',','').split(' ')[0])
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
        'availability_message': availability_message,
        'rating': rating,
        'ratings_count': ratings_count,
    }
    return {
        'status': 'success',
        'error_msg': '',
        'data': data
    }
