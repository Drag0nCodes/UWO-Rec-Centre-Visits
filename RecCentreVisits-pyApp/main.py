# Colin Brown
# Python script to scrape twitter data from @WesternWeightRm about how busy the weight room is
# Using tweety-ns

from tweety.exceptions import ActionRequired, RateLimitReached
from tweety import Twitter
import re;
EASTERNTIMEOFFSET = -4
app = Twitter("session")  # Create a twitter session

# Sign in to new session
#try:
#    app.sign_in("username", "password")
#except ActionRequired as e:
#    action = input(f"Action Required :> {str(e.message)} : ")
#    app.sign_in("username", "password", extra=action)

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
    lastMonth = int(re.findall("-\d+-", lastDate)[0][1:-1])
    lastDay = int(re.findall("-\d+", lastDate)[1][1:])
    lastHour = int(re.findall("\d+:", lastDate)[0][:-1])
    lastWR = int(re.findall(",\d+", lastDate)[0][1:])
tweetsCSVText = ""  # Will hold each pages scraped information
tweetsCount = 0

for times in range(0, 4):  # Get x number of twitter pages
    for tweet in all_tweets:  # Process each tweet on page (usually 20 of them)
        tweetTxt = tweet.text.lower()  # The text of the tweet

        if "wr" not in tweetTxt:  # Tweet does not have "wr"
            print("Could not find \'WR\' - Skipping tweet on  " + str(tweet.date) + ": " + tweetTxt + "\n\n")
            break

        matches = re.findall("\d+", tweetTxt)  # Get all numbers
        num = matches[0]  # WR num should be the first number

        tweetDate = str(tweet.date)
        tweetMonth = int(re.findall("-\d+-", tweetDate)[0][1:-1])
        tweetDay = int(re.findall("-\d+", tweetDate)[1][1:])
        tweetHour = int(re.findall(" \d+", tweetDate)[0][1:3])  # Get hour of tweet

        if tweetHour < -EASTERNTIMEOFFSET:  # Account for stupid ETC to ET time conversions
            tweetDay -= 1
            if tweetDay < 0:
                tweetMonth -= 1
                tweetDay = 30
                if tweetMonth == 0:
                    tweetMonth = 12

        tweetHour = (tweetHour + EASTERNTIMEOFFSET) % 24  # Change tweets hour to eastern time

        if tweetMonth == lastMonth and tweetDay == lastDay and tweetHour == lastHour and int(num) == lastWR:  # Stop code when tweet is caught up
            print("Matching tweet with start of CSV file. \nNew tweet time:" + re.findall(" \d+:\d+", tweetDate)[0] + "/" + str(tweetHour) + re.findall(":\d+", tweetDate)[0] + "\nStart of CSV time:" + re.findall(" .+,", lastDate)[0][:-1] + "\nEnter 'S' to stop.")
            input1 = input().lower()
            if input1 == 's':
                stop = True
                break

        if tweetMonth <= lastMonth and tweetDay < lastDay:
            print("Got too many tweets, cleanup CSV file around " + str(lastMonth) + "-" + str(lastDay))
            stop = True
            break

        tweetDateNew = re.findall("\d+", tweetDate)[0] + "-" + str(tweetMonth).zfill(2) + "-" + str(tweetDay).zfill(2) + " " + str(tweetHour) + re.findall(":\d+:", tweetDate)[0][:-1]  # New format of date
        tweetsCSVText = tweetDateNew + "," + num + "\n" + tweetsCSVText  # Save the tweet data to start of string
        tweetsCount += 1

    if stop:
        print("Stopping")
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
