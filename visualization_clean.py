import pylab as plt1
import numpy as np

class visualization_clean_time():
    def __init__(self, data):
        self.data = data

    def start(self):
        # data = {'amazon': {'time': 0.009972810745239258}, 'google': {'time': 0.02397322654724121}}
        # data = second_data_clean.CLEAN_DICT
        KEY_WORD = list(self.data.keys())
        x = np.arange(2)
        kw1, kw2 = KEY_WORD[0], KEY_WORD[1]
        times_arr = [self.data[kw1]['time'], self.data[kw2]['time']]
        fig, ax = plt1.subplots()
        for i, v in enumerate(times_arr):
            ax.text(i, v, " "+"{0:.4f}".format(v) + " secs", color='black', va='center', fontweight='bold')
        fig.canvas.set_window_title('Graph Tweet Clean Time')
        ax.set_xlabel('Key Words')
        ax.set_ylabel('Time in seconds')
        plt1.title('Tweet Clean Time for ' + kw1 + " and " +kw2)
        plt1.bar(x, times_arr)
        plt1.xticks(x, (kw1, kw2))
        plt1.tight_layout()
        plt1.show()

# visualization_clean_time().start()
