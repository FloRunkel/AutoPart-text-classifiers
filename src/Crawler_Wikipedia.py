import wikipediaapi 
import pandas as pd 

from Crawler import Crawler

# In dieser Klasse werden die Unternehmensdaten aus den Wikipedia eintraegen extrahiert 
# Dabei wird Wikipedia-API verwendet

class Crawler_Wikipedia(Crawler):
     
    def __init__(self, company_name, name_csv, example_sentences, label):
        self.company_name = company_name
        self.name_csv = name_csv
        self.example_sentences = example_sentences
        self.label = label
        super().__init__()
    
    # mittels dieser Methode koennen Unternehmen herausgelesen werden, die in dieser Branche (E-Commerce, Bankensektor oder auch im Cloud Bereich) taetig sind. 
    # dabei werden die Unternehmensbeschreibungen mittels des Wikipediaeintrages extrahiert und in Saetze unterteilt. 
    # Nachdem die Saetze unterteilt wurden, werden die einzelnen saetze auf aehnlichkeiten mit einem Beispielsatz geprueft. 
    # Sollte die aehnlichkeit des extrahierten Satzes mit dem Beispielssatz ueber 50% liegen, kann der Satz mit dem jeweiligen Label versehen werden. 
    # @Return: company_info_sentences, labels, Die extrahierten Saetz mit dem entsprechendem Label 
    
    def extract_Data(self):
        company_info_sentences=[]
        wiki_wiki = wikipediaapi.Wikipedia('de')
        page = wiki_wiki.page(self.company_name)
        
        if page.exists():
            for sentence in page.text.split('.'): 
                if len(sentence)>10: 
                    company_info_sentences.append(sentence.replace('\n', ''))
        else:
            print('Zu dieser Firma: ' + self.company_name + ' gibt es keinen Wikipediaartikel ' )

        return company_info_sentences
    
    # Das erstellte DataFrame, mit Eingabesequenzen und einer zugehörigen Zielvariable, werden in die angegbenen CSV-Datei geschrieben 

    def write_into_csv(self): 
        company_info_sentences = self.extract_Data()
        data_content, data_labels = self.get_labels_for_each_sentence(company_info_sentences,self.label,self.example_sentences)
        dict = {'Beschriftung': data_labels, 'Eingabesequenz': data_content} 
        pd.DataFrame(dict).to_csv(self.name_csv, index=False, sep = ';', encoding='utf-8', header=False, mode='a')