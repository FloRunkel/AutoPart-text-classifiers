import csv

# Dies ist einer Helper-Klasse, die die einzelnen CSV-Dateien (Results_Crawling - ECommerce/Cloud/Bankensektor) in eine gemeinsame CSV-Datei Results_Crawling zusammenfügt

class Combine_Crawler_Data:

    # In dieser Methode werden die einzelnen CSV-Datein in eine gemeinsame Datei zusammengefuegt
    # @Parameter: name_result_csv; gibt den Namen der Datei an, in welche die Daten zusammengefuegt werden sollen.
    # @Parameter: list_csv_Name; ist eine Liste mit den Namen der CSV-Dateien (Results_Crawling - ECommerce/Cloud/Bankensektor) die zusammengefuegt werden sollen
    # @Parameter: pfad; gibt den Speicherort der CSV-Dateien an 

    def get_Data_together(self, pfad, name_result_csv, list_csv_Name): 
        name_csv_01= pfad + list_csv_Name[0]
        name_csv_02= pfad + list_csv_Name[1]
        name_csv_03= pfad + list_csv_Name[2]
        daten = self.get_csv(name_csv_01) + self.get_csv(name_csv_02) + self.get_csv(name_csv_03)
        with open(name_result_csv, 'w') as result_csv:
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
 
        
        
        