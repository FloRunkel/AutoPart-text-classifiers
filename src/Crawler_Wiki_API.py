from sentence_transformers import SentenceTransformer, util
import wikipediaapi 
import pandas as pd 

# In dieser Klasse werden die Unternehmensdaten aus den Wikipedia eintraegen extrahiert 
# Dabei wird Wikipedia-API verwendet

class Crawler_Wiki_API:
     
    def __init__(self, company_name, name_csv, example_sentences, label):
        self.company_name = company_name
        self.name_csv = name_csv
        self.example_sentences = example_sentences
        self.label = label
    
    # mittels dieser Methode koennen Unternehmen herausgelesen werden, die in dieser Branche (E-Commerce, Bankensektor oder auch im Cloud Bereich) taetig sind. 
    # dabei werden die Unternehmensbeschreibungen mittels des Wikipediaeintrages extrahiert und in Saetze unterteilt. 
    # Nachdem die Saetze unterteilt wurden, werden die einzelnen saetze auf aehnlichkeiten mit einem Beispielsatz geprueft. 
    # Sollte die aehnlichkeit des extrahierten Satzes mit dem Beispielssatz ueber 50% liegen, kann der Satz mit dem jeweiligen Label versehen werden. 
    # @Return: company_info_sentences, labels, Die extrahierten Saetz mit dem entsprechendem Label 
    
    def get_text_from_website(self):
        company_info_sentences=[]
        wiki_wiki = wikipediaapi.Wikipedia('de')
        page = wiki_wiki.page(self.company_name)
        
        if page.exists():
            for sentence in page.summary.split('.'): 
                if len(sentence)>10: 
                    company_info_sentences.append(sentence.replace('\n', ''))
        else:
            print('Zu dieser Firma: ' + self.company_name + ' gibt es keinen Wikipediaartikel ' )

        return company_info_sentences
    
    # Mittels einiger Schluesselwoerter wird eine erste Annotation der Saetze durchgefuehrt
    # @Return: eine Liste der Eingabesequenzen und eine Liste der zugehoerigen Zielvariablen 
    
    def get_labels_for_each_sentence(self): 
        company_info_sentences = self.get_text_from_website()
        labels_list=[]

        model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')
        embeddings1 = model.encode(self.example_sentences, convert_to_tensor=True)
        embeddings2 = model.encode(company_info_sentences, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embeddings1, embeddings2) # type: ignore

        for j in range(len(cosine_scores)):
            for i in range(len(company_info_sentences)):
                if cosine_scores[j][i] > 0.5: 
                    labels_list.append(self.label)
                else: 
                    labels_list.append('Sonstiges')

        count = 0 
        for label in labels_list: 
            if label == 'Sonstiges': 
                count=+1
        
        if count == len(labels_list): 
            print('Nach der Firmenbeschreibung, ist die Firma: ' + self.company_name + ' nicht in der Branche taetig')

        return company_info_sentences, labels_list
    
    # Das erstellte DataFrame, mit Eingabesequenzen und einer zugehörigen Zielvariable, werden in die angegbenen CSV-Datei geschrieben 

    def write_into_csv(self): 
        data_content, data_labels = self.get_labels_for_each_sentence()
        dict = {'Beschriftung': data_labels, 'Eingabesequenz': data_content} 
        pd.DataFrame(dict).to_csv(self.name_csv, index=False, sep = ';', encoding='utf-8', header=False, mode='a')
    
