#Final version of the code
import xmltodict
import csv

doc_authors = []
doc_title = []
doc_periodical = []
doc_year = []
outputFile = open('output.csv', 'wb')

with open("H:\Pubs_basedon_TCIA.xml") as f:
    doc = xmltodict.parse(f.read())

for i in range(0,len(doc['xml']['records']['record'])):
    if doc["xml"]["records"]["record"][i]["ref-type"]["@name"] == "Journal Article":
        for author in range(0,len(doc['xml']['records']['record'][i]['contributors']['authors']['author'])):
            try:                
                doc_authors.append([])
                doc_authors[i].append(doc['xml']['records']['record'][i]['contributors']['authors']['author'][author][u'style']['#text'])
            except KeyError:
                doc_authors[i].append(doc['xml']['records']['record'][i]['contributors']['authors']['author'][u'style']['#text'])

doc_authors = filter(None, doc_authors)

for i in range(0,len(doc["xml"]["records"]["record"])):
    if doc["xml"]["records"]["record"][i]["ref-type"]["@name"] == "Journal Article":
        try:
            docyeartemp = doc["xml"]["records"]["record"][i]["dates"]["year"][u'style']["#text"]
            doc_year.append(docyeartemp)
            
            doctitletemp = doc["xml"]["records"]["record"][i]["titles"]["title"][u'style']["#text"]
            doc_title.append(doctitletemp)
            
            docperiodicaltemp = doc["xml"]["records"]["record"][i]["periodical"]["full-title"][u'style']["#text"]
            doc_periodical.append(docperiodicaltemp)            
        except KeyError:
            docperiodicaltemp = doc["xml"]["records"]["record"][1]["alt-periodical"]["full-title"][u'style']["#text"]
            doc_periodical.append(docperiodicaltemp)
        except TypeError:
            try:
                doctitletemp = doc["xml"]["records"]["record"][i]["titles"]["title"][u'style'][0]["#text"]
                doc_title.append(doctitletemp)
            except KeyError:
                doctitletemp = doc["xml"]["records"]["record"][i]["titles"]["title"][u'style'][0][0]["#text"]
                doc_title.append(doctitletemp)

doc_authors = [[y.encode('UTF8') for y in x] for x in doc_authors]
doc_title = [x.encode('UTF8') for x in doc_title]
doc_year = [x.encode('UTF8') for x in doc_year]
doc_periodical = [x.encode('UTF8') for x in doc_periodical]
doc_periodical.insert(39,'Magnetic Resonance Imaging')

outputWriter = csv.writer(outputFile)
outputWriter.writerow(['Authors:'])
outputWriter.writerow(doc_authors)
outputWriter.writerow(['Title:'])
outputWriter.writerow(doc_title)
outputWriter.writerow(['Periodical:'])
outputWriter.writerow(doc_periodical)
outputWriter.writerow(['Year:'])
outputWriter.writerow(doc_year)
outputWriter.writerow('')
outputWriter.writerow(['Each column is a separate record.'])
outputFile.close()
