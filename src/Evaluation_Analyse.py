import matplotlib.pyplot as plt
import pandas as pd

# Diese Klasse dient der Anylse der Daten, was zum Verstaendins des outputs der jeweiligen Machine Learning Methode beitragen kann

class Evaluation_Analyse:

    # @Paramter: name_csv_Datai; Name der zu analysierenden CSV-Datei
    
    def __init__(self, pfad_name_csv_Datai):
        self.pfad_name_csv_Datai = pfad_name_csv_Datai

    # DataFrame aus der CSV-Datei erstellen

    def read_csv_Datei(self):
        return pd.read_csv(self.pfad_name_csv_Datai, delimiter=';')
    
    # diese Methode erstellt ein Diagramm zur graphischen Analyse der Evaluationsergebnisse
    
    def graphik(self):
        df = self.read_csv_Datei()
        num_models = len(df)
        index = range(num_models)
        plt.title('Zero-Shot')

        plt.plot(index, df['F1-Score Micro'], label='F1-Score Micro', color='blue')
        plt.plot(index, df['F1-Score Macro'], label='F1-Score Macro', color='orange')
        plt.plot(index, df['MCC'], label='MCC', color='green')
        plt.xlabel('Model Description')
        plt.ylabel('Score')
        plt.xticks(index, df['Model Description'], rotation=45, ha='right')
        plt.ylim(-1,1)
        plt.legend()
        plt.show()
