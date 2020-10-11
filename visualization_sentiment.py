import pylab as plt1
import numpy as np

class visualization_sentiment_time():
    def __init__(self, data):
        self.data = data

    def start(self):
        # KEY_WORD = ["google", "amazon"]
        # data = {'amazon': {'time': 0.4288520812988281, 'AP': 81.25, 'AN': 100.0}, 'google': {'time': 0.4358344078063965, 'AP': 16.666666666666664, 'AN': 100.0}}
        # data = third_sentiment_calculate.SENTIMENT_DICT
        KEY_WORD = list(self.data.keys())
        kw1, kw2 = KEY_WORD[0], KEY_WORD[1]
        times_arr = [self.data[kw1]['time'], self.data[kw2]['time']]
        # positive_accuracy_arr = [data[kw1]['AP'], data[kw2]['AP']]
        x = np.arange(2)
        fig_time, ax = plt1.subplots()
        plt1.bar(x, times_arr)
        plt1.xticks(x, (kw1, kw2))
        for i, v in enumerate(times_arr):
            ax.text(i, v, " "+"{0:.4f}".format(v) + " secs", color='black', va='center', fontweight='bold')
        fig_time.canvas.set_window_title('Graph for Sentiment Processing Time')

        plt1.title('Sentiment Processing Time for ' + kw1 + " and " +kw2)
        plt1.xlabel("Key words (Products)")
        plt1.ylabel("Time in seconds")
        plt1.tight_layout()
        plt1.show()

class visualization_sentiment_accuracy():
    def __init__(self, data):
        self.data = data

    def start(self):
            # label = tk.Label(self, text="Sentiment Analysis Graph")
            # label.pack(pady=10,padx=10)
            # KEY_WORD = ["google", "amazon"]
            # data = {'amazon': {'time': 0.4288520812988281, 'AP': 81.25, 'AN': 100.0, 'ANEU':50}, 'google': {'time': 0.4358344078063965, 'AP': 16.666666666666664, 'AN': 100.0, 'ANEU':25}}
            # data = third_sentiment_calculate.SENTIMENT_DICT
            KEY_WORD = list(self.data.keys())
            kw1, kw2 = KEY_WORD[0], KEY_WORD[1]
            positive_accuracy_arr = [self.data[kw1]['AP'], self.data[kw2]['AP']]
            pos_arr = [self.data[kw1]['AP'], self.data[kw2]['AP']]
            neg_arr = [self.data[kw1]['AN'], self.data[kw2]['AN']]
            neu_arr = [self.data[kw1]['ANEU'], self.data[kw2]['ANEU']]
            sub_names_arr = ("positive", "negative", "neutral")
            # positive_accuracy_arr = [self.data[kw1]['AP'], self.data[kw2]['AP']]
            # print(pos_arr)
            # print(neg_arr)
            # print(sub_names_arr)
            # print(self.data)
            # exit()
            N = 2
            ind = np.arange(N)  # the x locations for the groups
            width = 0.27       # the width of the bars

            fig = plt1.figure()
            ax = fig.add_subplot(111)

            xvals = pos_arr
            rects1 = ax.bar(ind, xvals, width, color='b')
            yvals = neg_arr
            rects2 = ax.bar(ind+width, yvals, width, color='g')
            zvals = neu_arr
            rects3 = ax.bar(ind+width*2, zvals, width, color='r')

            # ax.set_ylabel('')
            ax.set_xticks(ind+width)
            ax.set_xticklabels([kw1, kw2])
            ax.legend( (rects1[0], rects2[0], rects3[0]), sub_names_arr )

            def autolabel(rects):
                for rect in rects:
                    h = rect.get_height()
                    ax.text(rect.get_x()+rect.get_width()/2., 1*h, "{0:.2f}".format(h),
                            ha='center', va='bottom')

            autolabel(rects1)
            autolabel(rects2)
            autolabel(rects3)
            fig.canvas.set_window_title('Graph for Sentiments')
            plt1.title('Graph for Sentiments ' + kw1 + " and " +kw2)
            plt1.xlabel("Keywords(Products)")
            plt1.ylabel("Sentiment Analysis in 100%")
            plt1.tight_layout()
            plt1.show()

