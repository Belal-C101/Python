import requests
import os
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from tkinter import simpledialog, messagebox
import tkinter as tk
import time


def get_input():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    url = simpledialog.askstring("URL", "Enter URL:")
    if url is None:
        messagebox.showerror("Input Error", "No input provided for URL.")
        root.destroy()
        return None, None

    epi = simpledialog.askinteger("Episode", "Enter episodes:")
    if epi is None:
        messagebox.showerror("Input Error", "No input provided for episodes.")
        root.destroy()
        return None, None

    return url, epi


def initialize_driver():
    edge_options = EdgeOptions()
    edge_options.add_extension(r'D:\TukTuk Cinema (Upbom)\Extension\uBlock-Origin.crx')
    # edge_options.add_extension(r'D:\TukTuk Cinema (Upbom)\Extension\AdBlocker.crx')
    # edge_options.add_extension(r'D:\TukTuk Cinema (Upbom)\Extension\IDM-Integration-Module.crx')

    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)
    driver.maximize_window()
    return driver


def scrape_links(driver, url, epi):
    megamax = []
    mix = []

    driver.get(url)
    for episode in range(1, epi + 1):
        current_url = driver.current_url
        if "watch/" not in current_url:
            try:
                download_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.watchAndDownlaod"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
                driver.execute_script("arguments[0].click();", download_button)
            except (ElementClickInterceptedException, TimeoutException):
                print("Download button not clickable or not found")

        src = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(src, "lxml")

        down_butt = soup.find("a", {"class": "download--item"})
        if down_butt:
            link = down_butt.get('href')
            if link:
                megamax.append(link)

        if episode == epi:
            break

        try:
            next_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.next"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            driver.execute_script("arguments[0].click();", next_button)
        except (ElementClickInterceptedException, TimeoutException):
            print("Next button not clickable or not found")

    return megamax, mix


def scrape_mixdrop_links(driver, megamax, epi, mix):
    for mixdrop in megamax:
        driver.get(mixdrop)
        src = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(src, "lxml")

        try:
            download_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.v-btn.v-theme--dark.text-orange.v-btn--density-default.v-btn--rounded.v-btn--size-default.v-btn--variant-tonal"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
            download_button.click()
        except (ElementClickInterceptedException, TimeoutException):
            print("Download button not clickable or not found")

        time.sleep(2)
        src = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(src, "lxml")

        links = soup.find_all("div", {"class": "v-virtual-scroll__item"})
        for tag in links:
            tag_a = tag.find("div", {"class": "v-list-item-title"}).text.strip()
            if tag_a and "streamwish" in tag_a:
                mixdrops_a = tag.find("div", {"class": "v-list-item__append"}).find("a")
                if mixdrops_a:
                    inc = mixdrops_a.get('href')
                    if inc:
                        mix.append(f"https:{inc}")

    return mix

download_dir = r'C:\Users\belal\Downloads'
def wait_for_downloads(download_dir, timeout=300):
    start_time = time.time()
    
    # Loop until timeout is reached
    while time.time() - start_time < timeout:
        # Check for files that are still being downloaded
        if any(filename.endswith('.crdownload') for filename in os.listdir(download_dir)):
            print("Downloads are still in progress...")
            time.sleep(5)  # Check every 10 seconds
        else:
            print("All downloads complete.")
            return
    
    # If the loop ends without finding a .crdownload file, print a timeout message
    print("Timed out waiting for downloads to complete.")

def download_files(driver, mix):
    for link in mix:
        driver.get(link)
        src = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(src, "lxml")

        try:
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.downloadv-item"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
            download_button.click()
            time.sleep(2)
        except (ElementClickInterceptedException, TimeoutException, NoSuchElementException):
            print("Download button not clickable or not found in the first attempt")

        try:
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.g-recaptcha.btn.btn-primary.submit-btn.py-3.px-4.justify-content-start"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
            download_button.click()
            time.sleep(2)
        except (ElementClickInterceptedException, TimeoutException, NoSuchElementException):
            print("Download button not clickable or not found in the second attempt")

        try:
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.dwnlonk"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
            download_button.click()
            time.sleep(2)
        except (ElementClickInterceptedException, TimeoutException, NoSuchElementException):
            print("Download button not clickable or not found in the third attempt")

    wait_for_downloads(download_dir)

def save_to_csv(megamax, mix):
    file_list = [megamax, mix]
    exported = zip_longest(*file_list)
    with open(r"\TukTuk Cinema (Upbom)\EXCEL\TukTuk_Cinema.csv", "w", encoding='utf-8', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(["Mega Max", "Mixdrop"])
        wr.writerows(exported)


def main():
    url, epi = get_input()
    if url and epi:
        driver = initialize_driver()
        try:
            megamax, mix = scrape_links(driver, url, epi)
            mix = scrape_mixdrop_links(driver, megamax, epi, mix)
            download_files(driver, mix)
        finally:
            driver.quit()
        save_to_csv(megamax, mix)


if __name__ == "__main__":
    main()
