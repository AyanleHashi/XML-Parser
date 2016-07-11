import xmltodict, csv

doc_authors = []
doc_title = []
doc_periodical = []
doc_year = []
outputFile = open('output.csv', 'w')

with open("H:\Pubs_basedon_TCIA.xml") as fd:
    doc = xmltodict.parse(fd.read())

for author in range(0,8):
    doc_authors.append(doc["xml"]["records"]["record"][0]["contributors"]["authors"]["author"][author][u'style']["#text"])
doc_title.append(doc["xml"]["records"]["record"][0]["titles"]["title"][u'style']["#text"])
doc_periodical.append(doc["xml"]["records"]["record"][0]["periodical"]["full-title"][u'style']["#text"])
doc_year.append(doc["xml"]["records"]["record"][0]["dates"]["year"][u'style']["#text"])

for i in range(0,len(doc["xml"]["records"]["record"])):
    if doc["xml"]["records"]["record"][i]["ref-type"]["@name"] == "Journal Article":
        try:
            doctitletemp = doc["xml"]["records"]["record"][i]["titles"]["title"][u'style']["#text"]
            doc_title.append(doctitletemp)
            
            docperiodicaltemp = doc["xml"]["records"]["record"][i]["periodical"]["full-title"][u'style']["#text"]
            doc_periodical.append(docperiodicaltemp)
            
            docyeartemp = doc["xml"]["records"]["record"][i]["dates"]["year"][u'style']["#text"]
            doc_year.append(docyeartemp)
        except TypeError:
            pass
        except KeyError:
            docperiodicaltemp = doc["xml"]["records"]["record"][1]["alt-periodical"]["full-title"][u'style']["#text"]
            doc_periodical.append(docperiodicaltemp)

doc_title = [x.encode('UTF8') for x in doc_title]
doc_year = [x.encode('UTF8') for x in doc_year]
doc_periodical = [x.encode('UTF8') for x in doc_periodical]

def writeCSV():
    try:
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow(['Authors:'])
        outputWriter.writerow(doc_authors)
        outputWriter.writerow(['Title:'])
        outputWriter.writerow(doc_title)
        outputWriter.writerow(['Periodical:'])
        outputWriter.writerow(doc_periodical)
        outputWriter.writerow(['Year:'])
        outputWriter.writerow(doc_year)
        outputFile.close()
    except UnicodeEncodeError:
        pass
writeCSV()
print len(doc_title)
print len(doc_periodical)
print len(doc_year)