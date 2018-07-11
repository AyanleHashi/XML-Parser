from bs4 import BeautifulSoup
import ftfy
import subprocess

"""
The main problem is that Google Scholar does not allow too many requests at a
time, and given how large the publication XML file is, it blocks you from
getting all of the URLs in one go.

Potential Solutions:
    -Have the script run in multiple parts
    -Add time.sleep(10) after each element in the for loop (change time if needed)
"""

path = "/home/ayanlehashi/mysite/scripts/Pubs_basedon_TCIA0618.xml"

class Record:
    def __init__(self,authors="",title="",periodical="",year="",pubtype="",url="",abstract="",citations=""):
        self.authors = authors
        self.title = title
        self.periodical = periodical
        self.year = year
        self.pubtype = pubtype
        self.url = url
        self.abstract = abstract
        self.citations = citations

        self.labels = []

    def __str__(self):
        return """
    <div id="paper">
        <h4>%s</h4>
        %s
        <br>
        <periodical>%s</periodical> %s
        <pub-type> %s</pub-type>
        <br>
        %s%s
    </div>
 """ % self.tuple_form()

    def tuple_form(self):
        return (self.title,self.authors,self.periodical,self.year,self.pubtype,self.url,self.abstract)

with open(path,encoding="utf8") as f:
    xml = f.read()

records = []
soup = BeautifulSoup(xml,"lxml")
abstract_number = 1
for record in soup.xml.records:
    authors = ""
    for author in record.contributors.authors:
        authors += author.text + "; "
    authors = ftfy.fix_text(authors[:-2])
    title = record.titles.title.text
    try:
        periodical = record.periodical.find_all("full-title")[0].text + ", "
    except AttributeError:
        periodical = ""
    year = record.dates.year.text
    pubtype = record.find_all("ref-type")[0]["name"]
    try:
        url = "<a href=\"" + record.urls.find_all("related-urls")[0].url.text + "\">Website</a>"
    except IndexError:
        url = ""
        citations = ""
        """
        #number of citations (scholar link too)
        #number of total citations per year (add to graph?)
        command = "scholar.py -c 1 --phrase \"{}\"".format(title)
        process = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
        out = process.communicate()[0].decode("cp1252").replace(r"\r","")
        url = out[out.find("URL")+4:out.find("Year")][:-12]
        citations = str(int(out[out.index("Citations")+len("Citations")+1:out.index("Versions")]))


        if "scholar.google.com" in url:
            url = url[26:]
        if len(url) != 0:
            url = "<a href=\"" + url + "\">Website</a>"
        """
    try:
        abstract = """<button type="button" class="btn btn-link" data-toggle="collapse" data-target="#demo{0}"><span class="glyphicon glyphicon-arrow-down"></span>Abstract</button>
        <div id="demo{0}" class="collapse">{1}</div>""".format(abstract_number,record.abstract.text)
        abstract_number += 1
    except AttributeError:
        abstract = ""
    if pubtype in ["Journal Article","Conference Proceedings"]:
        records.append(Record(authors,title,periodical,year,pubtype,url,abstract))

entry = ""
for r in records:
    entry += str(r)

paperpile_html = """<html>
    <head>
        <style>
            html {{
                font-family: "Helvetica";
                line-height:150%
            }}
            periodical {{
                color: green;
                font-style: italic;
            }}
            pub-type {{
                color: #666666;
            }}
            h4 {{
                margin-bottom: 0px;
                color: #0FA5F0;
            }}
            a {{
                text-decoration: none;
            }}
            #paper {{
                border: 1px solid #DDDDDD
            }}
        </style>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    </head>
    <div class="container">
        {}
    </div>
</html>
""".format(entry)

with open("/home/ayanlehashi/mysite/templates/paperpile.html","w",encoding="utf8") as paperpile_html_file:
    paperpile_html_file.write(paperpile_html)
