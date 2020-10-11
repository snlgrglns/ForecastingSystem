import findspark
findspark.init('C:/spark/spark-2.4.0-bin-hadoop2.7')
#findspark.init('spark-2.4.0-bin-hadoop2.7')
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.ml.feature import HashingTF, Tokenizer, IDF, StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.classification import NaiveBayes, RandomForestClassifier, LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import time, threading
class fourth_prediction():
    PREDICTION_DICT = {}  # {"classifier short keyword": ["Classifier Name Full","time", "prediction"]}
    PREDICTION_DATA_MONTHLY_DICT = {}
    PREDICTION_DATA_YEARLY_DICT = {}
    def __init__(self):
        self.SC =SparkContext()
        self.SQL_CONTEXT = SQLContext(self.SC)

    def start(self, key_word_file_names):
        # files = ["sad", "happy"]
        # files = first_data_scrapping().KEY_WORDS
        # file2 = "happy.csv"
        th1 = threading.Thread(name='prediction1', target=self.file_process, args=(key_word_file_names[0], ))
        th2 = threading.Thread(name='prediction2', target=self.file_process, args=(key_word_file_names[1], ))
        th1.start()
        th2.start()
        th1.join()
        th2.join()
        # self.PREDICTION_DATA_FRAMES
        return self.PREDICTION_DICT, self.PREDICTION_DATA_MONTHLY_DICT, self.PREDICTION_DATA_YEARLY_DICT

    def file_process(self, key_word):
        try:
            file_name = "sentiment_"+key_word+".csv"
            data = self.SQL_CONTEXT.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(file_name)
            data = data.dropna() #drop Rows/Columns with Null values in different ways
            tokenizer = Tokenizer(inputCol="text", outputCol="words")
            hashtf = HashingTF(numFeatures=2**16, inputCol="words", outputCol='tf')
            idf = IDF(inputCol='tf', outputCol="features", minDocFreq=5) #minDocFreq: remove sparse terms
            label_stringIdx = StringIndexer(inputCol = "sentiment", outputCol = "label")
            pipeline = Pipeline(stages=[tokenizer, hashtf, idf, label_stringIdx])
            # # Fit the pipeline to training documents.
            pipelineFit = pipeline.fit(data)
            dataset = pipelineFit.transform(data)
            dataset.show(5)
            print("Splitting [" + key_word + "] dataset into training and test set in the ratio 7:3")
            (trainingData, testData) = dataset.randomSplit([0.7, 0.3], seed = 100)
            print("[" + key_word + "] Training Dataset Rows: " + str(trainingData.count()))
            print("[" + key_word + "] Test Dataset Rows: " + str(testData.count()))
            print("###########################[" + key_word + "] Starting Prediction using Logistic Regression ##############################################")
            time.sleep(2)
            start_time_LR = time.time()
            lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
            lrModel = lr.fit(trainingData)
            predictions = lrModel.transform(testData)
            predictions.filter(predictions['prediction'] == 0) \
                .select("text","sentiment","negative","positive","label", "probability", "prediction") \
                .orderBy("sentiment", ascending=False) \
                .show(n = 10, truncate = 30)
            # accuracy_LR = predictions.filter(predictions.label == predictions.prediction).count() / float(testData.count())
            evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
            predn_LR=evaluator.evaluate(predictions)*100
            # print("accuracy_LR"+str(accuracy_LR))
            end_time_LR = time.time()
            elapse_time_LR = end_time_LR-start_time_LR
            print("[" + key_word + "] Logistic Regression Prediction: "+str(predn_LR))
            print("[" + key_word + "] Logistic Regression elapse time: "+str(elapse_time_LR))
            print("###########################[" + key_word + "] Completed Prediction using Logistic Regression ##############################################")

            print("###########################[" + key_word + "] Starting Prediction using Naive Bayes ##############################################")
            time.sleep(2)
            start_time_NB = time.time()
            nb = NaiveBayes(smoothing=1)
            model = nb.fit(trainingData)
            predictions = model.transform(testData)
            predictions.filter(predictions['prediction'] == 0) \
                .select("text","sentiment","negative","positive","label", "probability", "prediction") \
                .orderBy("probability", ascending=False) \
                .show(n = 10, truncate = 30)
            # accuracy_NB = predictions.filter(predictions.label == predictions.prediction).count() / float(testData.count())
            evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
            predn_NB=evaluator.evaluate(predictions)*100
            # print("accuracy_NB"+str(accuracy_NB))
            end_time_NB = time.time()
            elapse_time_NB = end_time_NB-start_time_NB
            print("[" + key_word + "] Naive Bayes Prediction: "+str(predn_NB))
            print("[" + key_word + "] Naive Bayes Elapse Time: "+str(elapse_time_NB))
            print("###########################[" + key_word + "] Completed Prediction using Naive Bayes ##############################################")
            print("###########################[" + key_word + "] Starting Prediction using Random Forest ##############################################")
            time.sleep(2)
            start_time_RF = time.time()
            rf = RandomForestClassifier(labelCol="label", \
                                        featuresCol="features", \
                                        numTrees = 100, \
                                        maxDepth = 4, \
                                        maxBins = 32)
            # Train model with Training Data
            rfModel = rf.fit(trainingData)
            predictions = rfModel.transform(testData)
            predictions.filter(predictions['prediction'] == 0) \
                .select("text","sentiment","negative","positive","label", "probability", "rawPrediction", "prediction") \
                .orderBy("probability", ascending=False) \
                .show(n = 10, truncate = 30)
            # accuracy_RF = predictions.filter(predictions.label == predictions.prediction).count() / float(testData.count())
            evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
            predn_RF = evaluator.evaluate(predictions)*100
            end_time_RF = time.time()
            elapse_time_RF = end_time_RF - start_time_RF
            # print("accuracy_RF"+str(accuracy_RF))
            print("[" + key_word + "] Random Forest Prediction: "+str(predn_RF))
            print("[" + key_word + "] Random Forest Elapse Time: "+str(elapse_time_RF))
            print("###########################[" + key_word + "] Completed Prediction using Random Forest ##############################################")
            # fourth_prediction.PREDICTION_DICT[key_word].append({
            #             "LR" : ["Logistic Regression", elapse_time_LR, predn_LR],
            #             "NB" : ["Naive Bayes", elapse_time_NB, predn_NB],
            #             "RF" : ["Random Forest", elapse_time_RF, predn_RF],
            #         })
            fourth_prediction.PREDICTION_DICT[key_word] = {
                "LR" : ["Logistic Regression", elapse_time_LR, predn_LR],
                "NB" : ["Naive Bayes", elapse_time_NB, predn_NB],
                "RF" : ["Random Forest", elapse_time_RF, predn_RF],
            }
            sentiment_dataframe_monthly = data.groupBy("month","sentiment") \
                .count()\
                .orderBy("month") #\
            grouped_positive_arr_mnth, grouped_negative_arr_mnth, grouped_neutral_arr_mnth = self.monthly_sentiment_dataframe_to_arrays(sentiment_dataframe_monthly)
            fourth_prediction.PREDICTION_DATA_MONTHLY_DICT[key_word] = {
                "POSITIVE":grouped_positive_arr_mnth,
                "NEGATIVE":grouped_negative_arr_mnth,
                "NEUTRAL":grouped_neutral_arr_mnth
            }
            sentiment_dataframe_yearly = data.groupBy("year","sentiment") \
                .count()\
                .orderBy("year")
            # print(sentiment_dataframe_yearly.count())
            sentiment_dataframe_yearly.show()
            grouped_positive_arr_yr, grouped_negative_arr_yr, grouped_neutral_arr_yr = self.yearly_sentiment_dataframe_to_arrays(sentiment_dataframe_yearly)
            fourth_prediction.PREDICTION_DATA_YEARLY_DICT[key_word] = {
                "POSITIVE":grouped_positive_arr_yr,
                "NEGATIVE":grouped_negative_arr_yr,
                "NEUTRAL":grouped_neutral_arr_yr
            }
                # print(fourth_prediction.PREDICTION_DICT)
        except Exception as ex:
            print(ex)

    def monthly_sentiment_dataframe_to_arrays(self, filtered_df):
        pos_arr=[0]*12
        neg_arr=[0]*12
        neu_arr=[0]*12
        for df_row in filtered_df.rdd.collect():
            df_sentiment = df_row["sentiment"]
            df_month = df_row['month']
            if(df_sentiment=="POSITIVE"):
                pos_arr[df_month-1] = df_row['count']
            elif(df_sentiment=="NEGATIVE"):
                neg_arr[df_month-1] = df_row['count']
            else:
                neu_arr[df_month-1] = df_row['count']
        return pos_arr, neg_arr, neu_arr

    def yearly_sentiment_dataframe_to_arrays(self, filtered_df):
        size_df = filtered_df.count()
        year_first = filtered_df.rdd.collect()[0]["year"]
        year_last = filtered_df.rdd.collect()[size_df-1]["year"]
        # print(year_first)
        # print(year_last)
        pos_arr={}
        neg_arr={}
        neu_arr={}
        for year in range(year_first-1, year_last+2):
            pos_arr[year] = 0
            neg_arr[year] = 0
            neu_arr[year] = 0
        for df_row in filtered_df.rdd.collect():
            df_sentiment = df_row["sentiment"]
            df_year = df_row['year']
            if(df_sentiment=="POSITIVE"):
                pos_arr[df_year] = df_row['count']
            elif(df_sentiment=="NEGATIVE"):
                neg_arr[df_year] = df_row['count']
            else:
                neu_arr[df_year] = df_row['count']
        return pos_arr, neg_arr, neu_arr
