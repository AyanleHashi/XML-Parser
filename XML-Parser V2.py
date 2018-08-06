from bs4 import BeautifulSoup
import ftfy
import csv

path = "/home/ayanlehashi/mysite/scripts/Pubs_basedon_TCIA0618.xml"

class Record:
    def __init__(self,i="",authors="",title="",periodical="",year="",pubtype="",url="",abstract="",citations="",keywords=""):
        self.i = i
        self.authors = authors
        self.title = title
        self.periodical = periodical
        self.year = year
        self.pubtype = pubtype
        self.url = url
        self.abstract = abstract
        self.citations = citations
        self.keywords = keywords
        if type(self.keywords) == type(list()):
            self.keywords = ", ".join(self.keywords)

    def __str__(self):
     return """
        <div id="{0}" class="paper droppable">
            <h4>{1}</h4>
            <author>{2}</author>
            <br>
            <periodical>{3}</periodical> {4}
            <pub-type> - {5}</pub-type>{6}
            <br>
            {7}{8}
            {9}
        </div>
     """.format(*self.tuple_form())

    def tuple_form(self):
        return (self.i,self.title,self.authors,self.periodical,self.year,self.pubtype,self.citations,self.url,self.abstract,self.keywords)

with open("/home/ayanlehashi/mysite/static/titleinfo_fixed_forreal_utf8.csv","r") as f:
    reader = csv.reader(f)
    title_info = []
    for row in reader:
        title_info.append((row[0],row[1],row[2]))

with open(path,encoding="utf8") as f:
    xml = f.read()

records = []
soup = BeautifulSoup(xml,"lxml")

abstract_number = 1
record_number = 1

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

    citations = ""
    info_url = ""
    for i in title_info:
        if title.replace("‐","-") == i[0].replace("‐","-"):
            citations = ", cited " + str(i[1]) + " times"
            info_url = "<a href=\"" + str(i[2]) + "\"><span class=\"glyphicon glyphicon-link\"></span>Website</a>"
    if len(citations) == 0:
        citations = ", cited 0 times"

    try:
        url = "<a href=\"" + record.urls.find_all("related-urls")[0].url.text + "\"><span class=\"glyphicon glyphicon-link\"></span>Website</a>"
    except IndexError:
        url = info_url
    try:
        abstract = """<button type="button" class="btn btn-link" data-toggle="collapse" data-target="#demo{0}"><span class="glyphicon glyphicon-arrow-down"></span>Abstract</button>
        <div id="demo{0}" class="collapse">{1}</div>""".format(abstract_number,record.abstract.text)
        abstract_number += 1
    except AttributeError:
        abstract = ""

    keyword_list = []
    try:
        for kw in record.keywords:
            s = ftfy.fix_text(kw.text.lower())
            if "," in s:
                keyword_list.extend([x.strip() for x in s.split(", ")])
            else:
                keyword_list.append(s)
    except:
        pass

    records.append(Record(str(record_number),authors,title,periodical,year,pubtype,url,abstract,citations,keyword_list))
    record_number += 1

entry = ""
for r in records:
    entry += str(r)

paperpile_html = """<html>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="https://wiki.cancerimagingarchive.net/s/en_GB/7400/f2dd15fadfb45568d4c57973599993b8f86142a0/28/_/favicon.ico">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js"></script>
    <script src="/static/draggable.js"></script>

    <head>
        <title>TCIA Publications</title>
        <style>
            html {{
                font-family: "Arial";
                line-height:150%;
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
                color: #009;
            }}
            a {{
                text-decoration: none;
            }}
            #sidebar {{
                width: 100px;
                position: fixed;
                z-index: 1;
                top: 120;
                left: 5;
            }}
            #header {{
                left: 0;
                right: 0;
                position: absolute;
                height: 100px;
                background-color: #eee;
            }}
            .input-group {{
                width: 70%;
                padding-top: 30;
                left: 17vw;
            }}
            .container {{
                padding-top: 50px;
            }}
            .draggable {{
                height: 40px;
                display: inline-block;
                background: #ddd;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #666;
            }}
            .draggable-after {{
                height: 40px;
                display: inline-block;
                background: #ddd;
                border-radius: 5px;
                border: 1px solid #666;
                padding: 10px;
            }}
            .btn-link {{
                padding: 0px;
            }}
        </style>
    </head>

    <div id="header">
        <div class="input-group">
            <span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span>
            <input id="searchbar" type="text" class="form-control searchbar" name="Searchbar">
        </div>
    <div>

    <div id="sidebar">
        <form action="" method="POST">
            <input id="labelInput" type="text" class="form-control searchbar" name="label" placeholder="Add label...">
            <button id="labelSubmit">Add</button>

            <!--<button id="titleSort" type="button">Title</button>
            <button id="authorSort" type="button">Author</button>-->
        </form>
    </div>

    <div class="container">

        {}
    </div>
</html>
""".format(entry)

with open("/home/ayanlehashi/mysite/templates/paperpile.html","w",encoding="utf8") as paperpile_html_file:
    paperpile_html_file.write(paperpile_html)
