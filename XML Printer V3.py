import xmltodict, csv

outputFile = open('output.csv','wb')

with open("H:\Pubs_basedon_TCIA.xml") as fd:
    doc = xmltodict.parse(fd.read())

for i in range(0,len(doc['xml']['records']['record'])):
    if doc["xml"]["records"]["record"][i]["ref-type"]["@name"] == "Journal Article":
        for author in range(0,len(doc['xml']['records']['record'][i]['contributors']['authors']['author'])):
            print doc['xml']['records']['record'][i]['contributors']['authors']['author'][author][u'style']['#text']