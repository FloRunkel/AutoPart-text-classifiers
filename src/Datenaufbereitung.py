from Data import Data
from spacy.lang.de.stop_words import STOP_WORDS
import csv
import string
import re
import spacy


# Datenaufbereitung für die Machine Learning Methoden

class Datenaufbereitung(Data):

    # @Parameter: name_csv_Datai; Name der CSV-Datei die für die Machine-Learning Modelle aufberietet werden soll 

    def __init__(self, name_csv_Datai):
        self.name_csv_Datai = name_csv_Datai
        self.nlp = spacy.load('de_core_news_md')
        self.stop_words = STOP_WORDS

    # einlesen der CSV-Datei die vorverarbeitet werden soll

    def read_csv_Datei(self):
        labeled_texts = {}
        with open(self.name_csv_Datai, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                text = row[0]
                label = row[1]
                labeled_texts[label] = text
        return labeled_texts
    
    def split_in_Train_Test_data(self):
        pass

    # entfernen der Satzzeichen 
    # @Parameter: in_string; Der Satz in der CSV Datei, wo die Satzzeichen entfernt werden sollen 

    def remove_punctuation(self, in_string: str):
        out_string = in_string.translate(str.maketrans('', '', string.punctuation))
        out_string = ' '.join(out_string.split())
        return out_string
    
    # alles zu kleinen Buchstaben 
    # @Parameter: in_string; Der Satz in der CSV Datei, der in lowercase geschrieben werden soll 

    def to_lower(self, in_string: str):
        out_string = in_string.lower()
        return out_string
    
    # entfernen der zahlen, da sie keine Beduetung für die Klassifizierung aufweisen 
    # @Parameter: in_string; Der Satz in der CSV Datei, in dem die Zahlen entfernt weden sollen 

    def remove_numbers(self, in_string: str):
        pattern = r'[0-9]'
        sentence_no_numbers = " ".join((re.sub(pattern, "", in_string)).split()) 
        sentence_no_numbers = ' '.join(sentence_no_numbers.split())
        return sentence_no_numbers
    
    # alle umlaute umschreiben 
    # @Parameter: in_string; Der Satz in der CSV Datei, in dem die Umlaute umgeschrieben weden sollen 

    def replace_special_letters(self, in_string: str):
        replacements_dic = {
            "ä": "ae",
            "ö": "oe",
            "ü": "ue",
            "ß": "ss"
        }
        rc = re.compile('|'.join(map(re.escape, replacements_dic)))

        def translate(match):
            return replacements_dic[match.group(0)]

        out_string = rc.sub(translate, in_string)
        return out_string
    
    # Woerter in einem Satz in Ihre Grundform bringen wie sie auch im Woerterbuch stehen 
    # @Parameter: in_string; Der Satz in der CSV Datei, in dem die Woerter in ihre Grundform gebracht werden sollen 

    def lemmatize(self, in_string: str):
        doc = self.nlp(in_string)
        lemmatized_tokens = [token.lemma_ for token in doc]
        lemmatized_text = ' '.join(lemmatized_tokens)
        return lemmatized_text 

    # alle stopwoerter die nicht relevant sind aus den saetzen entfernen 

    def remove_stop_words(self, in_string: str):
        doc = self.nlp(in_string)
        filtered_tokens = [token.text for token in doc if token.text.lower() not in self.stop_words]
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text

    # aufruf der oben definierten methoden 
    # Die umgeformten Daten in eine csv Datei einfuegen 

    def datenvorverarbeitung(self):
        dict_aufbereitet = []
        data_dict = self.read_csv_Datei()

        for text, label in data_dict.items():
            if len(text) > 10:
                processed_text = self.remove_punctuation(text)
                processed_text = self.to_lower(processed_text)
                processed_text = self.remove_numbers(processed_text)
                processed_text = self.replace_special_letters(processed_text)
                processed_text = self.lemmatize(processed_text)
                processed_text = self.remove_stop_words(processed_text)
                dict_aufbereitet.append({'Beschriftung': label, 'Eingabesequenz': processed_text})

        with open('/Users/florunkel/01_Flo/02_Uni/Wirtschaftsinformatik/08_Semester/Bachelorarbeit/Autopart/src/Crawling_Data/Data_Aufbereitet.csv', 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Beschriftung', 'Eingabesequenz']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(dict_aufbereitet)