from abc import ABC, abstractmethod

# Diese Abstract Klasse beeinhaltet alle notwendigen Methoden, die für die Machine Learning Modelle benoetigt werden. 
# @abstractmethod: train; damit werden die Modelle trainiert 
# @abstractmethod: evaluate; damit werden die Modelle ausgewertet 
# @abstractmethod: predcition; damit wird mittels der Modelle eine Vorhersage getroffen 

class Klassifikator(ABC):

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def prediction(self):
        pass