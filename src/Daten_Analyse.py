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

    # Mittels dieser Methode, kann Auskunft über die durchschnittlichen Satzlaengen geben
    # Hiebei wird ein Balkendiagramm erstellt, welches die durchschnittliche Satzlaenge pro Kategorie darstellt
    
    def satzlaenge_Data_plot(self):
        label = ["Softwareentwicklung im E-Commerce", "Softwareentwicklung im Bankensektor", "Softwareentwicklung für Cloud-Lösungen", "Sonstiges"]
        durchschnittsatzlaenge = []

        satz_laengen_sonstiges = [len(value) for key, value in self.read_csv_Datei().items() if value == "Sonstiges"]
        durchschnitt_sonstiges = sum(satz_laengen_sonstiges) / len(satz_laengen_sonstiges)
        durchschnittsatzlaenge.append(durchschnitt_sonstiges)
        
        satz_laengen_ecommerce = [len(value) for key, value in self.read_csv_Datei().items() if value == "Softwareentwicklung im E-Commerce"]
        durchschnitt_ecommerce = sum(satz_laengen_ecommerce) / len(satz_laengen_ecommerce)
        durchschnittsatzlaenge.append(durchschnitt_ecommerce)

        satz_laengen_bank = [len(value) for key, value in self.read_csv_Datei().items() if value == "Softwareentwicklung im Bankensektor"]
        durchschnitt_bank = sum(satz_laengen_bank) / len(satz_laengen_bank)
        durchschnittsatzlaenge.append(durchschnitt_bank)

        satz_laengen_cloud = [len(value) for key, value in self.read_csv_Datei().items() if value == "Softwareentwicklung für Cloud-Lösungen"]
        durchschnitt_cloud = sum(satz_laengen_cloud) / len(satz_laengen_cloud)
        durchschnittsatzlaenge.append(durchschnitt_cloud)

        plt.xticks(rotation=90, fontsize=14)
        plt.title("Durchschnittliche Satzlänge pro Kategorie", fontsize=20, fontweight="bold")
        plt.xlabel('Klassenbezeichnung', fontsize=16, fontweight="bold")
        plt.ylabel('Durchschnittliche Satzlängez', fontsize=16, fontweight="bold")
        plt.bar(label, durchschnittsatzlaenge)
        plt.show(block=True)

    # Mittels dieser Methode, kann Auskunft über die dhaufigkeit von Woerten innerhalb einer Klase geben 
    # Hiebei wird ein Balkendiagramm erstellt, welches die haufigkeit der Woerter pro Kategorie darstellt

    def woerterHaeufigkeit(self): 
        woerter_haeufigkeiten_sonstiges, woerter_haeufigkeiten_ec, woerter_haeufigkeiten_bank, woerter_haeufigkeiten_cloud= Counter(), Counter(), Counter(), Counter()

        for key, value in self.read_csv_Datei().items():
            if value == "Sonstiges":
                woerter = key.split()
                woerter_haeufigkeiten_sonstiges.update(woerter)
                
            if value == "Softwareentwicklung im E-Commerce": 
                woerter = key.split()
                woerter_haeufigkeiten_ec.update(woerter)

            if value == "Softwareentwicklung im Bankensektor": 
                woerter = key.split()
                woerter_haeufigkeiten_bank.update(woerter)

            if value == "Softwareentwicklung für Cloud-Lösungen": 
                woerter = key.split()
                woerter_haeufigkeiten_cloud.update(woerter)
        
        dict = {
            "Sonstiges": woerter_haeufigkeiten_sonstiges.most_common(15),
            "Softwareentwicklung im E-Commerce":woerter_haeufigkeiten_ec.most_common(15),
            "Softwareentwicklung im Bankensektor": woerter_haeufigkeiten_bank.most_common(15),
            "Softwareentwicklung für Cloud-Lösungen": woerter_haeufigkeiten_cloud.most_common(15)
        }

        for category, word_freq in dict.items():
            words, frequencies = zip(*word_freq) 
            plt.figure()
            plt.bar(words, frequencies)
            plt.xlabel("Wörter")
            plt.ylabel("Häufigkeiten")
            plt.title(f"Häufigkeiten der Top 5 Wörter - {category}")
            plt.xticks(rotation=45)
            plt.show()
