from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import random

product_url_list = list()
list_for_excel = list()
phone_number_list = list()

w_url = input("Veri çekilecek link: ")
excel_file = input("Kaydedilecek dosya adı: ")

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36", 
    "X-Amzn-Trace-Id": "Root=1-6209086d-6b68c17b4f73e9d6174b5736"
}

browser = webdriver.Firefox()

def scrapePhoneNumber(url):
    print(f"LİNK: {url}\n")
    waiting_time = random.randint(3,7)
    browser.get(url)
    time.sleep(waiting_time)

    try:
        browser.find_element_by_xpath('//*[@id="classifiedDetail"]/div/div[2]/div[3]/div/div[1]/div[3]/div[2]/button[1]').click()
        time.sleep(0.5)
    except:
        pass

    r = browser.page_source
    soup = BeautifulSoup(r, "lxml")

    print("TELEFON NUMARASI\n-------------------")

    try:
        phone_values = soup.find_all("span", attrs={"class":"phone-value"})
        for i in phone_values:
            phone_value = i.getText().strip()
            if(phone_value.startswith("0 (5")):
                phone_number_list.append(phone_value)
                print(phone_value)
    except:
        pass

    phone_number = "-"
    try:
        phone_numbers = soup.find_all("span", attrs={"class":"pretty-phone-part show-part"})
        for i in phone_numbers:
            phone_number = i.getText().strip()
            if(phone_number.startswith("0 (5")):
                phone_number_list.append(phone_number)
                print(phone_number)
    except:
        pass
    
    name = "-"
    try:
        name = soup.find("div", attrs={"class":"username-info-area"}).find("h5").getText().strip()
        print(name)
    except:
        pass
    
    il = "-"
    ilce = "-"
    try:
        h2_text_list = list()
        h2_tags = soup.find_all("h2")
        for i in h2_tags:
            h2_text = i.getText().strip("\n")
            h2_text_list.append(h2_text)
        il_ilce = h2_text_list[2].strip().strip("\n").split("/")
        il = il_ilce[0].strip().strip("\n")
        ilce = il_ilce[1].strip().strip("\n")
        print(il)
        print(ilce)
    except:
        pass

    print("--------------------------------------------------------------------")

    adv_infos = {
        "URL":url,
        "Tel No":phone_number,
        "Ad Soyad":name,
        "İl":il,
        "İlçe":ilce
    }

    list_for_excel.append(adv_infos)
    
def scrapeUrls(w_url):
    website_url = w_url

    waiting_time = random.randint(3,7)
    browser.get(website_url)
    time.sleep(waiting_time)

    r = browser.page_source
    soup = BeautifulSoup(r, "lxml")

    urls = soup.find_all("a", attrs={"class":"classifiedTitle"})
    for i in urls:
        url = "https://www.sahibinden.com" + i.get("href")
        product_url_list.append(url)
        print(url)

    print(f"\n-----------------------------------\nToplam ürün linki: {len(product_url_list)}\n-----------------------------------\n")

try:
    scrapeUrls(w_url)
    counter = 1
    for url in product_url_list:
        print("\n----------------------------------------------------------")
        print(counter)
        scrapePhoneNumber(url)

        if(counter % 10 == 0):
            time.sleep(23)
        counter += 1

except:
    pass
finally:
    print("\n******************************************\nVeri çekme işlemi tamamlandı...\nÇekilen veriler Excel dosyasına dönüştürülüyor...")
    file_name = excel_file + ".xlsx"
    df = pd.DataFrame(list_for_excel)
    df.to_excel(file_name, index = False)
    print(f"\n******************************************\nVeriler {excel_file} adlı Excel dosyasına dönüştürüldü...\n******************************************\n")
    print("PROGRAM SONLANDI")

