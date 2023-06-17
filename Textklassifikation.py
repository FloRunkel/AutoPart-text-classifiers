from ZeroShot import ZeroShot
from FewShot import FewShot
from ClassicTextclassfikation import ClassicTextclassfikation
from Daten_for_Shot_Versions import Daten_for_Shot_Versions 
from Daten_for_Classic_Version import Daten_for_Classic_Version
from Combine_Crawler_Data import Combine_Crawler_Data
from Crawler_StepStone import Crawler_StepStone
from Daten_Analyse import Daten_Analyse
from Crawler_Indeed import Crawler_Indeed

import random
import pandas as pd 

# In dieser Klasse werden alle benötigten Daten, Machine Learning Methode und Crawler aufgerufen und ausgefuehrt 

class Textklassifikation:

    # Ruft die Crawler Indeed Klasse auf mit der Webseite, aus welcher der Inhalt extrahiert werden soll.
    # Desweiteren wird der Crawlerklasse der Name der zu erstellenden CSV-Datei uebergeben. 

    def run_Crawler_Indeed(self,  pfad, list_titel, list_csv_Name): 
        for number_titel in range(len(list_titel)): 
            Crawler_Indeed(f'https://de.indeed.com/jobs?q={list_titel[number_titel]}&l=Deutschland&from=searchOnHP&vjk=b03e724b97697e90&page=', pfad + list_csv_Name[number_titel]).write_into_csv()

    # Ruft die Crawler Stepstone Klasse auf mit der Webseite, aus welcher der Inhalt extrahiert werden soll.
    # Desweiteren wird der Crawlerklasse der Name der zu erstellenden CSV-Datei uebergeben. 

    def run_Crawler_StepStone(self, number_of_Pages, pfad, list_titel, list_csv_Name):
        page=int
        for number_titel in range(len(list_titel)): 
            Crawler_StepStone(f'https://www.stepstone.de/jobs/{list_titel[number_titel]}/in-deutschland?radius=30&page={page}&wci=300000115.html', pfad + list_csv_Name[number_titel], number_of_Pages).write_into_csv()

    # Zusammenfuegen der gecrawlten Daten in eine CSV Datei 

    def run_Combine_Crawler_Data(self, pfad, list_csv_Name):
        Combine_Crawler_Data().get_Data_together(pfad, pfad + '/Results_Crawling.csv', list_csv_Name)

    # In dieser Methode wird die Daten_for_Shot_Versions Klasse aufgerufen, in der die Daten für die Shot Learning Methoden vorberitet werden. 
    # Die Methode wird zudem anschließend in der run_ZeroShot und run_FewShot Methode verwendet, um die Daten aus der CSV-Datei in einem Dictionary zu uebergeben.

    def get_Data_for_Shot_Versions(self):
        return Daten_for_Shot_Versions('/Users/florunkel/01_Flo/02_Uni/Wirtschaftsinformatik/08_Semester/Bachelorarbeit/Autopart/src/Crawling_Data/Data.csv').split_in_Train_Test_data()
   
    # In dieser Methode wird die Daten_for_Classic_Version Klasse aufgerufen, in der die Daten für die klassischen Learn Methoden vorberitet werden. 
    # Die Methode wird zudem anschließend in der run_ClassicTextklassification run Methode verwendet, um die Daten aus der CSV-Datei in einem DataFrame zu uebergeben.

    def get_Data_for_Classic_Version(self):
        return Daten_for_Classic_Version('/Users/florunkel//01_Flo/02_Uni/Wirtschaftsinformatik/08_Semester/Bachelorarbeit/Autopart/src/Crawling_Data/Data.csv').split_in_Train_Test_data()
    
    # Diese Methode dient dazu, die erlangten Daten aus den Webseiten mittels Graphiken zu Analysieren. 
    # Mittels der verteilung_Data_plot Methode kamm die Verteilung der einzelnen Kategorien in der CSV-Datei genauer betrachtet werden und Ausschlüsse über die Qualität der Daten geben. 

    def run_Data_Analyse(self):
        Daten_Analyse('/Users/florunkel/01_Flo/02_Uni/Wirtschaftsinformatik/08_Semester/Bachelorarbeit/Autopart/src/Crawling_Data/Data.csv').verteilung_Data_plot()
    
    # In dieser Methode wird die Machine Learning Methode Zero Shot angewendet.
    # Dabei werden die Daten mittels des Dictionarys aus der get_Data_for_Shot_Versions Methode übergeben und anschließend trainiert.

    def run_ZeroShot(self, models, boolean_multiLabel):
        train_texts, test_texts, train_labels, test_labels = self.get_Data_for_Shot_Versions()
            
        for model in models: 
            print(f"Training mit Modell: '{model}' ")
            number_train_sentence_in_csv = random.randint(0, len(train_texts)-1)
            sentence = train_texts[number_train_sentence_in_csv] 
            label = train_labels[number_train_sentence_in_csv]

            zs = ZeroShot(model, sentence, label, boolean_multiLabel)
            zs.evaluate(zs.train())  
            #zs.prediction(zs.train()) 
            

    # In dieser Methode wird die Machine Learning Methode Few Shot angewendet.
    # Dabei werden die Daten mittels des Dictionarys aus der get_Data_for_Shot_Versions Methode uebergeben.

    def run_FewShot(self, models, lrs, epochs, boolean_multiLabel):
        train_texts, test_texts, train_labels, test_labels = self.get_Data_for_Shot_Versions()

        for model in models: 
            for learning_rate in lrs:  
                model_beschreibung = f"Few-Shot mit Modell: '{model}', einer Lernrate von '{learning_rate}' und einer Epochen-Anzahl von {epochs}"
                print(model_beschreibung)
                
                fs = FewShot(model, learning_rate, epochs, boolean_multiLabel)
                corpus_fs = fs.create_Corpus(train_texts, train_labels, test_texts, test_labels)
                fs.train(corpus_fs)
                f1_micro, f1_macro, mcc = fs.evaluate(test_texts, test_labels)
                self.generate_Report(model_beschreibung, f1_micro, f1_macro, mcc)
                #fs.prediction('Suchen einen Softwareentwickler für E-Commerce Anwendungen')

    # In dieser Methode wird die Machine Learning Methode SimpleTransformers angewendet.
    # Dabei werden die Daten mittels des DataFrames aus der get_Data_for_Classic_Version Methode uebergeben.
        
    def run_ClassicTextclassfikation(self, lrs, epochs):
        train_df, test_df = self.get_Data_for_Classic_Version()

        for learning_rate in lrs:  
            #SimpleTransformer mit BERT 
            model_beschreibung_bert = f"Classic Textclassfikation mit Modell: BERT , einer Lernrate von '{learning_rate}' und einer Epochen-Anzahl von {epochs}"
            print(model_beschreibung_bert)
            kt_bert = ClassicTextclassfikation('bert', 'bert-base-cased', learning_rate, epochs)
            model = kt_bert.get_Classification_Model()
            kt_bert.train(model, train_df)
            f1_micro, f1_macro, mcc = kt_bert.evaluate(model, test_df)
            self.generate_Report(model_beschreibung_bert, f1_micro, f1_macro, mcc)
            #kt_bert.prediction(model, "Wir suchen App-Entwickler für den Bankensektor")

            #SimpleTransformer mit RoBERTa  
            model_beschreibung_RoBERTa = f"Classic Textclassfikation mit Modell: RoBERTa , einer Lernrate von '{learning_rate}' und einer Epochen-Anzahl von {epochs}"       
            print(model_beschreibung_RoBERTa)
            kt_roberta = ClassicTextclassfikation('roberta', 'roberta-base', learning_rate, epochs)
            model = kt_roberta.get_Classification_Model()
            kt_roberta.train(model, train_df)
            f1_micro, f1_macro, mcc = kt_roberta.evaluate(model,test_df)
            self.generate_Report(model_beschreibung_RoBERTa, f1_micro, f1_macro, mcc)
            #kt_roberta.prediction(model, "Wir suchen App-Entwickler für den Bankensektor")
    
    #Helper Methode um einen Report der Evaluatiosergebnisse zu erhalten. 

    def generate_Report(self, model_beschreibung, f1_micro, f1_macro, mcc): 
        dict = {'Model Beschreibung': model_beschreibung, 'F1-Score Micro':f1_micro, 'F1-Score Macro': f1_macro, 'MCC': f1_micro} 
        pd.DataFrame.from_records([dict]).to_csv('/Users/florunkel/01_Flo/02_Uni/Wirtschaftsinformatik/08_Semester/Bachelorarbeit/Autopart/src/Evaluation.csv',  index=False, sep = ';', encoding='utf-8', header=False, mode='a')

