from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd 
import urllib3
from Crawler import Crawler

urllib3.disable_warnings()

# In dieser Klasse werden die Daten aus der Webseite: Indeed extrahiert und in eine CSV-Datei geschreiben
# Dabei wird Selenium und BeautifulSoup verwendet

class Crawler_Indeed(Crawler):

    # @Parameter: url; Gibt die URL, der zu extrahierenden Webseite an
    # @Paramter: name_csv; Gibt an, unter welchem Namen die CSV-Datei gespeichert werden soll 

    def __init__(self, url,  name_csv, example_sentences, label):
        self.url = url
        self.name_csv = name_csv
        self.example_sentences = example_sentences
        self.label = label

    # In dieser Function werden die Daten aus der Indeed Webseite ausgelesen 
    # Die extrahierten Saetze über die jeweiligen Unternehmen die ausgelesen wurden, werden in einer CSV-Datei gespeichert
    # @Return: eine Liste der extrahierten Jobbeschreibungen 

    def extract_Data(self):
        options = Options()    
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        data_list=[]

        for i in range(0,50,10):
            driver.get(self.url+str(i))
            driver.implicitly_wait(20)
            
            for job in driver.find_elements(By.CLASS_NAME, "job-snippet"):
                soup = BeautifulSoup(job.get_attribute('innerHTML'),'html.parser')   
                try:
                     description = soup.find("li").text.replace("\n","").strip() # type: ignore
                except:
                    description = 'None'  
                data_list.append(description)

        driver.close()
        return data_list
     
 
    # Das erstellte DataFrame, mit Eingabesequenzen und einer zugehörigen Zielvariable, werden in der angegbenen CSV-Datei geschrieben 

    def write_into_csv(self): 
        company_info_sentences = self.extract_Data()
        data_content, data_labels = self.get_labels_for_each_sentence(company_info_sentences,self.label,self.example_sentences)
        dict = {'Beschriftung': data_labels, 'Eingabesequenz': data_content} 
        pd.DataFrame(dict).drop_duplicates(keep='first').to_csv(self.name_csv, index=False, sep = ';', encoding='utf-8', header=False, mode='a')