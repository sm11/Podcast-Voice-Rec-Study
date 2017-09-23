import feedparser
import json

feed = feedparser.parse('https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/10/non-explicit.rss')

with open('./static/options.json','w') as outfile:
    json.dump(feed, outfile, indent=4)

outfile.close()


