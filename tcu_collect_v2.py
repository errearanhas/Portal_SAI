import requests
import pandas as pd
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import time
import os


df = pd.read_csv('list_acordaos.txt', sep=";", header=None)
urls = df[0]


def fetch_acordao(url):
    name = url.split('=')[-1] + str(".doc")
    location = '../Portal_TCU_conflito_interesse/raw_req/' + name
    if not os.path.exists(location):
        r = requests.get(url, allow_redirects=True)
        open(location, 'wb').write(r.content)
        time.sleep(5)
    return name


def get_in_multiprocess(url_list, threads=4):
    print('Starting process ---- ' + time.ctime(time.time()))
    results = ThreadPool(threads).imap_unordered(fetch_acordao, url_list)
    count = 0
    for _ in tqdm(results):
        count += 1
    print('Files found: ' + str(count))
    print('Process finished ---- ' + time.ctime(time.time()))
    return


def get_in_queue(url_list):
    for i in tqdm(url_list):
        fetch_acordao(i)
    return
