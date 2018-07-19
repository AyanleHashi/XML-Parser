from bs4 import BeautifulSoup
import ftfy
import subprocess
import csv

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
    <div class="paper droppable">
        <h4>%s</h4>
        %s
        <br>
        <periodical>%s</periodical> %s
        <pub-type> - %s</pub-type> %s
        <br>
        %s%s
    </div>
 """ % self.tuple_form()

    def tuple_form(self):
        return (self.title,self.authors,self.periodical,self.year,self.pubtype,self.citations,self.url,self.abstract)

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
    """
    #number of citations (scholar link too)
    #number of total citations per year (add to graph?)
    command = "scholar.py -c 1 --phrase \"{}\"".format(title)
    process = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
    out = process.communicate()[0].decode("cp1252").replace(r"\r","")
    time.sleep(10)
    """
    try:
        #citations = str(int(out[out.index("Citations")+len("Citations")+1:out.index("Versions")]))
        citations = ""
        citations = " cited by " + citations
    except ValueError:
        citations = ""
    try:
        url = "<a href=\"" + record.urls.find_all("related-urls")[0].url.text + "\">Website</a> - "
    except IndexError:
        url = ""
        #url = out[out.find("URL")+4:out.find("Year")][:-12]

        if "scholar.google.com" in url:
            url = url[26:]
        if len(url) != 0:
            url = "<a href=\"" + url + "\">Website</a> - "
    try:
        abstract = """<button type="button" class="btn btn-link" data-toggle="collapse" data-target="#demo{0}"><span class="glyphicon glyphicon-arrow-down"></span>Abstract</button>
        <div id="demo{0}" class="collapse">{1}</div>""".format(abstract_number,record.abstract.text)
        abstract_number += 1
    except AttributeError:
        abstract = ""
        url = url[:-3]
    #if pubtype in ["Journal Article","Conference Proceedings"]:
    records.append(Record(authors,title,periodical,year,pubtype,url,abstract,citations))

entry = ""
for r in records:
    entry += str(r)

paperpile_html = """<html>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <head>
        <script type="text/javascript">
            $(document).ready(function() {{
                $(".draggable").draggable({{
                    revert: true,
                    revertDuration: 500
                }});

                $(".droppable").droppable({{
                    activeClass: "active",
                    drop: function (event, ui) {{
                        if ($(this).text().indexOf(ui.draggable.text()) == -1) {{
                            $(this).text($(this).text() + " " + ui.draggable.text());
                        }}

                        $(this).removeClass(ui.draggable.text());
                        $(this).addClass(ui.draggable.text());
                    }}
                  }});

                $("#searchbar").on("keyup", function() {{
                    var value = $(this).val().toLowerCase();
                    $(".container .paper").filter(function() {{
                        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
                    }});
                }});
            }});
        </script>

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
            .paper {{
                border: 1px solid #DDDDDD
            }}
            #sidebar {{
                height: 500px;
                width: 160px;
                position: fixed;
                z-index: 1;
                top: 0;
                left: 5;
                padding-top: 20px;
            }}
            .draggable {{
                /*width: 10px;*/
                height: 40px;
                display: inline-block;
                background: #ccc;
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #666;
            }}
            .droppable {{
                /*margin-left: 200px;
                margin-bottom: 5px;
                width: 125px;
                height: 125px;
                background: #999;
                color: #fff;
                padding: 10px;
                border: 4px solid #999;*/
            }}
            {{% for label in labels %}}
            .{{{{ label }}}} {{}}
            {{% endfor %}}
        </style>

    </head>
    <div id="sidebar">
        <form action="" method="POST">
            Add a label: <input type="text" name="label">
            <input type="submit" value="Add">
        </form>

        {{% for label in labels %}}
        <div class="draggable">{{{{ label }}}}</div>
        {{% endfor %}}

    </div>

    <div class="container">
        <input id="searchbar" type="text" name="search" placeholder="Search...">
        {}
    </div>
</html>
""".format(entry)

with open("/home/ayanlehashi/mysite/templates/paperpile.html","w",encoding="utf8") as paperpile_html_file:
    paperpile_html_file.write(paperpile_html)

with open("/home/ayanlehashi/mysite/static/classinfo.csv","w",encoding="utf8") as csvfile:
    writer = csv.writer(csvfile)
    for record in records:
        writer.writerow(record.tuple_form())