class visualization_sentiment_monthly():
    def __init__(self, data):
        self.data = data
        # data = {}
        # data=fourth_prediction.PREDICTION_DATA_MONTHLY_DICT
    def start(self):
        # data = fourth_prediction.PREDICTION_DATA_MONTHLY_DICT
        KEY_WORD = list(self.data.keys())
        # keyword1, keyword2 = KEY_WORD[0], KEY_WORD[1]
        for keyword in KEY_WORD:
            grouped_positive_arr_mnth = self.data[keyword]["POSITIVE"]
            grouped_negative_arr_mnth = self.data[keyword]["NEGATIVE"]
            grouped_neutral_arr_mnth = self.data[keyword]["NEUTRAL"]
            pos_percent, neg_percent, neu_percent = self.array_to_percentage(grouped_positive_arr_mnth, grouped_negative_arr_mnth, grouped_neutral_arr_mnth)
            # exit()
            # x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            # x = range(1,13)
            x = ["Jan", "Feb","Mar", "Apr", "May", "June","July", "Aug", "Sep", "Oct", "Nov", "Dec"]
            y = [pos_percent, neg_percent, neu_percent]
            labels=['POSITIVE', 'NEGATIVE', 'NEUTRAL']
            lines=[('r','-'),('g','-.'),('b',':')]
            fig = plt1.gcf()
            fig.canvas.set_window_title('Monthly Sentiments')
            if(KEY_WORD.index(keyword) == 0):
                plt1.subplot(2,1,1)
            else:
                plt1.subplot(2,1,2)
            # loop over data, labels and colors
            for i in range(len(y)):
                plt1.plot(x,y[i],color=lines[i][0],linestyle=lines[i][1],label=labels[i])
            plt1.title("Monthly Sentiment for " + keyword)
            plt1.xlabel("Months")
            plt1.ylabel("Sentiments in Percent")
            plt1.legend()
            plt1.tight_layout()
        plt1.show()


    def array_to_percentage(self,pos, neg, neu):
        pos_percent = [0]*12
        neg_percent = [0]*12
        neu_percent = [0]*12
        for i in range(0,12):
            # print(i)
            total_i = pos[i] + neg[i]+neu[i]
            if(total_i>0):
                pos_percent[i] = pos[i]*100/total_i
                neg_percent[i] = neg[i]*100/total_i
                neu_percent[i] = neu[i]*100/total_i
            else:
                pos_percent[i] = 0
                neg_percent[i] = 0
                neu_percent[i] = 0
        return pos_percent, neg_percent, neu_percent

class visualization_sentiment_yearly():
    def __init__(self, data):
        self.data = data
        # data=fourth_prediction.PREDICTION_DATA_MONTHLY_DICT
    def start(self):
        # data = fourth_prediction.PREDICTION_DATA_MONTHLY_DICT
        KEY_WORD = list(self.data.keys())
        # keyword1, keyword2 = KEY_WORD[0], KEY_WORD[1]
        for keyword in KEY_WORD:
            # keyword1, keyword2 = list(self.data.keys())
            # k1_self.data = self.data[keyword1]
            # k1_pos_self.data = k1_self.data["POSITIVE"]
            # print(k1_pos_self.data.keys())
            # print(list(k1_pos_self.data.keys()))
            grouped_positive_arr_yrs = self.data[keyword]["POSITIVE"]
            grouped_negative_arr_yrs = self.data[keyword]["NEGATIVE"]
            grouped_neutral_arr_yrs = self.data[keyword]["NEUTRAL"]
            grouped_positive_arr_yrs_vals = list(grouped_positive_arr_yrs.values())
            grouped_negative_arr_yrs_vals = list(grouped_negative_arr_yrs.values())
            grouped_neutral_arr_yrs_vals = list(grouped_neutral_arr_yrs.values())

            pos_percent, neg_percent, neu_percent = self.array_to_percentage(grouped_positive_arr_yrs_vals, grouped_negative_arr_yrs_vals, grouped_neutral_arr_yrs_vals)
            # print(pos_percent)
            # print(neg_percent)
            # print(neu_percent)
            # exit()
            # x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            x = list(grouped_positive_arr_yrs.keys())
            # print(x)
            # x = ["Jan", "Feb","Mar", "Apr", "May", "June","July", "Aug", "Sep", "Oct", "Nov", "Dec"]
            y = [pos_percent, neg_percent, neu_percent]
            labels=['POSITIVE', 'NEGATIVE', 'NEUTRAL']
            lines=[('r','-'),('g','-.'),('b',':')]
            fig = plt1.gcf()
            fig.canvas.set_window_title('Yearly Sentiments')
            if(KEY_WORD.index(keyword) == 0):
                plt1.subplot(2,1,1)
            else:
                plt1.subplot(2,1,2)
            # loop over self.data, labels and colors
            for i in range(len(y)):
                plt1.plot(x,y[i],color=lines[i][0],linestyle=lines[i][1],label=labels[i])
            plt1.title("Yearly Sentiment for " + keyword)
            plt1.xlabel("Years")
            plt1.ylabel("Sentiments in Percent")
            plt1.legend()
            plt1.tight_layout()
        plt1.show()


    def array_to_percentage(self,pos, neg, neu):
        # print(pos)
        # print(neg)
        # print(neu)
        ar_size = len(pos)
        print("****************************")
        pos_percent = [0]*ar_size
        neg_percent = [0]*ar_size
        neu_percent = [0]*ar_size
        # print(pos_percent)
        # print(neg_percent)
        # print(neu_percent)
        for i in range(0,ar_size):
            # print("i = ", i)
            total_i = pos[i] + neg[i]+neu[i]
            if(total_i>0):
                pos_percent[i] = pos[i]*100/total_i
                neg_percent[i] = neg[i]*100/total_i
                neu_percent[i] = neu[i]*100/total_i
            else:
                pos_percent[i] = 0
                neg_percent[i] = 0
                neu_percent[i] = 0
        print("*******************************")
        # print(pos_percent)
        # print(neg_percent)
        # print(neu_percent)
        return pos_percent, neg_percent, neu_percent

if __name__ == '__main__':
    # data = {'amazon': {'POSITIVE': {2018:2, 2019: 38}, 'NEGATIVE': {2019: 4}, 'NEUTRAL': {2019: 7}}, 'google': {'POSITIVE': {2018:5, 2019: 17}, 'NEGATIVE': {2019: 9}, 'NEUTRAL': {2019: 23}}}
    # visualization_sentiment_yearly().start(data)
    visualization_sentiment_accuracy().start()
