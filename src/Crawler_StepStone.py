from bs4 import BeautifulSoup
from time import sleep as pause
import pandas as pd
import requests
import urllib3
import os

from Crawler import Crawler

urllib3.disable_warnings()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# In dieser Klasse werden die Daten aus der Webseite: StepStone extrahiert und in eine CSV-Datei geschreiben
# Dabei wird BeautifulSoup verwendet

class Crawler_StepStone(Crawler):

    # @Parameter: url; gibt die URL, der zu extrahierenden Webseite an
    # @Paramter: name_csv; gibt an, unter welchem Namen die CSV-Datei gespeichert werden soll 
    # @Paramter: number_of_Pages; gibt an, wie viele Seiten der StepStone Webseiten gecrawlt werden sollen.

    def __init__(self, url,  name_csv, number_of_Pages, example_sentences, label):
        self.url = url
        self.name_csv = name_csv
        self.number_of_Pages = number_of_Pages
        self.example_sentences = example_sentences
        self.label = label

    # getter Methode für den Header der StepStone Webseite
    # @Return: Gibt den zu uebergebenen Header an die jeweilige Webseite wieder.

    def get_Header(self): 
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                   "User-Agent": "Mozilla/5.0"}
        return headers
    
    # Erstellt ein Anfrage an eine Webseite und den BeautifulSoup
    # @Return: gibt die Webseite mittels BeautifulSoup wieder

    def make_soup(self):
        page = requests.get(self.url, headers = self.get_Header(), verify=True)
        
        if page.status_code != 200: 
            print(page.status_code)

        return BeautifulSoup(page.content, "html.parser")
    
    # Dies ist eine Helper Methode die den Webseitenkontext ausließt 
    # Dabei ist es enscheident, wie viele Seiten der Webseite gecrawlt werden sollen
    # @Return: die gecrawlten Daten werden in Form einer Liste wiedergegeben

    def extract_Data(self): 
        pause(2)
        soup = self.make_soup()
        data_content = []
        company_context = str     
        for result in soup.find_all('article', attrs={'data-at': 'job-item'}):
            for content in result.find_all('div', attrs={'data-at': 'jobcard-content'}):
                company_context = content.find('span').get_text().strip()

            if '*' in company_context and not 'innen' in company_context and not 'Programmierer*in' in company_context and '. ' in company_context: # type: ignore
                data_content = data_content + company_context.split("*")
        return data_content
  
    # Erstellen eines DataFrames mit dem Webseitenkontext und einer zugehoerigen Zielvariabel 
    # Duplikate werden aufgrund von ueberscheidenen Jobangeboten geloescht
    # @Parameter: data_content; Wiedergabe des Websietenkontextes in Sätzen.
    # @Parameter: data_labels; Die Labels für einen Satz aus der Webseite
    # @Return: DataFrame mit einem Label und einem Satz aus dem Webseitenkontext 

    def create_DataFrame(self, data_content, data_labels): 
        dict = {'Beschriftung': data_labels, 'Eingabesequenz': data_content} 
        return pd.DataFrame(dict).drop_duplicates(keep='first')
    
    # Das erstellte DataFrame wird in eine CSV-Datei geschrieben. 

    def write_into_csv(self): 
        company_info_sentences = self.extract_Data()
        data_content, data_labels = self.get_labels_for_each_sentence(company_info_sentences,self.label,self.example_sentences)
        self.create_DataFrame(data_content, data_labels).to_csv(self.name_csv, index=False, sep = ';', encoding='utf-8', header=False, mode='a')