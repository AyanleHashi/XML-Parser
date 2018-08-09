from bs4 import BeautifulSoup
import ftfy
import csv

path = "/home/ayanlehashi/mysite/scripts/Pubs_basedon_TCIA0618.xml"

class Record:
    def __init__(self,i="",authors="",title="",periodical="",year="",pubtype="",citations="",url="",abstract="",keywords="",abstract_div=""):
        self.i = i
        self.authors = authors
        self.title = title
        self.periodical = periodical
        self.year = year
        self.pubtype = pubtype
        self.citations = citations
        self.url = url
        self.abstract = abstract
        self.keywords = keywords
        if self.keywords == []:
            self.keywords = ""
        self.abstract_div = abstract_div

    def __str__(self):
     return """
        <div id="{0}" class="paper droppable">
            <h4>{1}</h4>
            <author>{2}</author>
            <br><periodical>{3}</periodical> {4}
            <pub-type> - {5}</pub-type>{6}
            <br>{7}
            {8}
            {9}
            {10}
        </div>
     """.format(*self.tuple_form())

    def tuple_form(self):
        return (self.i,self.title,self.authors,self.periodical,self.year,self.pubtype,self.citations,self.url,self.abstract,self.keywords,self.abstract_div)

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
keyword_number = 1
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
            citations = ", cited " + i[1] + " times"
            if i[1] == "1":
                citations = citations[:-1]
            info_url = "<a href=\"" + str(i[2]) + "\"><span class=\"glyphicon glyphicon-link\"></span>Website</a>"
    if len(citations) == 0:
        citations = ", cited 0 times"

    try:
        url = "<a href=\"" + record.urls.find_all("related-urls")[0].url.text + "\"><span class=\"glyphicon glyphicon-link\"></span>Website</a>"
    except IndexError:
        url = info_url
    try:
        abstract = """<button type="button" class="btn btn-link" data-toggle="collapse" data-target="#abstract{0}"><span class="glyphicon glyphicon-arrow-down"></span>Abstract</button>""".format(abstract_number)
        abstract_div = """<div id="abstract{0}" class="collapse">{1}</div>""".format(abstract_number,record.abstract.text)
        abstract_number += 1
    except AttributeError:
        abstract = ""
        abstract_div = ""

    keyword_list = []
    keyword_list_div = ""
    try:
        for kw in record.keywords:
            s = ftfy.fix_text(kw.text)
            if "," in s:
                keyword_list.extend([x.strip() for x in s.split(", ")])
            else:
                keyword_list.append(s)
        keyword_list = " · ".join(keyword_list)
        keyword_list = """<button type="button" class="btn btn-link" data-toggle="collapse" data-target="#tag{0}"><span class="glyphicon glyphicon-tag"></span>Tags</button>
            <div id="tag{0}" class="collapse">{1}</div>""".format(keyword_number,keyword_list)

        keyword_number += 1
    except:
        pass

    records.append(Record(str(record_number),authors,title,periodical,year,pubtype,citations,url,abstract,keyword_list,abstract_div))
    record_number += 1

entry = ""
for r in records:
    entry += str(r)

paperpile_html = """<!DOCTYPE html>
    <html>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="shortcut icon" href="https://wiki.cancerimagingarchive.net/s/en_GB/7400/f2dd15fadfb45568d4c57973599993b8f86142a0/28/_/favicon.ico">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js"></script>
    <script src="/static/script.js"></script>

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
                position: relative;
                top: 100px;
                left: 1vw;
                width: 8vw;
            }}
            #wrapper {{
                position: fixed;
                top: 0;
                width: 8vw;
                height: 100%;
                background-color: #eee;
                z-index: 5;
            }}
            #header {{
                position: fixed;
                height: 100px;
                width: 100%;
                z-index: 4;
                background-color: #eee;/*#205081*/
                border-bottom: 2px solid #ccc;
                float: left;
            }}
            #labelInput {{
                width: 70%;
            }}
            .input-group {{
                width: 45vw;
                padding-top: 30px;
                left: 8vw;
            }}
            .container {{
                padding-top: 110px;
                margin-left: 8vw;
                width: 50vw;
                border: 2px solid #ccc;
            }}
            .draggable {{
                height: 40px;
                display: inline-block;
                background: #ddd;
                border-radius: 5px;
                border: 1px solid #666;
                padding: 10px;
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

    <body>
        <div id="header">
            <div class="input-group">
                <span class="input-group-addon"><i class="glyphicon glyphicon-search"></i></span>
                <input id="searchbar" type="text" class="form-control searchbar" name="Searchbar" autofocus>
            </div>
        </div>

        <div id="wrapper">
            <div id="sidebar">
                <form action="" method="POST">
                    <input id="labelInput" type="text" class="form-control searchbar" name="label" placeholder="Add label">
                    <button id="labelSubmit" class="btn">Add</button><br><br>
                    <b>LABELS</b>

                    <!--<button id="titleSort" type="button">Title</button>
                    <button id="authorSort" type="button">Author</button>-->
                </form>
            </div>
        </div>

        <div class="container">
            {}
            <ul class="pagination pagination-sm"></ul>
        </div>
    </body>
</html>
""".format(entry)

with open("/home/ayanlehashi/mysite/templates/paperpile.html","w",encoding="utf8") as paperpile_html_file:
    paperpile_html_file.write(paperpile_html)
