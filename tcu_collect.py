# -*- coding: utf-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import time


def click_download(driver, xpath):
    button = driver.find_element_by_xpath(xpath)
    button.click()
    button_word = driver.find_element_by_xpath("//*[@title='Fazer download do documento no formato WORD.']")
    button_word.click()
    return


def goto_next_page(driver):
    try:
        next_page = driver.find_element_by_xpath(
            '//*[@id="container"]/div[1]/div[2]/div/header/div[2]/mat-paginator/div/div/div[2]/button[2]')
        next_page.click()
    except:
        pass
    return


def count_acordaos_current_page(driver):
    page = BeautifulSoup(driver.page_source, 'lxml')
    number_acordaos_in_page = len(page.find_all('button', {'title': 'Fazer download do documento.'}))
    return number_acordaos_in_page


def main():
    print('Starting process ---- ' + time.ctime(time.time()))
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)  # run if chromedriver is in PATH
    driver.get(url)

    number_acordaos_in_page = count_acordaos_current_page(driver)

    for i in range(number_acordaos_in_page):
        try:
            xpath = '//*[@id="lista-resultado__itens"]/ul/li[' + str(i) + ']/div/div[2]/button'
            click_download(driver, xpath)
        except:
            goto_next_page(driver)

    print('Done ---- ' + time.ctime(time.time()))
    driver.close()
    return


if __name__ == "__main__":
    url_acordaos = \
        "https://pesquisa.apps.tcu.gov.br/#/resultado/acordao-completo/%2522partes%2520relacionadas%2522/%2520/%2520"
    url = url_acordaos
    main()
