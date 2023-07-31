from ZeroShot import ZeroShot
from FewShot import FewShot
from ClassicMultiClassClassification import ClassicMultiClassClassification
from ClassicMultiLabelClassification import ClassicMultiLabelClassification
from Daten_for_Shot_Versions import Daten_for_Shot_Versions 
from Daten_for_Classic_Version import Daten_for_Classic_Version
from Datenaufbereitung import Datenaufbereitung
from Daten_Analyse import Daten_Analyse
from Evaluation_Analyse import Evaluation_Analyse
import pandas as pd 

# In dieser Klasse werden die einzelnen Textklassifikatoren inizialisiert und die benötigten Parameter und Daten für die Klassifikatoren übergeben 

class TextklassifikatorExecute:

    def __init__(self, pfad:str,  models:list, learning_rate_values:list, epochs:int, multilabel_selecter:bool, percentual_data_use:float, Textklassifikator_select:dict,Textklassifikator_list:list):
        self.pfad = pfad
        self.models = models
        self.learning_rate_values = learning_rate_values
        self.epochs = epochs
        self.multilabel_selecter = multilabel_selecter
        self.percentual_data_use = percentual_data_use
        self.Textklassifikator_select = Textklassifikator_select
        self.Textklassifikator_list = Textklassifikator_list

    # diese Methode ruft die einzelnen Crawler auf und fuehrt sie aus 

    def run_Textklassifikator(self):
        for tkl in self.Textklassifikator_list:
            if tkl in self.Textklassifikator_select.keys():
                if self.Textklassifikator_select[tkl]:
                    print (f'{tkl} selected')
                    self.run_ZeroShot() if tkl == 'Zero-Shot' else self.run_FewShot() if tkl == 'Few-Shot' else self.run_ClassicTextclassfikation() if tkl == 'Classic' else print(f'{tkl} doesnt exists')

    # Datenvorverarbeitung für die ML-Modelle 

    def run_Datenaufbereitung(self): 
        Datenaufbereitung(self.pfad + '/Results_Crawling.csv').datenvorverarbeitung()
    
    # Diese Methode dient dazu, die erlangten Daten aus den Webseiten mittels Graphiken zu Analysieren. 
    # Mittels der verteilung_Data_plot Methode kamm die Verteilung der einzelnen Kategorien in der CSV-Datei genauer betrachtet werden und Ausschlüsse über die Qualität der Daten geben. 

    def run_Data_Analyse(self, name_to_analyse_data):
        analyse = Daten_Analyse(self.pfad + name_to_analyse_data)
        analyse.verteilung_Data_plot()
        analyse.satzlaenge_Data_plot()
        analyse.woerterHaeufigkeit()
    
    # In dieser Methode wird die Daten_for_Shot_Versions Klasse aufgerufen, in der die Daten für die Shot Learning Methoden vorberitet werden. 
    # Die Methode wird zudem anschließend in der run_ZeroShot und run_FewShot Methode verwendet, um die Daten aus der CSV-Datei in einem Dictionary zu uebergeben.
    
    def get_Data_for_Shot_Versions(self):
        return Daten_for_Shot_Versions(self.pfad + '/Data_MC.csv').split_in_Train_Test_data()
   
    # In dieser Methode wird die Daten_for_Classic_Version Klasse aufgerufen, in der die Daten für die klassischen Learn Methoden vorberitet werden. 
    # Die Methode wird zudem anschließend in der run_ClassicTextklassification run Methode verwendet, um die Daten aus der CSV-Datei in einem DataFrame zu uebergeben.
 # In dieser Methode wird die Daten_for_Classic_Version Klasse aufgerufen, in der die Daten für die klassischen Learn Methoden vorberitet werden. 
    # Die Methode wird zudem anschließend in der run_ClassicTextklassification run Methode verwendet, um die Daten aus der CSV-Datei in einem DataFrame zu uebergeben.

    def get_Data_for_Classic_Version(self):
        if self.multilabel_selecter == True: 
            return Daten_for_Classic_Version(self.pfad + '/Data_ML.csv').preparing_data_for_multi_label()
        else:
            return Daten_for_Classic_Version(self.pfad + '/Data_MC.csv').preparing_data_for_multi_class()

    # In dieser Methode wird die Machine Learning Methode Zero Shot angewendet.
    # Dabei werden die Daten mittels des Dictionarys aus der get_Data_for_Shot_Versions Methode übergeben und anschließend trainiert.

    def run_ZeroShot(self):
        train_texts, test_texts, train_labels, test_labels = self.get_Data_for_Shot_Versions()
            
        for model in self.models: 
            model_beschreibung = f"Zero-Shot mit Modell: '{model}'"
            print(model_beschreibung)
            data_prediction, data_ytrue = [], []
            i=0

            zs = ZeroShot(model, self.multilabel_selecter)
            for text, label in zip(test_texts, test_labels): 
                result = zs.train(text)
                data_prediction.append(result['labels'][0])#type: ignore
                data_ytrue.append(label)
                i=i+1

                if i == (len(test_texts)* self.percentual_data_use):
                    break; 

            f1_micro, f1_macro, mcc = zs.evaluate(data_prediction, data_ytrue)
            self.generate_Report(model_beschreibung, f1_micro, f1_macro, mcc)
        
    # In dieser Methode wird die Machine Learning Methode Few Shot angewendet.
    # Dabei werden die Daten mittels des Dictionarys aus der get_Data_for_Shot_Versions Methode uebergeben.

    def run_FewShot(self):
        train_t, test_t, train_l, test_l = self.get_Data_for_Shot_Versions()
        train_texts = train_t[:int(self.percentual_data_use * len(train_t))]
        test_texts = test_t[:int(self.percentual_data_use * len(test_t))]
        train_labels = train_l[:int(self.percentual_data_use * len(train_l))]
        test_labels = test_l[:int(self.percentual_data_use  * len(test_l))]

        for model in self.models: 
            for learning_rate in self.learning_rate_values:  
                model_beschreibung = f"Modell: '{model}', Lernrate: '{learning_rate}'"
                print(model_beschreibung)
                
                fs = FewShot(model, learning_rate, self.epochs, self.multilabel_selecter)
                corpus_fs = fs.create_Corpus(train_texts, train_labels, test_texts, test_labels)
                fs.train(corpus_fs)
                f1_micro, f1_macro, mcc = fs.evaluate(test_texts, test_labels)
                self.generate_Report(model_beschreibung, f1_micro, f1_macro, mcc)

    # In dieser Methode wird die Machine Learning Methode SimpleTransformers angewendet.
    # Dabei werden die Daten mittels des DataFrames aus der get_Data_for_Classic_Version Methode uebergeben.
        
    def run_ClassicTextclassfikation(self):
        train_df, test_df = self.get_Data_for_Classic_Version()
        train =  train_df.sample(frac=self.percentual_data_use)
        test =  test_df.sample(frac=self.percentual_data_use)

        for learning_rate in self.learning_rate_values:  
            if self.multilabel_selecter == True: 
                # MULTI-LABEL
                for model in self.models: 
                    if model == 'deepset/gbert-large': 
                        model_beschreibung_bert_ml = f" Multi-Label Classic Textclassfikation mit Modell: BERT , einer Lernrate von '{learning_rate}' und einer Epochen-Anzahl von '{self.epochs}' und der Verwendung von "+"{:.0%}".format(self.percentual_data_use)+" der verfuegbaren Daten."
                        print(model_beschreibung_bert_ml)
                        kt_bert_ml = ClassicMultiLabelClassification('bert', 'bert-base-cased', learning_rate, self.epochs)
                        model = kt_bert_ml.get_Classification_Model()
                        kt_bert_ml.train(model, train)
                        f1_micro, f1_macro, mcc = kt_bert_ml.evaluate(model, test)
                        self.generate_Report(model_beschreibung_bert_ml, f1_micro, f1_macro, mcc)

                    elif model == 'xlm-roberta-large': 
                        model_beschreibung_RoBERTa_ml = f" Multi-Label Classic Textclassfikation mit Modell: RoBERTa , einer Lernrate von '{learning_rate}' und einer Epochen-Anzahl von '{self.epochs}' und der Verwendung von "+"{:.0%}".format(self.percentual_data_use)+" der verfuegbaren Daten."
                        print(model_beschreibung_RoBERTa_ml)
                        kt_roberta_ml = ClassicMultiLabelClassification('roberta', 'roberta-base', learning_rate, self.epochs)
                        model = kt_roberta_ml.get_Classification_Model()
                        kt_roberta_ml.train(model, train)
                        f1_micro_r, f1_macro_r, mcc_r = kt_roberta_ml.evaluate(model, test)
                        self.generate_Report(model_beschreibung_RoBERTa_ml, f1_micro_r, f1_macro_r, mcc_r)
                    else: 
                        print('keine Implementierung fuer dieses Vortrainierte Modell')
            else:
                # MULTI-CLASS
                for model in self.models: 
                    if model == 'deepset/gbert-large': 
                        model_beschreibung_bert = f"BERT , Lernrate: '{learning_rate}'"
                        print(model_beschreibung_bert)
                        kt_bert = ClassicMultiClassClassification('bert', 'bert-base-cased', learning_rate, self.epochs)
                        model = kt_bert.get_Classification_Model()
                        kt_bert.train(model, train)
                        f1_micro_b, f1_macro_b, mcc_b= kt_bert.evaluate(model, test)
                        self.generate_Report(model_beschreibung_bert, f1_micro_b, f1_macro_b, mcc_b)
                    
                    elif model == 'xlm-roberta-large': 
                        model_beschreibung_RoBERTa= f"Modell: RoBERTa , Lernrate: '{learning_rate}'"
                        print(model_beschreibung_RoBERTa)
                        kt_roberta= ClassicMultiClassClassification('roberta', 'roberta-base', learning_rate, self.epochs)
                        model = kt_roberta.get_Classification_Model()
                        kt_roberta.train(model, train)
                        f1_micro_r, f1_macro_r, mcc_r = kt_roberta.evaluate(model,test)
                        self.generate_Report(model_beschreibung_RoBERTa, f1_micro_r, f1_macro_r, mcc_r)
                    else: 
                        print('keine Implementierung fuer dieses Vortrainierte Modell')

    # Methode um einen Report der Evaluatiosergebnisse zu erhalten. 

    def generate_Report(self, model_beschreibung, f1_micro, f1_macro, mcc): 
        pd.DataFrame.from_records([{'Model Beschreibung': model_beschreibung, 'F1-Score Micro':f1_micro, 'F1-Score Macro': f1_macro, 'MCC': mcc} ]).to_csv('/Users/florunkel/01_Flo/02_Uni/Wirtschaftsinformatik/08_Semester/Bachelorarbeit/Autopart/src/Evaluation.csv',  index=False, sep = ';', encoding='utf-8', header=False, mode='a')

    def generate_Evaluation_Graphik(self): 
        Evaluation_Analyse('/Users/florunkel/01_Flo/02_Uni/Wirtschaftsinformatik/08_Semester/Bachelorarbeit/Autopart/src/Evaluation.csv').graphik()