# In der Main Methode wird daher mittels der Aufrufe aus der Textklassifikation, die jeweiligen Machine Learning Methoden Machine Learning Methode und Crawler aufgerufen und ausgefuehrt. 
# vortrainierte Modelle für die Shot-Versionen ('deepset/gbert-large', 'xlm-roberta-large')
# Lernraten die fuer das Training verwendet werden (4e-4, 4e-5, 4e-6)
# Titel zur eingabe auf den zu crawlenden Webseiten ('softwareentwickler-e-commerce', 'softwareentwickler+bankensektor', 'softwareentwickler+für+Cloud-Lösungen')
# Namen der CSV-Datein ('/Results_Crawling_ECommerce.csv', '/Results_Crawling_Bankensektor.csv', '/Results_Crawling_Cloud.csv')

if __name__ == "__main__":
    models = ['deepset/gbert-large', 'xlm-roberta-large']
    learning_rate_values = [4e-4, 4e-5, 4e-6]
    pfad='/Users/florunkel/01_Flo/02_Uni/Wirtschaftsinformatik/08_Semester/Bachelorarbeit/Autopart/src/Crawling_Data' 
    list_titel = ['softwareentwickler-e-commerce', 'softwareentwickler+bankensektor', 'softwareentwickler+für+Cloud-Lösungen'] 
    list_csv_Name = ['/Results_Crawling_ECommerce.csv', '/Results_Crawling_Bankensektor.csv', '/Results_Crawling_Cloud.csv']

    #Textklassifikation().run_Crawler_StepStone(30, pfad, list_titel, list_csv_Name)
    #Textklassifikation().run_Crawler_Indeed(pfad, list_titel, list_csv_Name)
    #Textklassifikation().run_Combine_Crawler_Data(pfad, list_csv_Name)
    #Textklassifikation().run_Data_Analyse()

    Textklassifikation().run_ZeroShot(models, False)
    Textklassifikation().run_FewShot(models, learning_rate_values, 10, False)
    Textklassifikation().run_ClassicTextclassfikation(learning_rate_values, 10)