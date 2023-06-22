from sentence_transformers import SentenceTransformer, util
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd 
import urllib3

urllib3.disable_warnings()

# In dieser Klasse werden die Daten aus der Webseite: Indeed extrahiert und in eine CSV-Datei geschreiben
# Dabei wird Selenium und BeautifulSoup verwendet

class Crawler_Indeed():

    # @Parameter: url; Gibt die URL, der zu extrahierenden Webseite an
    # @Paramter: name_csv; Gibt an, unter welchem Namen die CSV-Datei gespeichert werden soll 

    def __init__(self, url,  name_csv, example_sentences, label ):
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
        data_content, data_labels = self.get_labels_for_each_sentence()
        dict = {'Beschriftung': data_labels, 'Eingabesequenz': data_content} 
        pd.DataFrame(dict).drop_duplicates(keep='first').to_csv(self.name_csv, index=False, sep = ';', encoding='utf-8', header=False, mode='a')
    
    # Mittels einiger Schluesselwoerter wird eine erste Annotation der Saetze durchgefuehrt
    # @Return: eine Liste der Eingabesequenzen und eine Liste der zugehoerigen Zielvariablen 

    def get_labels_for_each_sentence(self): 
        company_info_sentences = self.extract_Data()
        label_list=[]
        
        model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')
        embeddings1 = model.encode(self.example_sentences, convert_to_tensor=True)
        embeddings2 = model.encode(company_info_sentences, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embeddings1, embeddings2) # type: ignore

        for j in range(len(cosine_scores)):
            for i in range(len(company_info_sentences)):
                if cosine_scores[j][i] > 0.5: 
                    label_list.append(self.label)
                else: 
                    label_list.append('Sonstiges')

        count = 0 
        for label in label_list: 
            if label == 'Sonstiges': 
                count=+1
        
        if count == len(label_list): 
            print('Nach der Firmenbeschreibung, ist die Firma: nicht in der Branche taetig')

        return company_info_sentences, label_list
