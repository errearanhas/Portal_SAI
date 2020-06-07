import requests
import pandas as pd
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import time
import os


# Disclaimer: decisions before 01/01/2008 were manually excluded from this analysis.

df = pd.read_csv('list_decisions_parties.txt', sep=";", header=None)
# df = pd.read_csv('list_decisions_nep.txt', sep=";", header=None)
# df = pd.read_csv('list_decisions_conf.txt', sep=";", header=None)
urls = df[0]


def fetch_acordao(url, topic='RPT'):
    """
    Base function to get decisions URL and download the document
    """
    if topic == 'RPT':
        try:
            name = url.split('=')[-1]
        except:
            try:
                name = url.split("\\")[-1]
            except:
                name = url.split('/')[-1]
    elif topic == 'NEPOTISM':
        try:
            name = url.split('=')[-1]
        except:
            name = url.split("\\")[-1]
    elif topic == 'CONF_INTEREST':
        name = url.split('=')[-1] + str(".doc")

    if not os.path.exists(name):
        r = requests.get(url, allow_redirects=True)
        open(location, 'wb').write(r.content)
        time.sleep(5)
    return 1


def get_in_multiprocess(url_list, threads=8):
    """
    Function to fetch decisions in multiprocess task, if computer is able
    """
    print('Starting process ---- ' + time.ctime(time.time()))
    results = ThreadPool(threads).imap_unordered(fetch_acordao, url_list)
    count = 0
    for _ in tqdm(results):
        count += 1
    print('Files found: ' + str(count))
    print('Process finished ---- ' + time.ctime(time.time()))
    return


def get_in_queue(url_list):
    """
    Function to fetch decisions in a queue, without multiprocess functionality
    """
    for i in tqdm(url_list):
        fetch_acordao(i)
    return


def not_fetch_yet(df, url):
    """
    Function to generate a list of decisions not yet downloaded.
    """
    for i in url:
        name = i.split('=')[-1] + str(".doc")
        location = name
        if not os.path.exists(location):
            l.append(name)
    list_not = df[df[0].apply(lambda x: x.split("=")[-1]).isin([i.split(".")[0] for i in l])]
    return list_not
