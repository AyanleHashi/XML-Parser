#Updated to work with Conference Proceedings
import xmltodict
import csv

doc_authors = []
doc_title = []
doc_periodical = []
doc_year = []
doc_pubtype = []
outputFile = open('output2.csv', 'wb')
with open("H:\Pubs_basedon_TCIA0716.xml") as f:
    doc = xmltodict.parse(f.read())

for i in range(0,len(doc['xml']['records']['record'])):
    if doc["xml"]["records"]["record"][i]["ref-type"]["@name"] == "Journal Article"\
    or doc["xml"]["records"]["record"][i]["ref-type"]["@name"] == "Conference Proceedings":
        for author in range(0,len(doc['xml']['records']['record'][i]['contributors']['authors']['author'])):
            try:                
                doc_authors.append([])
                doc_authors[i].append(doc['xml']['records']['record'][i]['contributors']['authors']['author'][author][u'style']['#text'])
            except KeyError:
                doc_authors[i].append(doc['xml']['records']['record'][i]['contributors']['authors']['author'][u'style']['#text'])
doc_authors = filter(None, doc_authors)

for i in range(0,len(doc["xml"]["records"]["record"])):
    if doc["xml"]["records"]["record"][i]["ref-type"]["@name"] == "Journal Article"\
    or doc["xml"]["records"]["record"][i]["ref-type"]["@name"] == "Conference Proceedings":
        try:
            docpubtemp = doc["xml"]["records"]["record"][i]["ref-type"]["@name"]
            doc_pubtype.append(docpubtemp)
            print docpubtemp
            
            docyeartemp = doc["xml"]["records"]["record"][i]["dates"]["year"][u'style']["#text"]
            doc_year.append(docyeartemp)
            print docyeartemp
            
            doctitletemp = doc["xml"]["records"]["record"][i]["titles"]["title"][u'style']["#text"]
            doc_title.append(doctitletemp)
            print doctitletemp
            
            docperiodicaltemp = doc["xml"]["records"]["record"][i]["periodical"]["full-title"][u'style']["#text"]
            doc_periodical.append(docperiodicaltemp)
            print docperiodicaltemp
        except KeyError:
            try:
                docperiodicaltemp = doc["xml"]["records"]["record"][i]["alt-periodical"]["full-title"][u'style']["#text"]
                doc_periodical.append(docperiodicaltemp)
            except KeyError:
                docperiodicaltemp = 'None'
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
doc_pubtype = [x.encode('UTF8') for x in doc_pubtype]
doc_periodical.insert(39,'Magnetic Resonance Imaging')

outputWriter = csv.writer(outputFile)
outputWriter.writerow(['Author:', 'Title:', 'Periodical:', 'Year:','Publication Type:'])
try:
    for record in range(0,len(doc['xml']['records']['record'])):
        outputWriter.writerow([doc_authors[record], doc_title[record], doc_periodical[record], doc_year[record], doc_pubtype[record]])
except IndexError:
    print 'Done writing to file.'
outputFile.close()