from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import random

# FUNCTIONS

def createPageUrls(w_url, starting_page, ending_page):
    """Creates other page's urls from given url and append them into the list named website_url_list"""

    while(starting_page <= ending_page):
        website_url = w_url
        website_url = website_url + "&pagingOffset=" + str((starting_page - 1) * 50)
        website_url_list.append(website_url)
        starting_page += 1


def scrapeUrls(w_url):
    """Scrapes advertisement urls and append them into the list named product_url_list"""

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

    product_url_list.pop()
    product_url_list.pop()
    print(f"\n-----------------------------------\nToplam ürün linki: {len(product_url_list)}\n-----------------------------------\n")


def scrapeAdvInfo(url):
    """Goes to advertisement url and scrape name, surname, phone number and city information and append them into the list named list_for_excel"""

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


def saveAsExcelFile(excel_file, file_no):
    """Converts the list named list_for_excel to a DataFrame and then saves DataFrame as Excel file"""

    print("\n******************************************\nVeri çekme işlemi tamamlandı...\nÇekilen veriler Excel dosyasına dönüştürülüyor...")
    file_name = excel_file + str(file_no) + ".xlsx"
    df = pd.DataFrame(list_for_excel)
    df.to_excel(file_name, index = False)
    print(f"\n*********************************\nVeriler {file_name} adlı Excel dosyasına dönüştürüldü...\n*********************************\n")

    
website_url_list = list()
phone_number_list = list()

sleeping_time = int(input("Sayfalar arası kaç dakika beklesin: "))
sleeping_time *= 60 # saniyeye çevirdik

w_url = input("Veri çekilecek link: ")
excel_file = input("Kaydedilecek dosya adı: ")
starting_page = int(input("Başlangıç sayfası: "))
ending_page = int(input("Bitiş sayfası: "))

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36", 
    "X-Amzn-Trace-Id": "Root=1-6209086d-6b68c17b4f73e9d6174b5736"
}

createPageUrls(w_url, starting_page, ending_page)

file_no = 0
for w_url in website_url_list:
    try:
        browser = webdriver.Firefox()
        product_url_list = list()
        list_for_excel = list()

        scrapeUrls(w_url)

        print(f"\n---------------------------------------------------------\n{w_url}\n---------------------------------------------------------\n")

        counter = 1
        for url in product_url_list:
            print(f"------------\n{counter}")
            scrapeAdvInfo(url)
            counter += 1
        
        file_no += 1
    except:
        pass
    finally:
        saveAsExcelFile(excel_file, file_no)
        browser.quit()
        print("""
        ------------------------------------------------------------------------------------------
        - BELİRLEDİĞİNİZ SÜREDEN SONRA YENİ BİR TARAYICI AÇILACAK
        - DİĞER SAYFANIN VERİSİNİ ÇEKMEYE BAŞLAYACAK
        - BU CMD'Yİ KAPATMAYIN
        - PROGRAMI VERİ KAYBI YAŞAMADAN SONLANDIRMAK İÇİN CTRL C YAPABİLİRSİNİZ
        ------------------------------------------------------------------------------------------""")
        time.sleep(sleeping_time)
    
print("\n-----------------------\nPROGRAM SONLANDI\n-----------------------\n")