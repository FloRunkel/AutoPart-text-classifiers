from flair.data import Corpus, Sentence
from flair.embeddings import TransformerDocumentEmbeddings
from flair.datasets import SentenceDataset
from flair.trainers import ModelTrainer
from flair.models import TARSClassifier
from sklearn.metrics import f1_score, matthews_corrcoef
from Klassifikator import Klassifikator

# Machine Learning Methode: Few-Shot 
# Few-Shot Learning ist eine Machine Learning Methode, bei der ein Modell mit nur einer begrenzten Anzahl von Trainingsbeispielen trainiert wird, um neue Aufgaben oder Klassen zu erkennen. 
# Das Modell lernt, aus wenigen Beispielen zu generalisieren und Muster zu erkennen, um neue, aehnliche Beispiele zu klassifizieren.

class FewShot(Klassifikator):

    # @Parameter: model; welches Vortrainierte Modell verwendet werden soll. ()'deepset/gbert-large', 'xlm-roberta-large')
    # @Paramter: lrs; gibt an, welche Lernrate für das Modell verwendet werden soll
    # @Paramter: epochs; gibt die Epochenanzahl wieder
    # @boolean_multiLabel; ob eine Multi-Klassifikation erfolgen soll
    
    def __init__(self, model, lrs, epochs, boolean_multiLabel):
        self.model = model
        self.epochs = epochs 
        self.lrs = lrs
        self.boolean_multiLabel = boolean_multiLabel
    
    # In dieser Methode werden die aufgeteilten Trainings- und Testdaten in ein SentenceDataset gespeichert
    # @Return: Einen SentenceDataset mit den jeweiligen Eingabesequenzen 

    def create_dataset(self, texts, labels):
        sentences = []
        for text, label in zip(texts, labels): # type: ignore
            sentences.append(Sentence(text).add_label('Textclassification', label))
        return SentenceDataset(sentences)
    
    # Hier wird ein Corpus aus den Trainings- und Testdaten erstellt, der anschließend dem Modell uebergeben werden
    # @Return: Corpus aus den Trainings- und Testdaten

    def create_Corpus(self, train_texts, train_labels, test_texts, test_labels):
        train_dataset = self.create_dataset(train_texts, train_labels)
        test_dataset = self.create_dataset(test_texts, test_labels)

        return Corpus(train=train_dataset, test=test_dataset)
    
    # Hier wird das TARS Modell initialisiert. 
    # Zudem wird der Methode der Corpus aus Train- und Testdaten übergeben.
    # @Return: TARS Model 

    def initial_TARS_model(self, corpus):
        tars = TARSClassifier(embeddings=TransformerDocumentEmbeddings(model=self.model, fine_tune=True, batch_size=16))
        tars.add_and_switch_to_new_task(task_name='Textclassification', label_dictionary=corpus.make_label_dictionary(label_type = 'Textclassification'), label_type = 'Textclassification', multi_label= self.boolean_multiLabel)
        return tars
    
    # Gibt das Model mit dem TARS und dem Corpus wieder 
    # @Return: ModelTrainer mit dem initialisierten TARS und dem Coropus aus Trainings- und Testdaten

    def get_ModelTrainier(self, corpus): 
        return ModelTrainer(self.initial_TARS_model(corpus), corpus) 

    # Das eigentliche Training des Few-Shots
    # Uebergeben wird hierbei das beriets initialisierte TARS Modell und der Corpus aus den Trainings- und Testdaten. 
    # Zudem werden hier die epochen und die Lernrate eingestzet die der Klasse über den Konstruktor mitgeteilt wurden. 

    def train(self, corpus):
        self.get_ModelTrainier(corpus).train(base_path='resources/taggers/Textclassification',learning_rate=self.lrs, mini_batch_size=1,max_epochs=self.epochs, train_with_dev=True, save_final_model=True)

    # Evaluieren des Modelles mittels des F1-Scores und des MCCs
    # @Parameter: test_data; Testdaten für die Evaluierung des trainierten Modells
    # @Parameter: test_labels; die Zielvaraiblen in dem Fall y-TRUE
    # @Return: den F1-Score (Micro & Macro) sowie den MCC
    
    def evaluate(self, test_text, test_labels):
        tars = TARSClassifier.load('resources/taggers/Textclassification/final-model.pt')
        prediction_list=[]

        for text in test_text:
            sentence = Sentence(text)
            tars.predict(sentence, multi_label=self.boolean_multiLabel)
        
            if self.boolean_multiLabel == True: 
                for label in sentence.labels:
                    prediction_list.append((label.value))        
            else: 
                prediction_list.append(sentence.labels[0].value)
                
        f1_macro = f1_score(test_labels, prediction_list, average='macro')
        f1_micro = f1_score(test_labels, prediction_list, average='micro')
        mcc = matthews_corrcoef(test_labels, prediction_list)

        print('f1-score macro: ', f1_macro , ', f1-score micro: ', f1_micro , ',  mcc:  ' , mcc)
        return f1_micro, f1_macro, mcc

    # Mit dieser Methode laesst sich eine erste Vorhersage für einen Satz geben 
    # Dafür muss wieder das TARS Modell uebergeben werden, sowei ein Satz der der Vorhersage dient

    def prediction(self, sentence_for_prediction):
        tars = TARSClassifier.load('resources/taggers/Textclassification/final-model.pt')
        sentence = Sentence(sentence_for_prediction)
        tars.predict(sentence, multi_label=self.boolean_multiLabel)
        prediction_list=[]

        if self.boolean_multiLabel == True: 
            for label in sentence.labels:
                    prediction_list.append((label.value))
        else: 
            prediction_list.append(sentence.labels[0].value)
        
        print(sentence, "-> Predicted labels:", prediction_list)