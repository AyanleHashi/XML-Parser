from bs4 import BeautifulSoup
from ftfy import fix_text
from time import sleep, time
import csv
import subprocess

start = time()

with open("Pubs_basedon_TCIA0618.xml","r",encoding="utf8") as f:
    xml = f.read()

soup = BeautifulSoup(xml,"lxml")

record_titles = []
for record in soup.xml.records:
    record_titles.append(fix_text(record.titles.title.text))

with open("titleinfo_fixed.csv","r") as f:
    reader = csv.reader(f)
    file_titles = []
    for row in reader:
        file_titles.append(row[0])

s = list(set(record_titles))
t = list(set(file_titles))

with open("titleinfo_fixed.csv","a",newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
    
    no_output = []
    c = 0
    for record_title in record_titles:
        if record_title not in file_titles:
            command = "scholar.py -c 1 -p \"{}\" --cookie-file scholar-cookies.txt".format(record_title)
            process = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
            out = process.communicate()[0].decode("cp1252").replace("\r","")[:-2]
            try:
                citations = str(int(out[out.index("Citations")+10:out.index("Versions")]))
                
                if out.find("URL") != -1:
                    if out.find("Year") == -1:
                        url = out[out.index("URL")+4:out.index("Citations")].strip()
                    else:
                        url = out[out.index("URL")+4:out.index("Year")].strip()
                else:
                    url = ""
                
                if "scholar.google.com" in url:
                    url = url[26:]
                
                writer.writerow([fix_text(record_title.replace("–","-")),citations,url])
                print("\n".join([record_title,citations,url]) + "\n\n")
                file_titles.append(record_title)
            except ValueError as e:
                if len(out) == 0:
                    print("No output\n" + record_title + "\n")
                    c += 1
                    no_output.append(record_title)
                else:
                    print("ERROR ON " + record_title + "\n" + repr(e) + "\n")
            except Exception as e:
                print(repr(e) + "\n")
            sleep(10)

print("Finished in", time()-start,"seconds.")
print(c, "papers with no output.")