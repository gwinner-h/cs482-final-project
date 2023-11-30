import threading
import queue
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import time


def get_links():
    time.sleep(2)
    links = driver.find_elements(By.CLASS_NAME, "blocklink")
    return [link.get_attribute("href") for link in links]


def click_next_and_get_links(xpath):
    try:
        next_page_button = driver.find_element(By.XPATH, xpath)
        next_page_button.click()
        new_urls = get_links()
        return new_urls
    except NoSuchElementException:
        return []


def download_logs(url_queue, download_path):
    while True:
        url = url_queue.get()
        if url is None:
            break  # sentinel value to signal end of processing
        log_url = f"{url}.log"
        response = requests.get(log_url)
        log_name = url.split("/")[-1]
        log_path = download_path / f"{log_name}.log"
        with open(log_path, "wb") as f:
            f.write(response.content)
        url_queue.task_done()


DOWNLOAD_PATH = Path() / "logs"
DOWNLOAD_PATH.mkdir(exist_ok=True)

url_queue = queue.Queue()
download_thread = threading.Thread(
    target=download_logs, args=(url_queue, DOWNLOAD_PATH))
download_thread.start()

driver = webdriver.Chrome()

try:
    driver.get("https://replay.pokemonshowdown.com/?format=gen9ou")
    urls = get_links()
    for url in urls:
        url_queue.put(url)

    next_page_xpath = "/html/body/div[1]/div/div/div[1]/section/form/p[6]/a"
    while True:
        next_page_urls = click_next_and_get_links(next_page_xpath)
        if not next_page_urls:
            break
        for url in next_page_urls:
            url_queue.put(url)
        next_page_xpath = "/html/body/div[1]/div/div/div[1]/section/form/p[7]/a"
finally:
    driver.quit()

url_queue.put(None)
download_thread.join()