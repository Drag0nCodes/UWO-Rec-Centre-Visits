# UWO-Rec-Centre-Visits

This is a simple script to scrape the twitter post data from @WesternWeightRm and an excel spreadsheet to manage the data. 

# Background

@WesternWeightRm posts how many people are in the weight room every half hour during their business hours. I wanted to see how busy they were on average for each hour and when was the best time for me to go. 

# Usage and info

The excel file Rec Centre.xlsx in the python folder has the best information on the busyness of the weight room. As twitter changed their API policy (thanks Elon Musk for nothing) I was having to use a third-party API, Tweety, to get the data, and was only able to get tweets going back ~42 days or ~850 tweets before I would recieve empty pages of tweets from Twitter. This data gave me a good starting point of info for May and the first half of June. I plan to, every month, run the script and update the spreadsheet with new data. 

# Depreciated code

The JS folder is mostly depreciated and useless as the third-party API I used, Rettiwt, seemed to have issues getting the second page of tweets, and I was only able to ever get the most recent 20 tweets from the given account.