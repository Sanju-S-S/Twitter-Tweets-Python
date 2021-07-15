
import tweepy
import mysql.connector
from datetime import datetime, timedelta, timezone

from tweepy.api import API

consumer_key = 'WtKaPVLLVrYJno8vd4Y1Dv2FN'
consumer_secret = 'tzSoZ5pOFjECpZXeFYEmjZ1mebfsMggIE7S92Cw8RkuPzpQaEA'
access_token = '1291127568-HkeW484LnDkOAZoST03hDwZHPSLru39FE61wjct'
access_secret = 'EUMW5YHR3jW3unFgn39DNTRaHbcYAq7zSjh4CsaDyp8ZL'

tweetsPerQry = 100
maxTweets = 1000000
hashtag = "#mencatatindonesia"

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="twitter_db"
)

authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_secret)
api = tweepy.API(authentication, wait_on_rate_limit=True)
maxId = -1
tweetCount = 0
while tweetCount < maxTweets:
    if(maxId <= 0):
	    newTweets = API.search(q=hashtag, count=tweetsPerQry, result_type="recent", tweet_mode="extended")
    else:
        newTweets = API.search(q=hashtag, count=tweetsPerQry, max_id=str(maxId - 1), result_type="recent", tweet_mode="extended")

    if not newTweets:
	    print("Tweet Habis")
	    break

    val = []
    for tweet in newTweets:
        id = tweet.id
        id = str(id)
        created_at = tweet.created_at
        text = tweet.full_text.encode('utf-8')
        source = tweet.source
        username = tweet.user.name
        user_description = tweet.user.description 
        print(str(id)+":"+str(text)+"\n\n")

    mycursor = mydb.cursor()
    sql = '''
        INSERT INTO tweet (created_at, tweet_id, text, source, user_name, user_description) 
        VALUES (%s,%s,%s,%s,%s,%s) '''
    mycursor.executemany(sql, val)
    mydb.commit()
    tweetCount += len(newTweets)	
    maxId = newTweets[-1].id

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="root",
database="twitter_db"
)
mycursor = mydb.cursor()
print("Enter the Keyword needs to be Searched:")
keyword=input()
mycursor.execute("SELECT * FROM tweet where text="+keyword)
myresult = mycursor.fetchall()
for x in myresult:
  print(x)