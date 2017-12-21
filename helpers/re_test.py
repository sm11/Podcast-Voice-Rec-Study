import re
url = 'https://itunes.apple.com/us/podcast/majority-54/id1309354521?mt=2'


url_split = re.split('/', url)
elements = [re.findall('\id\d+', s) for s in url_split]
el = [e for e in elements if len(e)][0][0]
pod_id = re.split('id', el)[-1]


print (pod_id)


url_split = re.split('/', url)
elements = [re.findall('\id\d+', s) for s in url_split]
for el in elements:
    if len(el):
        pod_id = re.split('id', el[0])[-1]