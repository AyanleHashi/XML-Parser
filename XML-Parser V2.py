from bs4 import BeautifulSoup

class Record:
    def __init__(self,authors="",title="",periodical="",year="",pubtype=""):
        self.authors = authors
        self.title = title
        self.periodical = periodical
        self.year = year
        self.pubtype = pubtype

    def __str__(self):
        return "Authors: " + self.authors + "\nTitle: " + self.title +\
        "\nPeriodical: " + self.periodical + "\nYear: " + self.year +\
        "\nPublication Type: " + self.pubtype

    def tuple_form(self):
        return (self.authors,self.title,self.periodical,self.year,self.pubtype)

with open("C:\\Users\\hashiam\\Desktop\\Python Scripts\\Pubs_basedon_TCIA0518.xml",encoding="utf8") as f:
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
        periodical = record.periodical.find_all("full-title")[0].text
    except AttributeError:
        periodical = "None"
    year = record.dates.year.text
    pubtype = record.find_all("ref-type")[0]["name"]
    records.append(Record(authors,title,periodical,year,pubtype))

row = ""
for r in records:
        row += """    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
    </tr>
""" % r.tuple_form()

html_table = """HTML Table:
<html>
  <table style=\"width:100%\">
    <tr>
      <th>Authors</th>
      <th>Title</th>
      <th>Periodical</th>
      <th>Year</th>
      <th>Publication Type</th>
    </tr>
{}
  </table>
</html>

CSS:

table, th, td {{
    border: 1px solid black;
}}
th {{
    text-align: left;
}}""".format(row)

paperpile = """\n\nPaperPile Format:
<html>
<h3>%s</h3>
  %s
  <br>
  <periodical>%s</periodical>, %s
  <pub-type> - %s</pub-type>
</html>

CSS:

html {{
  font-family: "Arial";
}}
periodical {{
  color: green;
}}

pub-type {{
  color: LightGray;
}}""" % records[0].tuple_form()

with open("output.txt","w",encoding="utf8") as html:
    html.write(html_table)
    html.write(paperpile)

print(html_table)
print(paperpile)
