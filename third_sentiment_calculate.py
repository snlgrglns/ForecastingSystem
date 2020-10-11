import time
import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as panda
import threading

class third_sentiment_calculate():
    SENTIMENT_DICT = {}
    def __init__(self):
        self.TOTAL_ROWS = 0
        self.ROW_COUNT = 0

    def start(self, key_word_file_names):
        # files = ["sad", "happy"]
        # files = first_data_scrapping().KEY_WORDS
        # file2 = "happy.csv"
        th1 = threading.Thread(name='sentiment1', target=self.file_process, args=(key_word_file_names[0], ))
        th2 = threading.Thread(name='sentiment2', target=self.file_process, args=(key_word_file_names[1], ))
        # th3 = threading.Thread(name='progress', target=self.progress)
        # th3.start()
        th1.start()
        th2.start()
        th2.join()
        # th3.join()
        return self.SENTIMENT_DICT

    def sentiment_analysis(self, text):
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        return scores

    def progress(self):
        flag = True
        while flag:
            if(self.TOTAL_ROWS>0):
                analyzed = (self.ROW_COUNT/(self.TOTAL_ROWS)*100)
                print("\r Sentiment analysis = "+str(analyzed) + "%", end=" ")
                if(analyzed==100):
                    flag = False
            time.sleep(2)

    def file_process(self, key_word):
        try:
            cleaned_file = "clean_"+key_word+".csv"
            columns = ['_ch', 'date', 'year','month','text']
            # data_frame = panda.read_csv(cleaned_file,header=None, names=columns, encoding="latin-1") #"utf-8"
            data_frame = panda.read_csv(cleaned_file,header=None, names=columns, encoding="latin-1")
            total_count = sum(1 for line in open(cleaned_file))
            self.TOTAL_ROWS = self.TOTAL_ROWS + (total_count)
            nums = [1,total_count]
            # cleaned_text_list =  [[0 for j in range(6)] for i in range(total_count-1)]
            cleaned_text_list = [[0 for j in range(9)] for i in range(total_count-1)]
            pos_count = 0
            neg_count = 0
            neu_count = 0
            start_time = time.time()
            for i in range(1,nums[1]):
                if( (i+1)%1000 == 0 ):
                    print("[" + key_word + "] Tweets %d of %d has been processed" % (i+1, nums[1]-1) )
                self.ROW_COUNT = self.ROW_COUNT + 1

                single_text = data_frame['text'][i]
                # print(single_text)
                # t_data['sentiment']=data_frame.map_partitions(lambda df : df.apply(polar,axis=1))
                cleaned_text_list[i-1][0]=data_frame['date'][i]
                cleaned_text_list[i-1][1]=data_frame['year'][i]
                cleaned_text_list[i-1][2]=data_frame['month'][i]
                cleaned_text_list[i-1][3]=single_text
                sentiments = self.sentiment_analysis(single_text)
                cleaned_text_list[i-1][4] = sentiments["neg"]
                cleaned_text_list[i-1][5] = sentiments["pos"]
                cleaned_text_list[i-1][6] = sentiments["neu"]
                cleaned_text_list[i-1][7] = sentiments["compound"]
                if sentiments['compound'] == 0:
                    cleaned_text_list[i-1][8] = "NEUTRAL"
                    neu_count +=1
                elif sentiments['compound'] > 0:
                    # if sentiments['pos']-sentiments['neg'] > 0:
                    # pos_correct += 1
                    pos_count +=1
                    cleaned_text_list[i-1][8] = "POSITIVE"
                # elif not sentiments['compound'] < 0:
                else:
                    # if sentiments['pos']-sentiments['neg'] <= 0:
                    # neg_correct += 1
                    neg_count +=1
                    cleaned_text_list[i-1][8] = "NEGATIVE"
            end_time = time.time()
            elapsed_time = end_time - start_time
            # accuracy_positive = pos_correct/pos_count*100.0
            # accuracy_negative = neg_correct/neg_count*100.0
            accuracy_positive = pos_count/(pos_count+neg_count+neu_count)*100.0
            accuracy_negative = neg_count/(pos_count+neg_count+neu_count)*100.0
            accuracy_neu = neu_count/(pos_count+neg_count+neu_count)*100.0

            print("["+key_word+"]Process time = " + format(end_time - start_time))
            print("["+key_word+"]Positive sentiment = " + format(accuracy_positive))
            print("["+key_word+"]Neutral sentiment = " + format(accuracy_neu))
            print("["+key_word+"]Negative sentiment = " + format(accuracy_negative))
            self.SENTIMENT_DICT[key_word] = {
                "time": elapsed_time,
                "AP": accuracy_positive,
                "AN": accuracy_negative,
                "ANEU": accuracy_neu
            }
            clean_df = panda.DataFrame(cleaned_text_list,columns=['date', 'year', 'month', 'text', 'negative', "positive", "neutral", "compound", "sentiment"])
            # clean_df['target'] = 0
            clean_df.head()
            clean_df.to_csv("sentiment_"+key_word+".csv",encoding='utf-8')
        except Exception as ex:
            print("excep")
            print(ex)


if __name__ == '__main__':
    files = ["amazon", "google"]
    third_sentiment_calculate().start(files)
    print(third_sentiment_calculate().SENTIMENT_DICT)
#     sdc = third_sentiment_calculate().file_process("clean_google.csv")
