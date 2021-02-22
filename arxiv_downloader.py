import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import os


POOL_SIZE = 12


def pdf_downloader(link):
    paper_url = f'https://export.arxiv.org{link}'

    ind = link.rfind('/') + 1
    file_name = f'{link[ind:]}'
    print(file_name)
    print(paper_url)

    response_pdf = requests.get(paper_url)

    if response_pdf.status_code != 200:
        print(f'Unable to download paper {paper_url}')
        return

    with open(f'data/{file_name}', 'wb') as f:
        f.write(response_pdf.content)


if __name__ == '__main__':
    # starts from 1992
    time_range = range(2000, 2022)

    urls = []
    os.makedirs('data', exist_ok=True)

    for year in time_range:
        year_prefix = str(year)[2:]
        for month in range(1, 13):
            urls.append(f'https://export.arxiv.org/list/astro-ph/{year_prefix}{month:02d}?show=1000000')


    for url in urls:
        response = requests.get(url)

        if response.status_code != 200:
            print(f'There was an error retrieiving the page: {url}')
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = [ a_tag.get('href') + '.pdf' for a_tag in soup.find_all('a', attrs={'title': 'Download PDF'}) ]
        print(f'Number of papers found for {url} is {len(links)}')

        with Pool(POOL_SIZE) as p:
            p.map(pdf_downloader, links)
