import asyncio
import os
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

        # get the html table with list of animals
        terms_by_species_or_taxon_table_rows = bs.find_all('table')[2].find_all('tr')
        animal_index = 0
        collateral_adjectives_index = 5

        awaitables = []
        # group animals under collateral adjectives in a dict
        collateral_adjectives_animals = defaultdict(dict)
        for row in terms_by_species_or_taxon_table_rows[1:]:
            cells = row.find_all('td')
            if cells[collateral_adjectives_index].text in ['—', '']:
                # skip animals that dont have collateral adjective
                continue
            # some animals have multiple collateral adjectives, need to cover all
            c_adjectives = cells[collateral_adjectives_index].text.split(' ')
            for c_a in c_adjectives:
                # get title instead of text because sometimes text have additional info
                animal = cells[animal_index].a['title']
                collateral_adjectives_animals[c_a][animal] = None
                awaitables.append(download_animal_pic(session, c_a, animal, cells[animal_index].a['href']))
        # gather image download tasks and await for them
        responses = await asyncio.gather(*awaitables)
        for c_adj, animal, f_name in responses:
            # save downloaded file name for displaying later in the html
            collateral_adjectives_animals[c_adj][animal] = f_name
        return collateral_adjectives_animals


async def download_animal_pic(session: aiohttp.ClientSession, c_adj: str, animal: str, href: str) -> None:
    # get the animal wikipedia page to extract the image url
    async with session.get(f'https://en.wikipedia.org{href}') as response:
        if response.status == 200:
            html = await response.text()
        else:
            return c_adj, animal, None
    # extract image url
    bs = BeautifulSoup(html, 'lxml')
    image_url = f"https:{bs.find_all('a', {'class': 'mw-file-description'})[0].img['src']}"
    # filename to save image to
    filename = f'/tmp/{animal}.{image_url.split(".")[-1]}'
    if os.path.exists(filename):
        return c_adj, animal, filename
    # download image and write it to filename in tmp folder
    async with session.get(image_url) as response:
        if response.status == 200:
            async with aiofiles.open(filename, mode='wb') as f:
                await f.write(await response.read())
                return c_adj, animal, f.name
        else:
            return c_adj, animal, None


def output_as_html_file(collateral_adjectives_animals: Dict[str, Dict[str, str]]) -> None:
    # prepare table headers
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
        # add row for each collateral adjective with animal names and images.
        table += f'''
            <tr>
                <th>{c_adj}</th>
                <td>{", ".join(animals.keys())}</td>
                <td>{", ".join([f'<img src="../../../../{f_name}"/>' for f_name in animals.values()])}</td>
            </tr>
        '''
    # write table content to file
    with open('output.html', 'w') as fd:
        fd.write(table)


if __name__ == '__main__':
    collateral_adjectives_animals = asyncio.run(main())
    print(collateral_adjectives_animals)
    output_as_html_file(collateral_adjectives_animals)
