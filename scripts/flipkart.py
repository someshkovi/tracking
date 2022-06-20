import dataclasses

from bs4 import BeautifulSoup as bs
import requests
import re
import unicodedata
import traceback


def get_text(bs_attr, default=None):
    if bs_attr is None:
        return default
    out = bs_attr.text
    return out


def get_flipkart_results_by_search(search_parameter, no_of_pages=20, other_params={}):
    results = []
    for page in range(no_of_pages):
        link = f'https://www.flipkart.com/search?q={search_parameter}&page={page}'
        page = requests.get(link, verify=False)
        soup = bs(page.content, 'html.parser')
        for data in soup.findAll('div', class_='_3pLy-c row'):
            name = get_text(data.find('div', attrs={'class': '_4rR01T'}))
            price = get_text(data.find('div', attrs={'class': '_30jeq3 _1_WHN1'}))
            if isinstance(price, str):
                price = int(price.replace('₹', '').replace(',', ''))
            rating = float(get_text(data.find('div', attrs={'class': '_3LWZlK'})))
            specification = data.find('div', attrs={'class': 'fMghEO'})
            ratings_reviews = get_text(data.find('span', attrs={'class': '_2_R_DZ'}))
            if isinstance(ratings_reviews, str):
                rtrv = unicodedata.normalize("NFKD", ratings_reviews).replace(',', '').split()
                if len(rtrv) == 5 and rtrv[1] == 'Ratings' and rtrv[4] == 'Reviews':
                    ratings_count = int(rtrv[0])
                    reviews_count = int(rtrv[3])
            for each in specification:
                col = each.find_all('li', attrs={'class': 'rgWa7D'})
                specifications = []
                for x in range(len(col)):
                    specifications.append(get_text(col[x]))
            product = {
                'name': name,
                'price': price,
                'rating': rating,
                'specifications': specifications,
                'ratings_count': ratings_count,
                'reviews_count': reviews_count,
            }
            for key in other_params:
                product['key'] = get_text(data.find(other_params['key'][0],
                                                    attrs={other_params['key'][1]: other_params['key'][2]}))
            results.append(product)

    return {
        'status': 'success',
        'data': results,
        'error_msg': '',
    }


def get_flipkart_product_info(url):
    page = requests.get(url, verify=False)
    soup = bs(page.content, 'html.parser')
    data = soup.find('div', {'class': 'aMaAEs'})
    name = get_text(data.find('span', attrs={'class': 'B_NuCI'}))
    price = get_text(data.find('div', attrs={'class': '_30jeq3 _16Jk6d'}))
    if isinstance(price, str):
        price = int(price.replace('₹', '').replace(',', ''))
    rating = get_text(data.find('div', attrs={'class': '_3LWZlK'}))
    if rating is not None:
        rating = float(rating)
        ratings_reviews = get_text(data.find('span', attrs={'class': '_2_R_DZ'}))
        if isinstance(ratings_reviews, str):
            rtrv = unicodedata.normalize("NFKD", ratings_reviews).replace(',', '').split()
            if len(rtrv) == 5 and rtrv[1] == 'Ratings' and rtrv[4] == 'Reviews':
                ratings_count = int(rtrv[0])
                reviews_count = int(rtrv[3])
    else:
        ratings_count = 0
        reviews_count = 0
    if get_text(soup.find('div', attrs={'class': '_16FRp0'})) is None:
        availability = True
    else:
        availability = False
    if get_text(soup.find('div', attrs={'class': '_1dVbu9'})) is None:
        availability_message = get_text(soup.find('div', attrs={'class': '_2JC05C'}))
    else:
        availability_message = get_text(soup.find('div', attrs={'class': '_1dVbu9'}))

    product = {
        'name': name,
        'price': price,
        'rating': rating,
        'ratings_count': ratings_count,
        'reviews_count': reviews_count,
        'availability': availability,
        'availability_message': availability_message,
    }
    return {
        'status': 'success',
        'data': product,
        'error_msg': '',
    }


def main():
    query = input('Enter the search parameter: \n')
    results = get_flipkart_results_by_search(search_parameter=query, no_of_pages=20, other_params={})
    if results.get('status') == 'success':
        import pandas as pd

        df = pd.DataFrame(results)
        df = df.loc[:, ~df.columns.duplicated()]
        print(df.head())
        df.to_csv(f'{query}.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    try:
        value = get_flipkart_product_info(
            'https://www.flipkart.com/gigastar-intel-core-i7-3770-8-gb-ram-ssd-120gb-integrated-graphics-1000-hard-disk-windows-10-pro-64-bit-1-graphics-memory-gaming-tower/p/itm9931a01a28747?pid=CPUGDXBUTHHCVETQ&lid=LSTCPUGDXBUTHHCVETQ5XIQI7&marketplace=FLIPKART&store=6bo%2Fnl4%2Fdze&srno=b_10_364&otracker=browse&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_7_L2_view-all&fm=organic&iid=121b0986-de9c-4051-84af-5ce85d92676c.CPUGDXBUTHHCVETQ.SEARCH&ppt=browse&ppn=browse&ssid=wu3la2yj9c0000001654862177387')

    except:
        error_msg = traceback.format_exc()
        print(error_msg)
