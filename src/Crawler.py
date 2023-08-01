from abc import ABC, abstractmethod
from sentence_transformers import SentenceTransformer, util

# Dies ist eine Abstrakte-Klasse, die die benötigten Methoden der Crawler definiert und in der die Annotationen der Eingabesequenzen erfolgt
# @abstractmethod: werden die Webseiteninhalte aus den Webseiten extrahiert 
# @abstractmethod: wereden die extrahierten Webseiteninhalte aus den Webseiten in eine csv Datei geschrieben 

class Crawler(ABC):

    # Mittels einiger Schluesselwoerter wird eine erste Annotation der Saetze durchgefuehrt
    # @Return: eine Liste der Eingabesequenzen und eine Liste der zugehoerigen Zielvariablen 

    def get_labels_for_each_sentence(self,company_info_sentences,label,example_sentences): 

        label_list=[]
        
        model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')
        embeddings1 = model.encode(example_sentences, convert_to_tensor=True)
        embeddings2 = model.encode(company_info_sentences, convert_to_tensor=True)
        cosine_scores = util.cos_sim(embeddings1, embeddings2) # type: ignore

        for j in range(len(cosine_scores)):
            for i in range(len(company_info_sentences)):
                if cosine_scores[j][i] > 0.5: 
                    label_list.append(label)
                else: 
                    label_list.append('Sonstiges')

        count = 0 
        for label in label_list: 
            if label == 'Sonstiges': 
                count=+1
        
        if count == len(label_list): 
            print('Nach der Firmenbeschreibung, ist die Firma: nicht in der Branche taetig')

        return company_info_sentences, label_list
    

    # Abstracte Methoden, in der die Webseiteninhalte aus den Webseiten extrahiert werden
    @abstractmethod
    def extract_Data(self):
        pass
    
    # Abstracte Methoden, in der die extrahierten Webseiteninhalte aus den Webseiten in eine csv Datei geschrieben werden 
    @abstractmethod
    def write_into_csv(self): 
        pass

        