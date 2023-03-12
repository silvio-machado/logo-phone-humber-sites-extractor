import sys
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def find_logo_url(session, url):
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')
    logo_element = soup.find('img', {'alt': 'Logo'})
    if logo_element:
        logo_url = logo_element.get('src')
        if logo_url.startswith('/'):
            logo_url = f"{url}{logo_url}"
        return logo_url


async def find_phone_numbers(session, url):
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')
    phone_elements = soup.find_all('a', href=lambda href: href and 'tel:' in href)
    phones = [element['href'].replace('tel:', '') for element in phone_elements]
    phones = [phone.replace('-', '').replace('(', '').replace(')', '').replace('+', '').replace('.', '').strip() for phone in phones]
    phones = [phone for phone in phones if phone.isdigit()]
    return phones


async def process_url(session, url):
    logo_url = await find_logo_url(session, url)
    phones = await find_phone_numbers(session, url)
    return {'url': url, 'logo_url': logo_url, 'phones': phones}


async def main():
    async with aiohttp.ClientSession() as session:
        urls = sys.stdin.read().splitlines()
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(process_url(session, url)))
        results = await asyncio.gather(*tasks)
        for result in results:
            print(json.dumps(result))


if __name__ == '__main__':
    asyncio.run(main())
