from bs4 import BeautifulSoup
from time import sleep as pause
import pandas as pd
import requests
import urllib3

urllib3.disable_warnings()

# In dieser Klasse werden die Daten aus der Webseite: StepStone extrahiert und in eine CSV-Datei geschreiben
# Dabei wird BeautifulSoup verwendet

class Crawler_StepStone:

    # @Parameter: url; gibt die URL, der zu extrahierenden Webseite an
    # @Paramter: name_csv; gibt an, unter welchem Namen die CSV-Datei gespeichert werden soll 
    # @Paramter: number_of_Pages; gibt an, wie viele Seiten der StepStone Webseiten gecrawlt werden sollen.

    def __init__(self, url,  name_csv, number_of_Pages):
        self.url = url
        self.name_csv = name_csv
        self.number_of_Pages = number_of_Pages

    # getter Methode für die URL der StepStone Webseite
    # @Return: gibt die URL der Webseite wieder

    def get_url(self): 
        return self.url

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
        page = requests.get(self.url, headers = self.get_Header(), verify=False)
        return BeautifulSoup(page.content, "html.parser")
    
    # In dieser Methode werden die Daten aus den einzelnen Stellenangeboten ausgelesen und gespeichert 
    # @Return: gibt die einzelnen Saetze der Stellenangebote wieder

    def get_text_from_website(self):
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
        data_content, data_labels = self.get_labels_for_each_sentence()
        self.create_DataFrame(data_content, data_labels).to_csv(self.name_csv, index=False, sep = ';', encoding='utf-8', header=False, mode='a')
    
    # Mittels einiger Schluesselwoerter wird eine erste Annotation der Saetze durchgefuehrt
    # @Return: eine Liste der Eingabesequenzen und eine Liste der zugehoerigen Zielvariablen 

    def get_labels_for_each_sentence(self): 
        data_list = self.extract_Data()
        label_list=[]
        for sentence in range(0,len(data_list)):
            if "e-commerce" in self.url and ("Webentwicklung" in data_list[sentence] or "E-Commerce" in data_list[sentence]):
                label_list.append("Softwareentwicklung im E-Commerce")
            elif "bank" in self.url and ("Banken" in data_list[sentence] or "bank" in data_list[sentence]):
                label_list.append("Softwareentwicklung im Bankensektor")
            elif "Cloud" in self.url and ("Cloud" in data_list[sentence] or "cloud" in data_list[sentence]):
                label_list.append("Softwareentwicklung für Cloud-Lösungen")
            else:
                label_list.append("Sonstiges")
            
        return data_list, label_list
    
    # Dies ist eine Helper Methode die den Webseitenkontext ausließt 
    # Dabei ist es enscheident, wie viele Seiten der Webseite gecrawlt werden sollen
    # @Return: die gecrawlten Daten werden in Form einer Liste wiedergegeben

    def extract_Data(self): 
        list_Data_content = []
        for page in range(1,self.number_of_Pages):
            pause(2)
            #print("2 sec Pause bis zur nächsten Abfrage")
            self.get_url()
            list_Data_content += self.get_text_from_website()
        return list_Data_content