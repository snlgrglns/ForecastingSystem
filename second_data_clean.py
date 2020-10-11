import re
import time
import datetime
import pandas as panda
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer
import threading
# from first_data_scrapping import *

class second_data_clean():
    CLEAN_DICT = {}
    def __init__(self):
        self.TOKENIZER = WordPunctTokenizer()
        self.TOTAL_ROWS = 0
        self.ROW_COUNT = 0
        self.PATTERN_1 = r'@[A-Za-z0-9_]+'
        self.PATTERN_2 = r'https?://[^ ]+'
        self.PATTERN_COMBINED = r'|'.join((self.PATTERN_1, self.PATTERN_2))
        self.PATTERN_URL = r'www.[^ ]+'
        self.NEGATION_DICT = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                        "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                        "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                        "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                        "mustn't":"must not"}
        self.PATTERN_NEGATION = re.compile(r'\b(' + '|'.join(self.NEGATION_DICT.keys()) + r')\b')

    def start(self, key_word_file_names):
        # files = ["sad", "happy"]
        # files = first_data_scrapping().KEY_WORDS
        # file2 = "happy.csv"
        th1 = threading.Thread(name='product1', target=self.save, args=(key_word_file_names[0], ))
        th2 = threading.Thread(name='product2', target=self.save, args=(key_word_file_names[1], ))
        th3 = threading.Thread(name='progress', target=self.progress)
        th3.start()
        th1.start()
        th2.start()
        th3.join()
        # return key_word_file_names
        return self.CLEAN_DICT

    def progress(self):
        flag = True
        while flag:
            # print("1",self.TOTAL_ROWS)
            # print("2",self.ROW_COUNT)
            if(self.TOTAL_ROWS>0):
                fetched_percent = (self.ROW_COUNT/(self.TOTAL_ROWS)*100)
                print("\r Data Clean = "+str(fetched_percent) + "%", end=" ")
                if(fetched_percent==100):
                    flag = False
            time.sleep(2)

    def date_format(self, date_string):
        new_dt = date_string[:19]
        # print(new_dt)
        format_str = '%Y-%m-%d %H:%M:%S'#'%d/%m/%Y' # The format
        dt_obj = datetime.datetime.strptime(new_dt, format_str)
        return dt_obj.year, dt_obj.month#, dt_obj.day


    def clean_tweet(self, text):
        beauty_soup = BeautifulSoup(text, 'lxml')
        souped = beauty_soup.get_text()
        try:
            bom_removed = souped.decode("utf-8-sig").replace(u"\ufffd", "?")
        except:
            bom_removed = souped
        filtered = re.sub(self.PATTERN_COMBINED, '', bom_removed)
        filtered = re.sub(self.PATTERN_URL, '', filtered)
        lower_case = filtered.lower()
        negation_handled = self.PATTERN_NEGATION.sub(lambda x: self.NEGATION_DICT[x.group()], lower_case)
        letters_only = re   .sub("[^a-zA-Z]", " ", negation_handled)
        words = [x for x  in self.TOKENIZER.tokenize(letters_only) if len(x) > 1] #tokenize and remove white space
        return (" ".join(words)).strip()

    def save(self, key_word):
        noisy_file = key_word+".csv"
        columns = ['id','text','date']
        data_frame = panda.read_csv(noisy_file,header=None, names=columns, encoding="latin-1") #"utf-8"
        # data_frame = data_frame.drop(data_frame[(data_frame["text"] == "b''")].index)
        total_count = sum(1 for line in open(noisy_file))
        self.TOTAL_ROWS = self.TOTAL_ROWS + (total_count - 1)
        nums = [1,total_count]
        start_time = time.time()
        # cleaned_text_list =  [[0 for j in range(4)] for i in range(total_count-1)]
        cleaned_text_list =  [[0 for j in range(4)] for i in range(total_count-1)]
        row_iterate = 0
        # zero_occur_count = 0
        for i in range(nums[0],nums[1]):
            if( (i+1)%1000 == 0 ):
                print("["+key_word+"]Tweets %d of %d has been processed" % (i+1, nums[1]-1) )
            self.ROW_COUNT = self.ROW_COUNT + 1
            cleaned_txt = self.clean_tweet(data_frame['text'][i])
            if(len(cleaned_txt.strip())>0 and cleaned_txt!=0):
                # cleaned_text_list.append(cleaned_txt)
                date_str = data_frame['date'][i]
                cleaned_text_list[row_iterate][0]=date_str
                year, month = self.date_format(date_str)
                cleaned_text_list[row_iterate][1]=year
                cleaned_text_list[row_iterate][2]=month
                cleaned_text_list[row_iterate][3]=cleaned_txt
                row_iterate=row_iterate+1
            else:
                # zero_occur_count=zero_occur_count+1
                size = len(cleaned_text_list)
                cleaned_text_list.pop(size-1)
            # clean_tweet_texts[i-1][0]=self.clean_tweet(single_text)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("["+key_word+"]Clean time for " + noisy_file + " = " + str(elapsed_time))
        self.CLEAN_DICT[key_word] = {"time": elapsed_time}
        clean_df = panda.DataFrame(cleaned_text_list,columns=['date','year','month','text'])
        clean_df.head()
        clean_df.to_csv('clean_'+noisy_file,encoding='utf-8')
if __name__ == '__main__':
    sdc = second_data_clean().start(["google", "amazon"])
    print(second_data_clean().CLEAN_DICT)
