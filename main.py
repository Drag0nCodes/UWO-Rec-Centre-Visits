# Colin Brown
# Python script to scrape twitter data from @WesternWeightRm about how busy the weight room is
# Using tweety-ns

from tweety.exceptions import ActionRequired, RateLimitReached
from tweety import Twitter
from datetime import datetime
import pytz
import re
timezone = pytz.timezone('America/Toronto')
app = Twitter("session")  # Create a twitter session

# Sign in to new session

'''try:
    app.sign_in("drag0nonsteam@gmail.com", "BYTo85Qc*A&L3ht2")
except ActionRequired as e:
    action = input(f"Action Required :> {str(e.message)} : ")
    app.sign_in("drag0nonsteam@gmail.com", "BYTo85Qc*A&L3ht2", extra=action)
'''
# Sign in with previous session
app.connect()

print("Requesting page 1")
all_tweets = app.get_tweets("WesternWeightRm")  # Get first twitter page
lastTweets = ""  # Hold the previous all_tweets value
tweetsCount = 0;
stop = False
first = True

f = open("Output.csv", 'a+')  # Open for read write output.csv
f.seek(0, 2)
if f.tell() != 0:
    f.seek(f.tell() - 1)  # Move pointer one character back
    lastDate = ""
    while f.tell() > 0:  # Get last line
        f.seek(f.tell() - 2)  # Move pointer one character back
        char = f.read(1)
        if char == "\n":  # Newline character found
            break

# Read the last line
lastDate = f.readline()

f.seek(0, 2)
if lastDate is not None:  # Get info of last tweet in CSV file
    lastWR = int(re.findall(r",\d+", lastDate)[0][1:])  # Last WR val
    lastDate = re.findall(".+,", lastDate)[0][:-1]
    last_datetime = datetime.strptime(lastDate, '%Y-%m-%d %H:%M')
    last_datetime = timezone.localize(last_datetime)  # last tweet date in Toronto time zone
tweetsCSVText = ""  # Will hold each pages scraped information
tweetsCount = 0

for times in range(0, 100):  # Get x number of twitter pages
    for tweet in all_tweets:  # Process each tweet on page (usually 20 of them)
        tweetTxt = tweet.text.lower()  # The text of the tweet
        lines = tweetTxt.splitlines()  # lines of the tweet
        
        tweetDate = re.findall(r".+:\d+:", str(tweet.date))[0][:-1]  # Date and time from tweet
        utc_datetime = datetime.strptime(tweetDate, '%Y-%m-%d %H:%M')  # Make date and time into a datetime obj
        local_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(timezone)  # Change it from UTC to Toronto time (ET)

        # Get the line that has with "wr" in it
        wr_line = next((line for line in lines if "3wr" or "wr3" or "wr" in line), None)

        if wr_line is None:
            print("Could not find \'WR\' or \'WR3\' - Skipping tweet on " + str(local_datetime) + ": " + tweetTxt + "\n\n")
            continue

        if (re.findall(r"\d+", wr_line)):
            num = re.findall(r"\d+", wr_line)[-1]  # Get wr value
        else: 
            print("Could not find number value in tweet - Skipping tweet on " + str(local_datetime) + ": " + tweetTxt + "\n\n")

        if last_datetime == local_datetime and lastWR == int(num):  # Stop code when tweet is caught up
            print("Caught up to newest tweet already in Output.csv")
            stop = True
            break

        if last_datetime > local_datetime:  # In case there is some error where the previous if statement doesn't stop the code, this will stop the tweet if the new tweet is from before the oldest tweet previously processed
            print("Stopping due to error.\nGot a tweet before the last Output.csv line.\nDouble check output around new tweet time: " + local_datetime.strftime('%Y-%m-%d %H:%M') + " and previous tweet time: " + last_datetime.strftime('%Y-%m-%d %H:%M'))
            stop = True
            break

        tweetsCSVText = local_datetime.strftime('%Y-%m-%d %H:%M,') + num + "\n" + tweetsCSVText  # Save the tweet data to start of string
        tweetsCount += 1

    if stop:
        break

    if not all_tweets.is_next_page:
        print("No pages left")

    try:
        if len(all_tweets) > 0:
            print("Requesting page " + str(times + 2) + " around date " + str(
                all_tweets.tweets[(len(all_tweets.tweets) - 1)].date) + " with cursor: " + all_tweets.cursor)
        else:
            print("Page " + str(times + 1) + " had no tweets, requesting page " + str(times + 2) + " with cursor: " + all_tweets.cursor)
        all_tweets = app.get_tweets("WesternWeightRm", 1, False, 2, all_tweets.cursor)  # Get next page of tweets
    except RateLimitReached as e:  # RateLimit reached error with twitter (BRING BACK FREE API USAGE)
        print("\nOn twitter request " + str(times + 2) + ": " + e.message)
        break

f.write(tweetsCSVText)
print("Added " + str(tweetsCount) + " new data points to Output.csv")
f.close()
