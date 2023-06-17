from Data import Data
import matplotlib.pyplot as plt
import csv 
from collections import Counter

# Diese Klasse dient der Anylse der Daten, was zum Verstaendins des outputs der jeweiligen Machine Learning Methode beitragen kann

class Daten_Analyse(Data):

    # @Paramter: name_csv_Datai; Name der zu analysierenden CSV-Datei
    
    def __init__(self, name_csv_Datai):
        self.name_csv_Datai = name_csv_Datai
    
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
    
    # Diese Methode wird hier nicht verwendet, da keine Aufteilung der Daten in Trainings- und Testdaten von noeten ist

    def split_in_Train_Test_data(self): 
        pass

    # Mittels dieser Methode, kann Auskunft über die Anzahl der gelabelten Eingabesequenzen geben werden 
    # Hiebei wird ein Balkendiagramm dargestellt, welches die reine Anzhal der Labels veranschaulicht

    def verteilung_Data_plot(self):
        labeled_texts = self.read_csv_Datei()
        plot_labeled_texts = Counter(labeled_texts.values())

        plt.xticks(rotation=90, fontsize=14)
        plt.title("Anzahl Eingabesequenzen in den Klassen", fontsize=20, fontweight="bold")
        plt.xlabel('Klassenbezeichnung', fontsize=16, fontweight="bold")
        plt.ylabel('Anzahl im Datensatz', fontsize=16, fontweight="bold")
        plt.bar(list(plot_labeled_texts.keys()) ,list(plot_labeled_texts.values()))
        plt.show(block=True)