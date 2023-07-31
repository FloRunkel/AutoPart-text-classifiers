from sklearn.model_selection import train_test_split
import random
import csv
from Data import Data 

# Datenvorberitung für die Machine Learning Methoden: Zero-Shot und Few-Shot 

class Daten_for_Shot_Versions(Data):

    # @Parameter: name_csv_Datai; Namens der jewiligen einzulesenden CSV-Datei 

    def __init__(self, name_csv_Datai):
        self.name_csv_Datai = name_csv_Datai
        
    # Diese Methode dient dem lesen der CSV_Datei
    # Die gespeicherten Daten aus der CSV-Datei werden in einem Dictionary gespeichert
    # @Return: Daten aus der CSV-Datei in einem Dictionary

    def read_csv_Datei(self):
        labeled_texts = {}
        with open(self.name_csv_Datai, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                text = row[0]
                label = row[1]
                labeled_texts[label] = text
                
        return labeled_texts
    
    # Diese Methode dient dem zufälligen mischen der Eingabesequenzen und der zugehoerigen Zielvariablen
    # @Return: zip der gemischten Daten im Dictionary

    def shuffleData(self, texts, labels):
        zipped = list(zip(texts, labels))
        random.shuffle(zipped)
        
        return zip(*zipped)
    
    # In dieser Methode werden die gemischten Daten aus dem Dictionary in Trainings und Testdaten unterteilt. 
    # @Return: Trainings- und Testdaten 

    def split_in_Train_Test_data(self): 
        texts, labels = self.shuffleData(self.read_csv_Datei().keys(), self.read_csv_Datei().values())
        train_texts, test_texts, train_labels, test_labels = train_test_split(texts, labels, test_size=0.3)
        return train_texts, test_texts, train_labels, test_labels