# Colin Brown
# Python script to scrape twitter data from @WesternWeightRm about how busy the weight room is
# Using tweety-ns

from tweety.exceptions import ActionRequired, RateLimitReached
from tweety import Twitter

f = open("output.csv", 'w')  # Open and clear output.csv
tweetsCSVText = ""  # Will hold each pages scraped information

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
# all_tweets = app.get_tweets("WesternWeightRm", 1, False, 2, 'DAABCgABGP-hVAG__GMKAAIYymPTvtdg4AgAAwAAAAIAAA') # Get specified twitter page with cursor
lastTweets = ""  # Hold the previous all_tweets value
tweetsCount = 0;

for times in range(0, 100):  # Get x number of twitter pages
    tweetsCount += len(all_tweets.tweets)
    for tweet in all_tweets:  # Process each tweet on page (usually 20 of them)
        tweetTxt = tweet.text.lower()  # The text of the tweet
        indexStart = 0  # Index of "WR"
        if "wr" not in tweetTxt:  # Tweet does not have "wr"
            print("Could not find \'WR\' - Skipping tweet on  " + str(tweet.date) + ": " + tweetTxt + "\n\n")
            break
        else:  # Get index of "wr"
            indexStart = tweetTxt.index("wr")
        if tweetTxt[indexStart + 2] == " ":  # tweet is format "WR 12" (has space)
            indexStart += 3
        else:  # tweet is format "WR12" (no space)
            indexStart += 2

        indexEnd = tweetTxt.index("\n", indexStart)  # Get the index of the end of the "wr" line
        num = tweetTxt[indexStart:indexEnd] + 'a'  # Get the WR value, some emojis didn't process properly, adding a character to end fixed
        for x in range(0, len(num)):  # Remove the emoji(s)
            if not num[x].isnumeric():
                num = num[0:x]
                break

        tweetsCSVText += str(tweet.date) + ", " + num + "\n"  # Save the tweet data to string
    f.write(tweetsCSVText)  # Write the last page to csv file
    tweetsCSVText = ""  # Reset string for next page
    if not all_tweets.is_next_page:
        print("No pages left")

    try:
        if len(all_tweets) > 0:
            print("Requesting page " + str(times + 2) + " around date " + str(
                all_tweets.tweets[(len(all_tweets.tweets) - 1)].date) + " with cursor: " + all_tweets.cursor)
        else:
            print("Page " + str(times + 1) + " had no tweets, requesting page " + str(times + 2) + " with cursor: " + all_tweets.cursor)
        lastTweets = all_tweets  # Save tweet page
        all_tweets = app.get_tweets("WesternWeightRm", 1, False, 2, all_tweets.cursor)  # Get next page of tweets
    except RateLimitReached as e:  # RateLimit reached error with twitter (BRING BACK FREE API USAGE)
        print("\nOn twitter request " + str(times + 2) + ": " + e.message + "Was able to collect " + str(
            tweetsCount) + " tweets\nThe last cursor for next tweets (also written to next_cursor.txt, may reread up to 20 repeat tweets):" + lastTweets.cursor)
        g = open("next_cursor.txt", 'w')
        g.write("Last cursor: " + lastTweets.cursor + "\ncursor_top: " + lastTweets.cursor_top)  # Save cursor info to file
        g.close()
        break

f.close()
