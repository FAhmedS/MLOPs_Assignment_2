import time
import json
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

"# -- coding: utf-8 --"

app = Flask(__name__)

def calctime(a):
    return time.time()-a

positive=0
negative=0
compound=0

count=0
initime=time.time()
plt.ion()

import test

ckey=test.ckey
csecret=test.csecret
atoken=test.atoken
asecret=test.asecret

class listener(StreamListener):
    
    def on_data(self,data):
        global initime
        t=int(calctime(initime))
        all_data=json.loads(data)
        tweet=all_data["text"].encode("utf-8")
        tweet=" ".join(re.findall("[a-zA-Z]+", tweet))
        blob=TextBlob(tweet.strip())

        global positive
        global negative     
        global compound  
        global count
        
        count=count+1
        senti=0
        for sen in blob.sentences:
            senti=senti+sen.sentiment.polarity
            if sen.sentiment.polarity >= 0:
                positive=positive+sen.sentiment.polarity   
            else:
                negative=negative+sen.sentiment.polarity  
        compound=compound+senti        
        print count
        print tweet.strip()
        print senti
        print t
        print str(positive) + ' ' + str(negative) + ' ' + str(compound) 
        
    
        plt.axis([ 0, 70, -20,20])
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([t],[positive],'go',[t] ,[negative],'ro',[t],[compound],'bo')
        plt.show()
        plt.pause(0.0001)
        if count==200:
            return False
        else:
            return True
        
    def on_error(self,status):
        print status


auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

twitterStream=  Stream(auth, listener(count))
twitterStream.filter(track=["Donald Trump"])


@app.route('/')
def index():
    return render_template('live.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        key_word = request.form['key_word']
        tweets = api.search(key_word, count=100)
        pos = 0
        neg = 0
        for tweet in tweets:
            analysis = TextBlob(tweet.text)
            if analysis.sentiment.polarity >= 0:
                pos += 1
            else:
                neg += 1
        if pos > neg:
            sentiment = 'Positive'
        elif neg > pos:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        return render_template('predict.html', key_word=key_word, sentiment=sentiment)
    else:
        return render_template('predict.html')


if __name__ == '__main__':
    app.run(debug=True)
