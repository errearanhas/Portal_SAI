import requests
import pandas as pd
from multiprocessing.pool import ThreadPool

df = pd.read_csv('list_acordaos.txt', sep=";", header=None)
urls = df[0].head(3)


def fetch_acordao(url):
    name = url.split('=')[-1] + str(".doc")
    r = requests.get(url, allow_redirects=True)
    location = '../Portal_TCU_conflito_interesse/raw_req/' + name
    open(location, 'wb').write(r.content)
    return name


results = ThreadPool(4).imap_unordered(fetch_acordao, urls)


count = 0
for name in results:
    count += 1
    print(count)