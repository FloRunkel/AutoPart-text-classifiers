from CrawlerExecute import CrawlerExecute 
from TextklassifikatorExecute import TextklassifikatorExecute

# In der Main Methode wird daher mittels der Aufrufe aus der Textklassifikation, die jeweiligen Machine Learning Methoden Machine Learning Methode und Crawler aufgerufen und ausgefuehrt. 
# vortrainierte Modelle für die Shot-Versionen ('deepset/gbert-large', 'xlm-roberta-large')
# Lernraten die fuer das Training verwendet werden (4e-4, 4e-5, 4e-6)
# Titel zur eingabe auf den zu crawlenden Webseiten ('softwareentwickler-e-commerce', 'softwareentwickler+bankensektor', 'softwareentwickler+für+Cloud-Lösungen')
# Namen der CSV-Datein ('/Results_Crawling_ECommerce.csv', '/Results_Crawling_Bankensektor.csv', '/Results_Crawling_Cloud.csv')

if __name__ == "__main__":
        pfad='/Users/florunkel/01_Flo/02_Uni/Wirtschaftsinformatik/08_Semester/Bachelorarbeit/Autopart/src/Crawling_Data' 
        list_titel = ['softwareentwickler-e-commerce', 'softwareentwickler+bankensektor', 'softwareentwickler+für+Cloud-Lösungen'] 
        list_csv_Name = ['/Results_Crawling_ECommerce.csv', '/Results_Crawling_Bankensektor.csv', '/Results_Crawling_Cloud.csv']
        labels = ['Softwareentwicklung im E-Commerce', 'Softwareentwicklung im Bankensektor', 'Softwareentwicklung für Cloud-Lösungen']
        example_sentences = ["Das Unternehmen entwickelt Software für den E-Commerce", "Das Unternehmen entwickelt Software für den Bankensektor", "Das Unternehmen entwickelt Software für Cloud-Lösungen"]
        name_result_csv = '/Results_Crawling.csv'

        #Firmen die bekannt sind in der jeweiligen Branche Software zu entwickeln 
        company_name_sEC = ['Zalando','Otto Group','Shopify', 'About You', 'Mytheresa', 'Home24','Spreadshirt','flaconi','Westwing','ebay','Amazon', 'Bonprix', 'Magento', 'Demandware']
        company_name_sB = ['Avaloq','SAP SE','adesso AG','Finanz Informatik', 'Fiducia & GAD IT AG', 'Hypoport AG', 'Temenos Group','msg for banking','Finnova','Crealogix', 'CPU Softwarehouse']
        company_name_sC = ['Amazon Web Services','Microsoft Azure','Google Cloud Platform','Bluemix', 'IBM','Equinix', 'Dropbox','iCloud','VMware','Oracle', 'Salesforce','Equinix']

        crawler_list = ['Wikipedia','Indeed','StepStone']
        crawler_select = {
                'Wikipedia' : True,
                'Indeed' : True,
                'StepStone' : True
        }

        crawler = CrawlerExecute(pfad=pfad, list_titel=list_titel,list_csv_Name=list_csv_Name,name_result_csv=name_result_csv, labels=labels, example_sentences=example_sentences,company_name_sEC=company_name_sEC,company_name_sB=company_name_sB,company_name_sC=company_name_sC,crawler_select=crawler_select, crawler_list= crawler_list)

        #crawler.run_Crawler(numberStepsStone=10)

        models =  ['xlm-roberta-large']  #['deepset/gbert-large', 'xlm-roberta-large'] #['deepset/gbert-large'] ['xlm-roberta-large'] 
        learning_rate_values = [1e-05]   #[1e-05, 2e-5, 3e-5, 4e-4, 4e-5, 4e-6]    
        epochs =  18
        multilabel_selecter= True  
        percentual_data_use = 1

        Textklassifikator_list = ['Zero-Shot','Few-Shot','Classic']
        Textklassifikator_select = {
                'Zero-Shot' : False,  
                'Few-Shot' : False,
                'Classic' : True
        }

        klassifikator = TextklassifikatorExecute(pfad=pfad, models=models, learning_rate_values=learning_rate_values,epochs=epochs,multilabel_selecter=multilabel_selecter, percentual_data_use=percentual_data_use, Textklassifikator_select=Textklassifikator_select, Textklassifikator_list= Textklassifikator_list)

        #klassifikator.run_Datenaufbereitung()
        #klassifikator.run_Data_Analyse('/Data_MC.csv')

        klassifikator.run_Textklassifikator()
        #klassifikator.generate_Evaluation_Graphik()