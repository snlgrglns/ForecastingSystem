import pylab as plt1
import numpy as np

class visualization_prediction():
    def __init__(self, data):
        self.data = data

    def valueGraph(self):
        # KEY_WORD = ["google", "amazon"]
        # data = {
        #     'amazon': {'LR': ['Logistic Regression', 4.899856090545654, 0.3333333333333333], 'NB': ['Naive Bayes', 1.316478967666626, 0.3333333333333333], 'RF': ['Random Forest', 3.464771270751953, 0.3333333333333333]},
        #     'google': {'LR': ['Logistic Regression', 4.69430947303772, 1.0], 'NB': ['Naive Bayes', 1.6614549160003662, 1.0], 'RF': ['Random Forest', 3.3550236225128174, 1.0]}
        # }
        # # data = fourth_prediction.PREDICTION_DICT
        KEY_WORD = list(self.data.keys())
        kw1, kw2 = KEY_WORD[0], KEY_WORD[1]
        kw1_pred_arr = [self.data[kw1]['LR'][2], self.data[kw1]['NB'][2], self.data[kw1]['RF'][2]]
        kw2_pred_arr = [self.data[kw2]['LR'][2], self.data[kw2]['NB'][2], self.data[kw2]['RF'][2]]
        sub_names_arr = [self.data[kw2]['LR'][0], self.data[kw2]['NB'][0], self.data[kw2]['RF'][0]]
        # positive_accuracy_arr = [self.data[kw1]['AP'], self.data[kw2]['AP']]
        print(kw1_pred_arr)
        print(kw2_pred_arr)
        print(sub_names_arr)
        print(self.data)
        # exit()
        N = 3
        ind = np.arange(N)  # the x locations for the groups
        width = 0.27       # the width of the bars

        fig = plt1.figure()
        ax = fig.add_subplot(111)

        yvals = kw1_pred_arr
        rects1 = ax.bar(ind, yvals, width, color='b')
        zvals = kw2_pred_arr
        rects2 = ax.bar(ind+width, zvals, width, color='g')

        # ax.set_ylabel('Prediction value 0 to 1')
        ax.set_xticks(ind+width)
        ax.set_xticklabels( sub_names_arr )
        ax.legend( (rects1[0], rects2[0]), (kw1, kw2) )

        def autolabel(rects):
            for rect in rects:
                h = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/2., 1*h, "{0:.2f}".format(h),
                        ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.canvas.set_window_title('Graph for Accuracy Prediction Value')
        plt1.title('Accuracy Prediction Value for ' + kw1 + " and " +kw2)
        plt1.xlabel("Classifiers")
        plt1.ylabel("Accuracy Prediction Value in Percentage")
        plt1.tight_layout()
        plt1.show()

    def timeGraph(self):
        # data = {
        #     'amazon': {'LR': ['Logistic Regression', 4.899856090545654, 0.3333333333333333], 'NB': ['Naive Bayes', 1.316478967666626, 0.3333333333333333], 'RF': ['Random Forest', 3.464771270751953, 0.3333333333333333]},
        #     'google': {'LR': ['Logistic Regression', 4.69430947303772, 1.0], 'NB': ['Naive Bayes', 1.6614549160003662, 1.0], 'RF': ['Random Forest', 3.3550236225128174, 1.0]}
        # }
        # self.data = fourth_prediction.PREDICTION_DICT
        KEY_WORD = list(self.data.keys())
        kw1, kw2 = KEY_WORD[0], KEY_WORD[1]
        kw1_times_arr = [self.data[kw1]['LR'][1], self.data[kw1]['NB'][1], self.data[kw1]['RF'][1]]
        kw2_times_arr = [self.data[kw2]['LR'][1], self.data[kw2]['NB'][1], self.data[kw2]['RF'][1]]
        sub_names_arr = [self.data[kw2]['LR'][0], self.data[kw2]['NB'][0], self.data[kw2]['RF'][0]]
        print(self.data)
        print(kw1_times_arr)
        print(kw2_times_arr)
        print(sub_names_arr)
        # exit()
        N = 3
        ind = np.arange(N)  # the x locations for the groups
        width = 0.27       # the width of the bars

        fig = plt1.figure()
        ax = fig.add_subplot(111)

        yvals = kw1_times_arr
        rects1 = ax.bar(ind, yvals, width, color='b')
        zvals = kw2_times_arr
        rects2 = ax.bar(ind+width, zvals, width, color='g')

        # ax.set_ylabel('Time in seconds')
        ax.set_xticks(ind+width)
        ax.set_xticklabels( sub_names_arr )
        ax.legend( (rects1[0], rects2[0]), (kw1, kw2) )

        def autolabel(rects):
            for rect in rects:
                h = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/2., 1*h, "{0:.2f}".format(h),
                        ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        fig.canvas.set_window_title('Graph for Accuracy Prediction Time')
        plt1.title('Accuracy Prediction Time for ' + kw1 + " and " +kw2)
        plt1.xlabel("Classifiers")
        plt1.ylabel("Accuracy Prediction time in seconds")
        plt1.tight_layout()
        plt1.show()

# visualization_prediction_time().start()
