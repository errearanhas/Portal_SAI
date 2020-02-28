# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import itertools
import time


def click_download(driver, xpath):
    """
    Click in download button and chooses DOCX as file format
    """
    # button = driver.find_element_by_xpath(xpath)
    button = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH, xpath)))
    driver.execute_script("arguments[0].click();", button)
    # button.click()
    button_word = driver.find_element_by_xpath("//*[@title='Fazer download do documento no formato WORD.']")
    # button_word.click()
    driver.execute_script("arguments[0].click();", button_word)
    return


def goto_next_page(driver):
    """
    Click in the next page button
    """
    try:
        next_page = WebDriverWait(driver, 60).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div[1]/div[2]/div/header/div[2]/mat-paginator/div/div/div[2]/button[2]')))
        #next_page = driver.find_element_by_xpath('//*[@id="container"]/div[1]/div[2]/div/header/div[2]/mat-paginator/div/div/div[2]/button[2]')
        driver.execute_script("arguments[0].click();", next_page)
        # next_page.click()
    except:
        print("Não clicou próxima página!")
        return 1
    return


def count_acordaos_current_page(driver):
    """
    Get the number of 'acórdãos' in current page
    """
    page = BeautifulSoup(driver.page_source, 'lxml')
    number_acordaos_in_page = len(page.find_all('button', {'title': 'Fazer download do documento.'}))
    return number_acordaos_in_page


def download_acordaos_in_page(number_acordaos_in_page, driver):
    for i in range(number_acordaos_in_page):
        xpath = '//*[@id="lista-resultado__itens"]/ul/li[' + str(i+1) + ']/div/div[2]/button'
        click_download(driver, xpath)
        time.sleep(20)
    return


def main():
    print('Starting process ---- ' + time.ctime(time.time()))
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    # options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)  # run if chromedriver is in PATH
    driver.get(url)

    number_acordaos_in_page = count_acordaos_current_page(driver)

    for idx, val in enumerate(itertools.cycle(range(81))):
        download_acordaos_in_page(number_acordaos_in_page, driver)
        time.sleep(20)
        if goto_next_page(driver) == 1:
            break
        time.sleep(20)
        if idx > 810:
            break

    print('Done ---- ' + time.ctime(time.time()))
    driver.close()
    return


if __name__ == "__main__":
    url_acordaos = "https://pesquisa.apps.tcu.gov.br/#/resultado/acordao-completo/%2522conflito%2520de%2520interesse%2522/DTRELEVANCIA%253A%255B20080101%2520to%252020190812%255D/%2520"
    url = url_acordaos
    main()
