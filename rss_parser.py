#!/usr/bin/python
import urllib
import urllib.request
import json
import re
import os
import sys
from xml.dom import minidom
from xml.etree import ElementTree as etree
import feedparser
import json

# progress bar functions
def _reporthook(numblocks, blocksize, filesize, url=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
    except:
        percent = 100
    if numblocks != 0:
        bar = '#' * int(percent/5) + '-' * int(20-percent/5)
        print('\r[%s] %s%s   ' % (bar, percent, '%')),
        sys.stdout.flush()

#import requests
def geturl(url, dst):
    """
    if(os.path.isfile(dst)):
        if(input("A file already exists with that name. Continue? (y/n)").lower() == 'n'):
            print("Move the file and try again")
            sys.exit(0)
    """

    try:
        urllib.request.urlretrieve(url, dst.encode("ascii", "ignore"),
                       lambda nb, bs, fs, url=url: _reporthook(nb,bs,fs,url))
    except IOError:
        print("There was an error retrieving the data. Check your internet connection and try again.")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nYou have interrupted an active download.\n Cleaning up fines now.")
        os.remove(dst)
        sys.exit(1)

def parseFeed(url):
    feed = feedparser.parse(url)
    with open('./static/optionsA.json', 'w') as outfile:
        json.dump(feed, outfile, indent=4, sort_keys=True)

    with open('./static/optionsA.json', 'r') as infile:
        data = json.load(infile)

        p_ids = []
        title_list = data['entries']
        for item in title_list:
            a = dict(item)
            url = a.get('link')
            title = a.get('title')
            pod_id = re.findall(r'\d+', url)[0]
            add_id = [{'title': title, 'id':pod_id}]
            p_ids.append(add_id)
    return p_ids

def main():
    link = 'https://rss.itunes.apple.com/api/v1/us/podcasts/top-podcasts/all/200/non-explicit.rss'
    pod_ids = parseFeed(link)
    result = []
    count = 1

    # grab podcast feed
    for cast in pod_ids:
        podcastName = cast[0]['title']
        podcastId = cast[0]['id']
        url = "https://itunes.apple.com/lookup?id=" + str(podcastId) + "&entity=podcast"
        try:
            with urllib.request.urlopen(url) as url2:
                response = url2.read().decode(url2.headers.get_content_charset())
        except IOError:
            print("There was an error retrieving the data. Check your internet connection and try again.")
            sys.exit(0)

        data = json.loads(response)
        rss = data["results"][0]["feedUrl"]

        # grab all podcast .mp3 files
        url_str = rss
        try:
            xml_str = urllib.request.urlopen(url_str).read()
        except IOError:
            print("There was an error retrieving the data. Check your internet connection and try again.")
        
        xmldoc = minidom.parseString(xml_str)

        values = xmldoc.getElementsByTagName('enclosure')
        titles = xmldoc.getElementsByTagName('title')

        # append the title list such that the correct title is corresponding to the
        # equivlanet .mp3 link

        nameChecker = True
        counter = 1

        while nameChecker:
            if podcastName == titles[counter].firstChild.nodeValue:
                counter = counter + 1
            else:
                nameChecker = False

        titles = titles[counter:]

        # insert mp3 list into mp3list array
        mp3list = []
        for val in values:
            mp3list.append(val.attributes['url'].value)

        saveLoc = os.path.dirname(os.path.realpath(__file__)) + "/static/audio/" + titles[0].firstChild.nodeValue + ".mp3"

        pod_dict={}
        pod_dict['count'] = count
        pod_dict['podcasts'] = [{'title': podcastName, 'file-name': saveLoc}]
        count += 1

        result.append(pod_dict)
        geturl(mp3list[0], saveLoc)

    with open('./static/options.json', 'w') as outfile:
        json.dump(result, outfile, indent=4, sort_keys=True)
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n')
        sys.exit(0)
