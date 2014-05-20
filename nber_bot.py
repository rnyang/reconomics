# NBER Bot
# Ron Yang 2014
#
# Grabs each week's NBER working papers from RSS
# and posts each paper to reddit.com/r/economics
# at a fixed interval over the week

# External Libraries
import time
import sys

# Feedparser: RSS Feeds
import feedparser

# Praw: Reddit API
import praw

# 1. Setup

feed_url = "http://www.nber.org/rss/new.xml"
feed = feedparser.parse(feed_url)
latest_article = None
queue = []

user_agent = 'USER AGENT'
uname = 'NBER BOT'
pw = 'NBER BOT PASS'

r = praw.Reddit(user_agent=user_agent)
r.login(uname, pw)

# 2. Loop
while True:
    
    # 2.1 Initialize Loop
    if latest_article == None:
        latest_article = feed["items"][0]["title"]

    # 2.2 Check for new items and add them to queue
    if feed["items"][0]["title"] != latest_article:
        # If there are new articles
        for i in xrange(0, len(feed["items"])):
            next_article = feed["items"][i]["title"]

            # If the next 
            if next_article != latest_article:
                print "processing", next_article
                queue.append(feed["items"][i])

            # If we hit our old latest article
            if next_article == latest_article:
                print 'exhausted all new articles'
                break

        # update latest article to top of rss feed
        latest_article = feed["items"][0]["title"]

    # 2.3 Sleep!

    # Every 10 seconds (testing only)
    # time.sleep(10)

    # Every 4 Hours
    time.sleep(4*60*60)

    # 2.4 Post Links from Queue
    try:
        # Get new post
        curr_post = queue.pop()

        print "Posting ", curr_post['title']

        # Format and submit the post
        textbody = curr_post['summary'] + '\n\n\n' + curr_post['link']
        title = "NBER:" + curr_post['title']

        r.submit('reddit_api_test', title, text=textbody)
        
    except:
        print "No New Posts!"



