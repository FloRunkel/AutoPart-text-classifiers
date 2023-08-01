from sklearn.model_selection import train_test_split
import pandas as pd
from Data import Data

# Datenvorberitung für die Machine Learning Methoden: SimpleTransformers

class Daten_for_Classic_Version(Data): 

    # @Parameter: name_csv_Datai; Namens der jewiligen einzulesenden CSV-Datei 

    def __init__(self, name_csv_Datai):
        self.name_csv_Datai = name_csv_Datai
    
    # Diese Methode dient dem lesen der CSV_Datei
    # Die gespeicherten Daten aus der CSV-Datei werden in einem Dictionary gespeichert
    # @Return: Daten aus der CSV-Datei in einem DataFrame

    def read_csv_Datei(self):
        df = pd.read_csv(self.name_csv_Datai, delimiter=';')
        return df.sample(frac = 1)
    
    # Für die SimpleTransformer Bibliothek, müssen die Zielvariablen in Zahlen angegeben werden. 
    # Daher werden die jeweiligen Klassen in Zahlen von 0 bis 3 umgewandelt 
    # @Return: DataFrame mit geaenderten Zielvariablen

    def changeLabels(self, df):
        df.replace('Softwareentwicklung im E-Commerce',0, inplace=True)
        df.replace('Softwareentwicklung im Bankensektor', 1, inplace=True)
        df.replace('Softwareentwicklung für Cloud-Lösungen', 2, inplace=True)
        df.replace('Sonstiges', 3, inplace=True)   
        return df
    
    # In dieser Methode werden die gemischten Daten aus dem Dictionary in Trainings und Testdaten unterteilt 
    # @Return: Trainings- und Testdaten 

    def split_in_Train_Test_data(self, df): 
        train_df, test_df = train_test_split(df, test_size=0.3)
        return train_df, test_df


    # Vorbereitung der Daten für Multi-Class 
    # @Return: Trainings- und Testdaten 

    def preparing_data_for_multi_class(self): 
        labeled_texts = self.changeLabels(self.read_csv_Datei())
        labeled_texts.columns = ['labels', 'text']
        return self.split_in_Train_Test_data(labeled_texts)
    
    # Vorbereitung der Daten für Multi-Label
    # @Return: Trainings- und Testdaten 

    def preparing_data_for_multi_label(self): 
        df = self.read_csv_Datei()
        df.columns = ['text', 'sonstiges', 'ecommerce', 'bank', 'cloud']
        df["ecommerce"] = df["ecommerce"].astype(int)
        df["bank"] = df["bank"].astype(int)
        df["cloud"] = df["cloud"].astype(int)
        df['labels'] = list(zip(df.sonstiges.tolist(), df.ecommerce.tolist(), df.bank.tolist(), df.cloud.tolist()))
        df = df.drop(columns=['sonstiges', 'ecommerce', 'bank', 'cloud'])
        return self.split_in_Train_Test_data(df)