import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
from latest_user_agents import get_random_user_agent
import csv


@dataclass
class Product:
    product_link: str
    title: str

def get_html(page):
    headers = {
        'User-Agent': get_random_user_agent()
    }
    url = f'https://www.guitarcenter.com/All-Deals.gc?N=18144#pageName=collection-page&N=18144+50723&Nao=30&recsPerPage=90&profileCountryCode=BJ&profileCurrencyCode=XOF'
    resp = httpx.get(url, headers=headers)
    return HTMLParser(resp.text)

def parse_product(html):
    products = html.css('div.productDetails')
    results = []
    for item in products:
        new_item = Product(
            product_link = 'https://www.guitarcenter.com' + item.css_first('.productTitle a').attributes['href'],
            title = item.css_first('.productTitle a').text().strip(),
        )
        results.append(asdict(new_item))
    return results

def to_csv(res):
    with open('results.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=['product_link', 'title'])
        writer.writerows(res)

def main():
    for x in range(0, 90, 60):
        print(x)
        html = get_html(x)
        res = parse_product(html)
        to_csv(res)

if __name__ == '__main__':
    main()