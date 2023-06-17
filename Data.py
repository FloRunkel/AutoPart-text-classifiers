from abc import ABC, abstractmethod

# Diese Abstract Klasse beeinhaltet alle notwendigen Methoden, die für die Erhebung der Daten benoetigt werden. 
# read_csv_Datei: einlesen der CSV_Datei
# split_in_Train_Test_data: Aufteilung der Daten in Trainings- und Testdaten.

class Data(ABC):
    
    @abstractmethod
    def read_csv_Datei(self):
        pass
    
    @abstractmethod
    def split_in_Train_Test_data(self): 
        pass