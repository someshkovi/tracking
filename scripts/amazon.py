import unicodedata
from typing import List
# from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

import httpx
from bs4 import BeautifulSoup as bs
from scripts.products import Product
from scripts.constants import Constants


class Amazon:
    """
        Amazon fetching
    """

    def search_page_data(self, link: str) -> List[dict]:
        product_names = set()
        results = []
        page = httpx.get(link, verify=False)
        soup = bs(page.content, 'html.parser')
        for div in soup.findAll('div', attrs={'class': 'a-section'}):
            name = div.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
            if name and name not in product_names:
                product = Product()
                product_names.add(name)
                price = div.find('span', attrs={'class': 'a-price-whole'})
                # currency = d.find('span', attrs={'class': 'a-price-symbol'})
                rating = div.find('span', attrs={'class': 'a-icon-alt'})
                ratings_count = div.find('span', attrs={'class': 'a-size-base s-underline-text'})
                try:
                    link = div.find_all('a')[0].get('href')
                    product.site = 'amazon.in'
                    product.name = name.string
                    product.price = int(price.string.replace(',', ''))
                    product.rating = float(rating.string.split(' ')[0])
                    product.ratings_count = int(ratings_count.string.replace(',', ''))
                    product.url = None if link is None else f'https://amazon.in{link}'
                    results.append(product.__dict__)

                except Exception as exp:
                    print(exp)
        return results

    def multithread_search_data(self, search_parameter: str, no_of_pages: int = 2) -> List[dict]:
        links = [f'https://www.amazon.in/s?k={search_parameter}&page={page}' for page in
                     range(1, no_of_pages + 1)]
        results = []
        with ThreadPool() as pool:
            thread_results = pool.imap(self.search_page_data, links)
            for result in thread_results:
                results += result
        return [dict(s) for s in {frozenset(d.items()) for d in results}]


def get_amazon_results_by_search(search_parameter: str, no_of_pages=2) -> dict:
    results = []
    product_names = set()
    for page in range(no_of_pages):
        link = f'https://www.amazon.in/s?k={search_parameter}&page={page}'

        page = httpx.get(link, verify=False)

        soup = bs(page.content, 'html.parser')

        for div in soup.findAll('div', attrs={'class': 'a-section'}):
            name = div.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
            if name and name not in product_names:
                product = Product()
                product_names.add(name)
                price = div.find('span', attrs={'class': 'a-price-whole'})
                # currency = d.find('span', attrs={'class': 'a-price-symbol'})
                rating = div.find('span', attrs={'class': 'a-icon-alt'})
                ratings_count = div.find('span', attrs={'class': 'a-size-base s-underline-text'})
                try:
                    link = div.find_all('a')[0].get('href')
                    product.site = 'amazon.in'
                    product.name = name.string
                    product.price = int(price.string.replace(',', ''))
                    product.rating = float(rating.string.split(' ')[0])
                    product.ratings_count = int(ratings_count.string.replace(',', ''))
                    product.url = None if link is None else f'https://amazon.in{link}'
                    results.append(product.__dict__)
                except Exception as exp:
                    print(exp)
    return {
        'status': Constants.SUCCESS,
        'error_msg': '',
        'data': results
    }


def get_amazon_product_info(url: str) -> dict:
    # page = requests.get(url, verify=True) ##request module cause robot verification so being faced out##
    try:
        page = httpx.get(url, verify=False)
    except httpx.ConnectError:
        error_msg = f'SSL certificate error for url {url}, try with verify false in code'
        return {
            'status': Constants.FAILURE,
            'error_msg': error_msg,
            'data': {}
        }
    # except Exception as e:
    # 	print (e)
    # 	return
    soup = bs(page.content, features='lxml')
    req_soup = soup.find(id='centerCol')
    try:
        product = Product()
        product.name = req_soup.find(id='productTitle').get_text().strip()
        if req_soup.find('span', attrs={'class': 'a-price a-text-price a-size-medium apexPriceToPay'}) is not None:
            price_element = req_soup.find('span', attrs={'class': 'a-price a-text-price a-size-medium apexPriceToPay'}
                                          ).find('span', attrs={'class': 'a-offscreen'})
        else:
            price_element = req_soup.find('span', attrs={'class': 'a-price-whole'})
        price_str = price_element.get_text()
        rating = req_soup.find('span', attrs={'class': 'a-icon-alt'})
        if rating is not None:
            rating = rating.get_text()
        ratings_count = req_soup.find(id='acrCustomerReviewText')
        if ratings_count is not None:
            ratings_count = ratings_count.get_text()
    except Exception as exp:
        error_msg = f'exception in getting product info = {exp}'
        return {
            'status': Constants.ERROR,
            'error_msg': error_msg,
            'data': {}
        }

    try:
        product.availability_message = soup.select(
            '#availability .a-color-success')[0].get_text().strip()
        product.availability = True
    except Exception:
        try:
            product.availability_message = soup.select(
                '#availability .a-color-price')[0].get_text().strip()
            product.availability = True
        except Exception:
            product.availability_message = None
            product.availability = False

    try:
        price = unicodedata.normalize('NFKD', price_str)
        price = price.split('.')[0].replace(',', '').replace('₹', '')
        product.price = float(price)
        product.rating = float(rating.split(' ')[0])
        product.ratings_count = int(req_soup.find(
            id='acrCustomerReviewText').get_text().replace(',', '').split(' ')[0])
    except Exception as exp:
        error_msg = f'exception in getting product info = {exp}'
        return {
            'status': Constants.ERROR,
            'error_msg': error_msg,
            'data': {}
        }

    data = product.__dict__
    return {
        'status': Constants.SUCCESS,
        'error_msg': '',
        'data': data
    }


if __name__ == '__main__':
    import time

    start_time = time.time()
    data2 = get_amazon_results_by_search('mobile', 10)
    print(data2['data'])
    print(len(data2['data']))
    print(f"--- {time.time() - start_time} seconds ---")

    start_time = time.time()
    data2 = Amazon().multithread_search_data('mobile', 10)
    print(data2)
    print(len(data2))
    data2.sort()
    print(f"--- {time.time() - start_time} seconds ---")
