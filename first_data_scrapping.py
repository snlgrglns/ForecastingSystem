import threading
import time
import GetOldTweets3 as got
import csv

class first_data_scrapping():
    def __init__(self):
        self.TWEET_COUNT=0
        self.MAX_TWEET = 50   #it pulls one tweet less
        self.DATE_SINCE = "2019-01-01"
        self.DATE_UNTIL = "2019-05-14"
        self.KEY_WORDS = []


    # MAX_TWEET_2 = MAX_TWEET_1
    def run_scrap(self, keyword):

        self.KEY_WORDS.clear()
        # product1 = input("Please enter first product:").strip()
        # while not product1:
        #     product1 = input("Empty!!! Please enter first product:").strip()
        #
        # product2 = input("Please enter second product:").strip()
        # while not product2:
        #     product2 = input("Empty!!! Please enter second product:").strip()

        # self.KEY_WORDS = [product1, product2]
        self.KEY_WORDS = keyword
        th1 = threading.Thread(name='product1', target=self.get_tweets, args=(self.KEY_WORDS[0], ))
        th2 = threading.Thread(name='product2', target=self.get_tweets, args=(self.KEY_WORDS[1], ))
        th3 = threading.Thread(name='progress', target=self.progress)
        th3.start()
        th1.start()
        th2.start()
        th3.join()
        return self.KEY_WORDS

    def get_tweets(self, searchString):
            with open(searchString+'.csv', 'w', newline='') as csvfile:
                fieldnames = ['id', 'text', 'date']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                tweetCriteria = got.manager.TweetCriteria().setQuerySearch(searchString).setUntil(self.DATE_UNTIL).setSince(self.DATE_SINCE).setMaxTweets(self.MAX_TWEET)
                for i in range(0, self.MAX_TWEET-1):
                    self.TWEET_COUNT = self.TWEET_COUNT + 1
                    tweet = got.manager.TweetManager.getTweets(tweetCriteria)[i]
                    id = tweet.id.encode("utf-8")
                    text = tweet.text.encode("utf-8")
                    date = tweet.date
                    writer.writerow({'id':id, 'text':text, 'date':date})
                    # print(tweets.text)
                # print("Scrapping completed for keyword \"" + searchString +"\" " )
            print("")

    def progress(self):
        flag = True
        while flag:
            fetched_percent = (self.TWEET_COUNT/((self.MAX_TWEET-1)*2)*100)
            time.sleep(5)
            print("\r Data Scrapping = {0:.4f}".format(fetched_percent) + "%", end=" ")
            if(fetched_percent==100):
                flag = False
# test_thread().enter_products()
if __name__ == '__main__':
	first_data_scrapping().run_scrap(["adidas","nike"])
