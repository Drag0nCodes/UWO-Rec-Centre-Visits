# UWO-Rec-Centre-Visits

This is a simple script to scrape the twitter post data from @WesternWeightRm and an excel spreadsheet to manage the data. 

## Background

@WesternWeightRm posts how many people are in the weight room every half hour during their business hours. I wanted to see how busy they were on average for each hour and when was the best time for me to go. 

## Usage and info

The excel file Rec Centre.xlsx has the best information on the busyness of the weight room. As twitter changed their API policy (thanks a lot Elon) I was having to use a third-party API, [Tweety(-ns)](https://github.com/mahrtayyab/tweety), to get the data, and was only able to get tweets going back ~42 days or ~850 tweets before I would receive empty pages of tweets from Twitter. This initial data gave me a good starting point of data starting May 2nd 2024. I plan to, every month, run the script and update the spreadsheet with new data. 
