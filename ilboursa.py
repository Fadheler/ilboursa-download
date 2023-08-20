from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from datetime import datetime
import os
import time
from dateutil.relativedelta import relativedelta
import pandas as pd

def quotes(ticker, start_date, end_date=datetime.strftime(datetime.now(), "%d/%m/%Y"), path=False):
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")
    if end_date < start_date:
        print("End date < Start date")
        return False
    
    #Create a new folder
    dirname = ticker + " - " + start_date.strftime("%d-%m-%Y") + " - " + end_date.strftime("%d-%m-%Y")
    #if argument specified
    if path != False:
        dirname = path

    if os.path.exists(dirname):
        for f in os.listdir(dirname):
            if not f.endswith(".csv"):
                continue
            os.remove(os.path.join(dirname, f))
    else:
        os.mkdir(dirname)
    dirname = "/"+dirname+"/"
    #Correction for windows filepaths
    if os.name == "nt":
        dirname = dirname.replace("/", "\\")

    print("Download path:", dirname)
    #Launch browser and navigate to ilboursa download page
    options = webdriver.ChromeOptions()
    prefs = {
    "download.default_directory" : os.path.dirname(os.path.realpath(__file__))+dirname,
    "savefile.default_directory" : os.path.dirname(os.path.realpath(__file__))+dirname,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
    }
    print("Chromedriver options:", prefs)
    options.add_experimental_option("prefs",prefs);
    driver = webdriver.Chrome(options = options)
    driver.get("https://www.ilboursa.com/marches/download/"+ticker)


    #Send requests and download files
    current_start = start_date
    i = 0
    while True:
        if current_start+relativedelta(days=+90) < end_date:
            current_stop = current_start + relativedelta(days=+90)
        else:
            current_stop = end_date
        #Dirty fix
        if current_start > current_stop or current_start >= datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d"):
            break
        i += 1
        print("Current dates: "+current_start.strftime("%Y-%m-%d")+" - "+current_stop.strftime("%Y-%m-%d"))
        button = driver.find_element(By.XPATH, "//button[contains(@class, 'btnR')]")
        driver.execute_script("document.getElementById('dtFrom').setAttribute('value', '"+current_start.strftime("%Y-%m-%d")+"');")
        driver.execute_script("document.getElementById('dtTo').setAttribute('value', '"+current_stop.strftime("%Y-%m-%d")+"');")
        button.click()
        time.sleep(1)
        #Wait for file to appear in folder:
        while os.path.exists(dirname[1:]+"cotations_"+ticker+".csv") == False:
            print("Waiting for CSV file download")
            if 'La limite est de 3 mois' in driver.find_element(By.XPATH, "//body").text or 'Pas de données' in driver.find_element(By.XPATH, "//body").text:
                current_stop = current_stop+relativedelta(days=-1)
                if current_start < current_stop:
                    print("Corrected dates: "+current_start.strftime("%Y-%m-%d")+" - "+current_stop.strftime("%Y-%m-%d"))
                    button = driver.find_element(By.XPATH, "//button[contains(@class, 'btnR')]")
                    driver.execute_script("document.getElementById('dtFrom').setAttribute('value', '"+current_start.strftime("%Y-%m-%d")+"');")
                    driver.execute_script("document.getElementById('dtTo').setAttribute('value', '"+current_stop.strftime("%Y-%m-%d")+"');")
                    button.click()
                else:
                    pd.DataFrame().to_csv(dirname[1:]+"cotations_"+ticker+".csv")
            time.sleep(1)
        time.sleep(1)
        #Rename generated file
        os.rename(dirname[1:]+"cotations_"+ticker+".csv", dirname[1:]+"cotations_"+ticker+"_"+str(i)+".csv")
        
        if current_stop < end_date:
            current_start = current_stop+relativedelta(days=+1)
        else:
            break

    CSVs = pd.DataFrame(columns=['symbole','date','ouverture','haut','bas','cloture','volume'])
    CSVs = pd.concat([pd.read_csv(dirname[1:]+"cotations_"+ticker+"_"+str(idx+1)+".csv", delimiter=";") for idx in range(i) ], ignore_index=True)
    CSVs.to_csv(dirname[1:]+"cotations_"+ticker+".csv", index=False)
