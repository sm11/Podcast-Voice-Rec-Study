import feedparser
import json


feed = feedparser.parse('https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/200/non-explicit.rss')

with open('./static/optionsA.json', 'w') as outfile:
    json.dump(feed, outfile, indent=4, sort_keys=True)

with open('./static/optionsA.json', 'r') as infile:
    data = json.load(infile)

    result = []
    count = 1
    title_list = data['entries']
    for item in title_list:
        a = dict(item)
        pod_dict = {}
        pod_dict['count'] = count
        pod_dict['podcasts'] = [{'title': a.get('title'), 'file-name': a.get('link')}]
        count += 1
        result.append(pod_dict)
        #print (pod_dict)



with open('./static/options.json', 'w') as outfile:
    json.dump(result, outfile, indent=4, sort_keys=True)

