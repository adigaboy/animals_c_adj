import asyncio
from collections import defaultdict
from typing import Dict

import aiofiles
import aiohttp
from bs4 import BeautifulSoup


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://en.wikipedia.org/wiki/List_of_animal_names') as response:
            if response.status == 200:
                html = await response.text()
            else:
                raise Exception(f'Get page failed with status_code: {response.status}')

        # remove from HTML the animal Alphabets rows from the table that break it
        bs = BeautifulSoup(html, 'lxml')
        for th in bs.find_all('th', {'colspan': '7'}):
            th.parent.decompose()

        terms_by_species_or_taxon_table_rows = bs.find_all('table')[2].find_all('tr')
        animal_index = 0
        collateral_adjectives_index = 5

        awaitables = []
        # group animals under collateral adjectives in a dict
        collateral_adjectives_animals = defaultdict(dict)
        for row in terms_by_species_or_taxon_table_rows[1:]:
            cells = row.find_all('td')
            if cells[collateral_adjectives_index].text == '—' or cells[collateral_adjectives_index].text == '':
                # some animals dont have collateral adjective
                continue
            c_adjectives = cells[collateral_adjectives_index].text.split(' ')
            for c_a in c_adjectives:
                animal = cells[animal_index].a['title']
                collateral_adjectives_animals[c_a][animal] = None
                awaitables.append(download_animal_pic(session, c_a, animal, cells[animal_index].a['href']))
        responses = await asyncio.gather(*awaitables)
        for c_adj, animal, f_name in responses:
            collateral_adjectives_animals[c_adj][animal] = f_name
        return collateral_adjectives_animals


async def download_animal_pic(session: aiohttp.ClientSession, c_adj: str, animal: str, href: str) -> None:
    async with session.get(f'https://en.wikipedia.org{href}') as response:
        if response.status == 200:
            html = await response.text()
        else:
            raise Exception('error')
    bs = BeautifulSoup(html, 'lxml')
    image_url = f"https:{bs.find_all('a', {'class': 'mw-file-description'})[0].img['src']}"
    async with session.get(image_url) as response:
        if response.status == 200:
            async with aiofiles.open(f'/tmp/{animal}.{image_url.split(".")[-1]}', mode='wb') as f:
                await f.write(await response.read())
                return c_adj, animal, f.name


def output_as_html_file(collateral_adjectives_animals: Dict[str, Dict[str, str]]) -> None:
    table = '''
        <table border="1">\n
            <thead>
                <tr>
                    <th>Collateral Adjective</th>
                    <th>Animal</th>
                    <th>Image</th>
                </tr>
            </thead>
            <tbody>
    '''
    for c_adj, animals in collateral_adjectives_animals.items():
        table += f'''
            <tr>
                <th>{c_adj}</th>
                <td>{", ".join(animals.keys())}</td>
                <td>{", ".join([f'<img src="../../../../{f_name}"/>' for f_name in animals.values()])}</td>
            </tr>
        '''
    with open('output.html', 'w') as fd:
        fd.write(table)


if __name__ == '__main__':
    collateral_adjectives_animals = asyncio.run(main())
    print(collateral_adjectives_animals)
    output_as_html_file(collateral_adjectives_animals)
