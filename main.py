from collections import defaultdict
from io import StringIO
from typing import Dict, List

import numpy as np
import pandas as pd
import wikipedia
from bs4 import BeautifulSoup


def main():
    df = scrape_page_and_get_table()

    # group animals under collateral adjectives in a dict
    collateral_adjectives_animals = defaultdict(list)
    for row in df.iloc:
        if not row['Collateral adjective'] or row['Collateral adjective'] == '—':
            # some animals dont have collateral adjective
            continue
        c_adjectives = row['Collateral adjective'].split(' ')
        for c_a in c_adjectives:
            collateral_adjectives_animals[c_a].append(row.Animal)
    return collateral_adjectives_animals

def scrape_page_and_get_table() -> pd.DataFrame:
    # read wikipedia page using library
    html = wikipedia.page('List of animal names').html()

    # remove from HTML the animal Alphabets rows from the table that break it
    bs = BeautifulSoup(html, 'lxml')
    for th in bs.find_all('th', {'colspan': '7'}):
        th.parent.decompose()

    # read the table into pandas dataframe
    df = pd.read_html(StringIO(str(bs)))[2]
    df = df.replace({np.nan: None})

    return df

def output_as_html_file(collateral_adjectives_animals: Dict[str, List[str]]) -> None:
    # transform dict to a pandas data frame
    df = pd.DataFrame.from_dict(
        {
            c_adj: [', '.join(animals)] for c_adj, animals in  collateral_adjectives_animals.items()
        },
        orient='index',
        columns=['animals']
    )
    df.columns.name = 'Collateral Adjective'

    with open('output.html', 'w') as fd:
        fd.write(df.to_html())


if __name__ == '__main__':
    collateral_adjectives_animals = main()
    print(collateral_adjectives_animals)
    output_as_html_file(collateral_adjectives_animals)
