import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs


class AnimeScraper(object):
    def __init__(self, pages_count: int):
        self.url = 'https://myanimelist.net/topanime.php?limit='
        self.pages_count = pages_count
        self.anime_data = {}
        asyncio.run(self.main())

    # Get page html text
    async def fetch(self, session, page_url):
        async with session.get(page_url) as response:
            if response.status == 200:
                html_text = await response.text()
                await self.get_detail_anime_urls_from_page(html_text, session)

    # Get anime info from page
    async def get_anime_data(self, session, url):
        def none_validation(value):
            if value is None:
                return None
            return value.getText()

        async with session.get(url) as response:
            if response.status == 200:
                anime_info = {}
                html_text = await response.text()
                soup = bs(html_text, 'html.parser')

                anime_info['score'] = float(none_validation(soup.find('span', attrs={'itemprop': 'ratingValue'})))
                if anime_info.get('score') < 8.00:
                    return

                title_div = soup.find('div', class_='h1-title')
                anime_title = title_div.find('h1', class_='title-name h1_bold_none').getText()
                description = none_validation(soup.find('p', attrs={'itemprop': 'description'}))
                anime_info['description'] = description.replace('[Written by MAL Rewrite]', '').replace('<br/>', '')
                anime_info['type'] = none_validation(soup.find('span', attrs={'class': 'information type'}))
                anime_info['season'] = none_validation(soup.find('span', attrs={'class': 'information season'}))
                anime_info['studio'] = none_validation(soup.find('span', attrs={'class': 'information studio author'}))

                genres_items = soup.findAll('span', attrs={'itemprop': 'genre'})
                anime_info['genres'] = [none_validation(item) for item in genres_items]

                anime_info['image'] = soup.find('img', attrs={'alt': anime_title})['data-src']
                self.anime_data[anime_title] = anime_info

    # Get url for detail anime page
    async def get_detail_anime_urls_from_page(self, html_text, session):
        soup = bs(html_text, 'html.parser')
        all_anime = soup.findAll('a', class_='hoverinfo_trigger fl-l ml12 mr8', href=True)
        tasks = [self.get_anime_data(session, anime.get('href')) for anime in all_anime]
        await asyncio.gather(*tasks)

    async def main(self):
        # Generate urls
        urls = [f'{self.url}{page_cnt}' for page_cnt in range(0, self.pages_count, 50)]
        # Generate tasks
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in urls]
            await asyncio.gather(*tasks)


class GenresScraper(object):
    def __init__(self):
        self.url = 'https://myanimelist.net/anime/genre/info'
        self.genres_data = []
        asyncio.run(self.main())

    async def fetch(self, session):
        async with session.get(self.url) as response:
            if response.status == 200:
                html_text = await response.text()
                await self.get_genres_info(html_text)

    async def get_genres_info(self, html_text):
        soup = bs(html_text, 'html.parser')
        genres_items = soup.findAll('li')
        self.genres_data = [item.find('strong').getText() for item in genres_items]

    async def main(self):
        async with aiohttp.ClientSession() as session:
            await self.fetch(session)


class StudiosScraper(object):
    def __init__(self):
        self.url = 'https://myanimelist.net/anime/producer'
        self.studios_data = []
        asyncio.run(self.main())

    async def fetch(self, session):
        async with session.get(self.url) as response:
            if response.status == 200:
                html_text = await response.text()
                await self.get_studios_info(html_text)

    async def get_studios_info(self, html_text):
        soup = bs(html_text, 'html.parser')
        studio_items = soup.findAll('a', attrs={'class': 'genre-name-link'})
        for item in studio_items:
            studio_raw = item.getText()
            self.studios_data.append(studio_raw[:studio_raw.index('(')].strip())

    async def main(self):
        async with aiohttp.ClientSession() as session:
            await self.fetch(session)