if __name__ == '__main__':
    files = ["adidas", "nike"]
    sdc = fourth_prediction().start(files)
    time.sleep(2)
    print(fourth_prediction.PREDICTION_DICT)
    print("["+files[0]+"] Logistic Regression Time: ", fourth_prediction.PREDICTION_DICT[files[0]]["LR"][1])
    print("["+files[1]+"] Logistic Regression Time: ", fourth_prediction.PREDICTION_DICT[files[1]]["LR"][1])
    print("["+files[0]+"] Naive Bayes Time: ", fourth_prediction.PREDICTION_DICT[files[0]]["NB"][1])
    print("["+files[1]+"] Naive Bayes Time: ", fourth_prediction.PREDICTION_DICT[files[1]]["NB"][1])
    print("["+files[0]+"] Random Forest Time: ", fourth_prediction.PREDICTION_DICT[files[0]]["RF"][1])
    print("["+files[1]+"] Random Forest Time: ", fourth_prediction.PREDICTION_DICT[files[1]]["RF"][1])
    print("["+files[0]+"] Logistic Regression Accuracy: ", fourth_prediction.PREDICTION_DICT[files[0]]["LR"][2])
    print("["+files[1]+"] Logistic Regression Accuracy: ", fourth_prediction.PREDICTION_DICT[files[1]]["LR"][2])
    print("["+files[0]+"] Naive Bayes Accuracy: ", fourth_prediction.PREDICTION_DICT[files[0]]["NB"][2])
    print("["+files[1]+"] Naive Bayes Accuracy: ", fourth_prediction.PREDICTION_DICT[files[1]]["NB"][2])
    print("["+files[0]+"] Random Forest Accuracy: ", fourth_prediction.PREDICTION_DICT[files[0]]["RF"][2])
    print("["+files[1]+"] Random Forest Accuracy: ", fourth_prediction.PREDICTION_DICT[files[1]]["RF"][2])
    # print(fourth_prediction.PREDICTION_DATA_FRAMES)
    # exit()
    # abcv = visualization_sentiment()
    # visualization_sentiment().tttt(fourth_prediction.PREDICTION_DATA_MONTHLY_DICT)
    # visualization_sentiment().tttt()
    # data = fourth_prediction.PREDICTION_DATA_FRAMES["google"]
    # positive = data.filter("sentiment='POSITIVE'")
    # positive.groupBy("month","sentiment") \
    #         .count()\
    #         .orderBy("month") \
    #         .show()
        # print("["+key_word+"]")
    #print(fourth_prediction.PREDICTION_DICT[files[0]])
    #print(fourth_prediction.PREDICTION_DICT[files[1]])
