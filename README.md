# ForecastingSystem
Materials and Methods
  - Data collection
  - Data preparation and cleaning
Sentiment analysis
Accuracy Prediction using PySpark
  - Naïve Bayes
  - Random Forest Classifier
  - Logistic Regression
Results/Visualization/Graphs

# Requirements
Setup Hadoop in local machine. And following are the python library used
GetOldTweets3==0.0.9 <br />
pandas==0.24.2 <br />
bs4==4.7.1 <br />
nltk==3.4 <br />
findspark==1.3.0 <br />
pyspark==2.4.1 <br />
tkinter==8.6 <br />
matplotlib==2.2.2 <br />
numpy==1.14.3 <br />

# To run the project
1. To define the amount of data to be fetched, in first_data_scrapping.py, change the value of self.MAX_TWEET = 5000 (in line number = 9)
2. Similarly, to change the start date and end date, in first_data_scrapping.py, change the value. (in line number 10 and 11)
3. Then, setup hadoop and give provide hadoop path in fouth_prediction.py, line 2
4. To run the program, run the ui_menu.py file.

