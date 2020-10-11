import tkinter as tk
from tkinter import *
from visualization_clean import *
from visualization_sentiment import *
from visualization_prediction import *

class fifth_visualization_menu():
    def __init__(self, clean_time_data, sentiment_data, accuracy_prediction_data, monthly_data, yearly_data):
        self.clean_time_data = clean_time_data
        self.sentiment_data = sentiment_data
        self.accuracy_prediction_data = accuracy_prediction_data
        self.monthly_data = monthly_data
        self.yearly_data = yearly_data
    def create_window(self):
        root = tk.Tk()
        window = tk.Toplevel(root)

    def main(self):
        root = tk.Tk()
#	root.lift()
        root.title("Sales Forecast Graph Visualization")
        tk.Button(root, text="Data Clean Time", command=visualization_clean_time(self.clean_time_data).start).grid(row=0,padx=(10, 10), pady=(10,10), sticky='EW')
        tk.Button(root, text="Overall Sentiment Analysis Time", command=visualization_sentiment_time(self.sentiment_data).start).grid(row=1,padx=(10, 10), pady=(10,10), sticky='EW')
        tk.Button(root, text="Overall Sentiment Analysis", command=visualization_sentiment_accuracy(self.sentiment_data).start).grid(row=2,padx=(10, 10), pady=(10,10), sticky='EW')
        tk.Button(root, text="Monthly Sentiment", command=visualization_sentiment_monthly(self.monthly_data).start).grid(row=3,padx=(10, 10), pady=(10,10), sticky='EW')
        tk.Button(root, text="Yearly Sentiment", command=visualization_sentiment_yearly(self.yearly_data).start).grid(row=4,padx=(10, 10), pady=(10,10), sticky='EW')
        tk.Button(root, text="Prediction Accuracy Time", command=visualization_prediction(self.accuracy_prediction_data).timeGraph).grid(row=5,padx=(10, 10), pady=(10,10), sticky='EW')
        tk.Button(root, text="Prediction Accuracy Analysis", command=visualization_prediction(self.accuracy_prediction_data).valueGraph).grid(row=6,padx=(10, 10), pady=(10,10), sticky='EW')
        mainloop()
# b.pack()
# if __name__ == '__main__':
#     fifth_visualization_menu().main()
