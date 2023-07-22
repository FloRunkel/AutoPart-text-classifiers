from sklearn.metrics import f1_score, matthews_corrcoef
from simpletransformers.classification import MultiLabelClassificationModel, MultiLabelClassificationArgs
from Klassifikator import Klassifikator

# Machine Learning Methode: SimpleTransformers 
# SimpleTransformers ist eine Python-Bibliothek für die Verwendung von Transformer-Modellen zur natuerlichen Sprachverarbeitung. 
# Sie bietet eine einfache Schnittstelle für Training, Auswertung und Anpassung von Modellen für Aufgaben wie Klassifikation und Textgenerierung.

class ClassicMultiLabelClassification(Klassifikator):
    
    # @Parameter: model; welches Vortrainierte Modell verwendet werden soll. (BERT oder RoBERTa)
    # @Parameter: model_name; gibt an, welches Vortrainierte Modell für die SimpleTransformers Methode verwendet werden soll
    # @Paramter: lrs; gibt an, welche Lernrate für das Modell verwendet werden soll
    # @Paramter: epochs; gibt die Epochenanzahl wieder

    def __init__(self, model, modelname, lrs, epochs):
        self.model = model
        self.modelname = modelname
        self.lrs = lrs
        self.epochs = epochs

    # getter Methode für die Zielvariablen
    # @Return: Eine Liste der jeweiligen Kategorien für die KLassifikation 

    def get_labels(self): 
        return ["Softwareentwicklung im E-Commerce", "Softwareentwicklung im Bankensektor", "Softwareentwicklung für Cloud-Lösungen", "Sonstiges"]
    
    # Festlegung der Klassificationsparameter für die Klassifikation 
    # @Return: Das Klassifikationsmodell mit den Klassificationsparameter

    def model_parameter(self):
        model_args = MultiLabelClassificationArgs()
        model_args.overwrite_output_dir = True
        model_args.learning_rate = self.lrs
        model_args.num_train_epochs = self.epochs
        model_args.reprocess_input_data=True
        return model_args
    
    # Erzeugung eines Klassifikationsmodels für die jeweilige Label-Klassifikation  
    # @Return: Das Klassifikationsmodell mit den Klassificationsparameter

    def get_Classification_Model(self): 
        return MultiLabelClassificationModel(self.model, self.modelname, args=self.model_parameter(), num_labels=4, use_cuda=False)
        
    # Trainieren des SimpleTransformers mittels des Klassificationsmodells und der Klassificationsparameter
    # @Parameter: trainData; Trainingsdaten für die Train-Methode der SimpleTransformers Bibliothek

    def train(self, model, trainData):
        model.train_model(trainData)
    
    # Evaluieren des Modelles mittels des F1-Scores und des MCCs
    # @Parameter: model; ist das bereits trainierte Modell, damit eine Evaluierung erfolgen kann
    # @Parameter: test_data; Testdaten für die Evaluierung des trainierten Modells
    # @Return: den F1-Score (Micro & Macro) sowie den MCC

    def evaluate(self, model, test_data):
        prediction_list = []
        target_list  = test_data['labels'].values.tolist()
        predictions, raw_outputs = model.predict(test_data['text'].values.tolist())

        for pre in predictions:
            prediction_list.append(pre)
        
        f1_macro = f1_score(target_list, prediction_list, average='macro')
        f1_micro = f1_score(target_list, prediction_list, average='micro')
        mcc = 'kein support fuer MultiLabel'

        print('f1-score macro: ', f1_macro , ', f1-score micro: ', f1_micro , ',  mcc:  ' , mcc)
        return f1_micro, f1_macro, mcc
    
    # Vorhersage für einen Satz auf basis des bereits Trainierten Modells 
    # @Parameter: model; ist das bereits trainierte Modell, damit eine Vorhersage getroffen werden kann
    # @Parameter: sentence; ein Satz für den eine Vorhersage getroffen werden soll

    def prediction(self, model, sentence):
        predictions, raw_outputs = model.predict([sentence])
        print(f"Die Eingabe '{sentence}' wurde als '{self.get_labels()[predictions[0]]}' klassifiziert.")
        return self.get_labels()[predictions[0]]