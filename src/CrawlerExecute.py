import csv
from Crawler_Indeed import Crawler_Indeed
from Crawler_Wikipedia import Crawler_Wikipedia
from Crawler_StepStone import Crawler_StepStone

# In dieser Klasse werden die einzelnen Crawler inizialisiert und die benötigten Informationen für das Extrahieren der Webseiteninhalte übergeben 

class CrawlerExecute:

    def __init__(self, pfad:str, list_titel:list, list_csv_Name:list, name_result_csv:str,  labels:list, example_sentences:list, company_name_sEC:list, company_name_sB:list, company_name_sC:list, crawler_select:dict,crawler_list:list):
        self.pfad = pfad
        self.list_titel = list_titel
        self.list_csv_Name = list_csv_Name
        self.name_result_csv = name_result_csv
        self.labels = labels
        self.example_sentences = example_sentences
        self.company_name_sEC = company_name_sEC
        self.company_name_sB = company_name_sB
        self.company_name_sC = company_name_sC
        self.crawler_select = crawler_select
        self.crawler_list = crawler_list

    # diese Methode ruft die einzelnen Crawler auf und fuehrt sie aus 

    def run_Crawler(self,**kwargs):

        number_of_stepPages = kwargs.get('numberStepsStone') if 'numberSteps' else 10

        for craw in self.crawler_list:
            if craw in self.crawler_select.keys():
                if self.crawler_select[craw]:
                    print (f'{craw} selected')
                    self.run_Crawler_Wikipedia() if craw == 'Wikipedia' else self.run_Crawler_Indeed() if craw == 'Indeed' else self.run_Crawler_StepStone(number_of_stepPages) if craw == 'StepStone' else print(f'{craw} doesnt exists')

        self.get_Data_together()

    # Mittels der Wiki API werden die Infos zu den fuehrenden Unternehmen gesammelt und in die jeweilige CSV-Datei geschrieben
    # Desweiteren wird der Crawlerklasse der Name der zu erstellenden CSV-Datei uebergeben. 

    def run_Crawler_Wikipedia(self): 
        for number_titel_EC in range(len(self.company_name_sEC)): 
            Crawler_Wikipedia(self.company_name_sEC[number_titel_EC],  self.pfad + self.list_csv_Name[0], self.example_sentences[0], self.labels[0]).write_into_csv()

        for number_titel_B in range(len(self.company_name_sB)): 
            Crawler_Wikipedia(self.company_name_sB[number_titel_B],  self.pfad + self.list_csv_Name[1], self.example_sentences[1], self.labels[1]).write_into_csv()

        for number_titel_CS in range(len(self.company_name_sC)): 
            Crawler_Wikipedia(self.company_name_sC[number_titel_CS],  self.pfad + self.list_csv_Name[2], self.example_sentences[2], self.labels[2]).write_into_csv()

    # Ruft die Crawler Indeed Klasse auf mit der Webseite, aus welcher der Inhalt extrahiert werden soll.
    # Desweiteren wird der Crawlerklasse der Name der zu erstellenden CSV-Datei uebergeben. 

    def run_Crawler_Indeed(self): 
        for number_titel in range(len(self.list_titel)): 
            Crawler_Indeed(f'https://de.indeed.com/jobs?q={self.list_titel[number_titel]}&l=Deutschland&from=searchOnHP&vjk=b03e724b97697e90&page=', self.pfad + self.list_csv_Name[number_titel], self.example_sentences[number_titel], self.labels[number_titel]).write_into_csv()

    # Ruft die Crawler Stepstone Klasse auf mit der Webseite, aus welcher der Inhalt extrahiert werden soll.
    # Desweiteren wird der Crawlerklasse der Name der zu erstellenden CSV-Datei uebergeben. 

    def run_Crawler_StepStone(self, number_of_Pages):
        for page in range(1, number_of_Pages):
            for number_titel in range(len(self.list_titel)): 
                Crawler_StepStone(f'https://www.stepstone.de/jobs/{self.list_titel[number_titel]}/in-deutschland?radius=30&page={page}&wci=300000115.html', self.pfad + self.list_csv_Name[number_titel], number_of_Pages, self.example_sentences[number_titel], self.labels[number_titel]).write_into_csv()

    # In dieser Methode werden die einzelnen CSV-Datein in eine gemeinsame Datei zusammengefuegt
    # @Parameter: name_result_csv; gibt den Namen der Datei an, in welche die Daten zusammengefuegt werden sollen.
    # @Parameter: list_csv_Name; ist eine Liste mit den Namen der CSV-Dateien (Results_Crawling - ECommerce/Cloud/Bankensektor) die zusammengefuegt werden sollen
    # @Parameter: pfad; gibt den Speicherort der CSV-Dateien an 

    def get_Data_together(self): 
        name_csv_01= self.pfad + self.list_csv_Name[0]
        name_csv_02= self.pfad + self.list_csv_Name[1]
        name_csv_03= self.pfad + self.list_csv_Name[2]
        daten = self.get_csv(name_csv_01) + self.get_csv(name_csv_02) + self.get_csv(name_csv_03)
        with open(self.pfad + self.name_result_csv, 'w') as result_csv:
            writer = csv.writer(result_csv, delimiter=';')
            writer.writerows(daten)
    
    # Dies ist eine Helper Methode der get_Data_together Methode, da sie die Daten aus den einzelnen CSV-Dateien in eine Liste speichert.
    # @Parameter: name_csv; Namen der CSV-Dateien (Results_Crawling - ECommerce/Cloud/Bankensektor) die zusammengefuegt werden sollen
    # @Return: Uebergabe der Daten aus den CSV_Dateien 

    def get_csv(self, name_csv): 
        daten=[]
        with open(name_csv, 'r') as csv_01:
            reader = csv.reader(csv_01, delimiter=';')
            next(reader)
            daten.extend([row for row in reader])
        return daten