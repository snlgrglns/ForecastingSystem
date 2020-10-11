from first_data_scrapping import *
from second_data_clean import *
from third_sentiment_calculate import *
from fourth_prediction import *
import fifth_visualization_menu as v_menu
import time
class ui_menu():
    KEY_WORDS=[]
    def __init__(self):
        self.MENU_LIST = {1: "Start New Data Scrapping", 2:"Start if You have already csv files", 3:"Visualization", 6:"Exit"}
        self.CHOICE = 0
        self.clean_time_data = {}
        self.sentiment_data = {}
        self.accuracy_prediction_data = {}
        self.monthly_data = {}
        self.yearly_data = {}
        self.EXIT = False
    print("-----------------------------------------------------------------------\
        \nWelcome Sales Forecasting \
        \n-----------------------------------------------------------------------")
    def show_menu(self):
        while(self.EXIT!=True):
            self.display_menu()
            try:
                choice = int(input("Please select one option: "))
                while(choice not in self.MENU_LIST.keys()):
                    choice = int(input("Error!!! Please select the correct option: "))
                self.proceed_choice(choice)
            except Exception as ex:
                print(ex)
                print("Input error!!!!!!!!!")
                self.show_menu()


    def display_menu(self):
        print()
        for menu_item in self.MENU_LIST:
            print(str(menu_item) + ". " + self.MENU_LIST[menu_item])
        print()

    def enter_product(self):
        product1 = input("Please enter first product:").strip()
        while not product1:
            product1 = input("Empty!!! Please enter first product:").strip()

        product2 = input("Please enter second product:").strip()
        while not product2:
            product2 = input("Empty!!! Please enter second product:").strip()
        key_word = [product1, product2]
        return key_word

    def proceed_choice(self, choice):
        try:
            print("##################### "+str(choice)+". "+ self.MENU_LIST[choice]+" #########################")

            if(choice==1):
                self.KEY_WORDS = self.enter_product()
                # if __name__ == '__main__':
                scrap = first_data_scrapping()
                # if(len(self.KEY_WORDS)<1):
                scrap.run_scrap(self.KEY_WORDS)
                time.sleep(2)
                print("\n##################### Data scrapping compleded #########################")
                print("\n##################### Now proceeding to cleaning #########################")
                self.clean_time_data = second_data_clean().start(self.KEY_WORDS)
                time.sleep(2)
                print("\n##################### Cleaning completed #########################")
                print("\n##################### Now starting sentiment analysis #########################")
                self.sentiment_data = third_sentiment_calculate().start(self.KEY_WORDS)
                time.sleep(2)
                print("\n##################### Sentiment analysis completed #########################")
                print("\n##################### Now starting prediction accuracy #########################")
                self.accuracy_prediction_data, self.monthly_data, self.yearly_data = fourth_prediction().start(self.KEY_WORDS)
                time.sleep(2)
                print("\n##################### Prediction accuracy completed #########################")
                print("\n##################### Now starting visualization #########################")
                menu_init = v_menu.fifth_visualization_menu(self.clean_time_data, self.sentiment_data, self.accuracy_prediction_data, self.monthly_data, self.yearly_data)
                menu_init.main()
                # fth.main()
                print("\n##################### visualization completed #########################")
            elif(choice==2):
                self.KEY_WORDS = self.enter_product()
                print("\n##################### Now proceeding to cleaning #########################")
                self.clean_time_data = second_data_clean().start(self.KEY_WORDS)
                time.sleep(2)
                print("\n##################### Cleaning completed #########################")
                print("\n##################### Now starting sentiment analysis #########################")
                self.sentiment_data = third_sentiment_calculate().start(self.KEY_WORDS)
                time.sleep(2)
                print("\n##################### Sentiment analysis completed #########################")
                print("\n##################### Now starting prediction accuracy #########################")
                self.accuracy_prediction_data, self.monthly_data, self.yearly_data = fourth_prediction().start(self.KEY_WORDS)
                time.sleep(2)
                print("\n##################### Prediction accuracy completed #########################")
                print("\n##################### Now starting visualization #########################")
                menu_init = v_menu.fifth_visualization_menu(self.clean_time_data, self.sentiment_data, self.accuracy_prediction_data, self.monthly_data, self.yearly_data)
                menu_init.main()
                # fth.main()
                print("\n##################### visualization completed #########################")
            elif(choice==3):
                menu_init = v_menu.fifth_visualization_menu(self.clean_time_data, self.sentiment_data, self.accuracy_prediction_data, self.monthly_data, self.yearly_data)
                menu_init.main()
                # fth.main()
                print("\n##################### visualization completed #########################")
            elif(choice==6):
                self.EXIT = True
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    menu = ui_menu()
    menu.show_menu()
