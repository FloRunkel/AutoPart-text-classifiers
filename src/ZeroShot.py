from transformers import pipeline
from sklearn.metrics import f1_score, matthews_corrcoef
from Klassifikator import Klassifikator

# Machine Learning Methode: Zero-Shot 
# Zero-Shot Learning ist eine Machine Learning Methode, bei der ein Modell trainiert wird, um Aufgaben oder Klassen zu erkennen, für die es während des Trainings keine direkten Beispiele erhalten hat. 
# Das Modell lernt, auf Basis von allgemeinem Wissen oder Informationen über die Eigenschaften der Aufgaben oder Klassen Vorhersagen zu treffen. 
# Es kann neue Aufgaben oder Klassen basierend auf diesem Wissen erkennen und klassifizieren.

class ZeroShot(Klassifikator):

    # @Parameter: model_name; gibt an, welches Vortrainierte Modell für die Zero-Shot Methode verwendet werden soll.  ('deepset/gbert-large', 'xlm-roberta-large')
    # @Parameter: train_sentence; ein Zufaellig ausgewaehlter Satz der für das Training vorgeschrieben ist
    # @Parameter: train_sentence_label; die zugörige korrekte Zielvariable. Dies dient dem Vergeliche bei einer evaluation
    # @Parameter: boolean_multi_label; über diesen Parameter kann entschieden werde, ob eine Multi-Klassifikation trainiert werden soll 

    def __init__(self, model_name,  multilabel_selecter):
        self.model_name = model_name
        self.multilabel_selecter = multilabel_selecter

    # getter Methode für die Zielvariablen
    # @Return: Eine Liste der jeweiligen Kategorien für die KLassifikation 

    def getLabels(self): 
        labels = ["Softwareentwicklung im E-Commerce", "Softwareentwicklung im Bankensektor", "Softwareentwicklung für Cloud-Lösungen", "Sonstiges"]
        return labels
    
    # diese Methode gibt die Pipline der Zero-Shot Methode wieder
    # @Return: Pipeline der Zero-Shot Methode 

    def create_pipeline(self):
        return pipeline("zero-shot-classification", model=self.model_name)
        
    # In der Train Methode wird mittels der davor generierten Pipline trainiert
    # @Return: Klassifizerungspipeline der Zero-Shot Methode 

    def train(self, text):
        classifier_pipeline = self.create_pipeline()
        return classifier_pipeline(text, self.getLabels(), multi_label=self.multilabel_selecter)
       
    # Hier wird eine Evaluation der Zero-Shot Methode durchgefuehrt und eine Prozentangabe für die jeweiligen Labels gegeben 
   
    def prediction(self, result): 
        for i in range(0,4):
            predicted_label = result['labels'][i]
            confidence_score = result['scores'][i]
            print(f'{predicted_label} -> {confidence_score:.2%}')
        
        return result['labels'][0]

    # Evaluierung des Modells 
    # Dabei wird die ausgabe des vorhergesagter Kategorie mit der eigentlichen Zielvariable verglichen, sowie eine Prozentangabe für die getroffene Klassifikation 

    def evaluate(self,data_prediction, data_ytrue):
        f1_macro = f1_score(data_ytrue, data_prediction, average='macro')
        f1_micro = f1_score(data_ytrue, data_prediction, average='micro')
        mcc = matthews_corrcoef(data_ytrue, data_prediction)

        print('f1-score macro: ', f1_macro , ', f1-score micro: ', f1_micro , ',  mcc:  ' , mcc)
        return f1_micro, f1_macro, mcc