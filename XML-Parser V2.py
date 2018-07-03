from bs4 import BeautifulSoup
import subprocess


path = "C:\\Users\\hashiam\\Desktop\\Python Scripts\\Pubs_basedon_TCIA0618.xml"

class Record:
    def __init__(self,authors="",title="",periodical="",year="",pubtype="",url="",abstract=""):
        self.authors = authors
        self.title = title
        self.periodical = periodical
        self.year = year
        self.pubtype = pubtype
        self.url = url
        self.abstract = abstract
    
    def __str__(self):
        return """
  <div>
  <h4>%s</h4>
  %s
  <br>
  <i><periodical>%s</periodical></i> %s
  <pub-type> - %s</pub-type>
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
for record in soup.xml.records:
    authors = ""
    for author in record.contributors.authors:
        authors += author.text + "; "
    authors = authors[:-2]
    title = record.titles.title.text
    try:
        periodical = record.periodical.find_all("full-title")[0].text + ", "
    except AttributeError:
        periodical = ""
    year = record.dates.year.text
    pubtype = record.find_all("ref-type")[0]["name"]
    try:
        url = "<a href=\"" + record.urls.find_all("related-urls")[0].url.text + "\">Website</a> - "
    except IndexError:
        url = ""
        #number of citations (scholar link too)
        #number of total citations per year (add to graph?)
        command = "scholar.py -c 1 --phrase \"{}\"".format(title)
        process = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
        out = process.communicate()[0].decode("cp1252").replace(r"\r","")
        url = out[out.find("URL")+4:out.find("Year")][:-12]
        
        if "scholar" in url:
            url = url[26:]
        url = "<a href=\"" + url + "\">Website</a> - "
        
    try:
        abstract = record.abstract.text
    except AttributeError:
        abstract = ""
        url = url[:-3]
    if pubtype in ["Journal Article","Conference Proceedings"]:
        records.append(Record(authors,title,periodical,year,pubtype,url,abstract))

entry = ""
for r in records:
    entry += str(r)

paperpile_html = """<html>
  <style>
    html {{
      font-family: "Helvetica";
      line-height:150%
    }}
    periodical {{
      color: green;
    }}
    pub-type {{
      color: #666666;
    }}
    h4 {{
      margin-bottom: 0px;
      color: #064361;
    }}
    a {{
      text-decoration: none;
    }}
    div {{
      margin-right: 25em;
      margin-left: 35em;
    }}
  </style>  
  {}
</html>
""".format(entry)

with open("paperpile.html","w",encoding="utf8") as paperpile_html_file:
    paperpile_html_file.write(paperpile_html)

#------------------------------------------------------------------------------

row = ""
for r in records:
    row += """    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
    </tr>
""" % r.tuple_form()

table_html = """<html>
  <style>
      table, th, td {{
        border: 1px solid black;
      }}
      th {{
        text-align: left;
      }}
  </style>
  
  <table style=\"width:100%\">
    <tr>
      <th>Title</th>
      <th>Authors</th>
      <th>Periodical</th>
      <th>Year</th>
      <th>Publication Type</th>
      <th>URL</th>
      <th>Abstract</th>
    </tr>
{}
  </table>
</html>""".format(row)

with open("table.html","w",encoding="utf8") as table_html_file:
    table_html_file.write(table_html)
