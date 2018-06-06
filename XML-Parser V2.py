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
#The following for loop only looks at the first record; remove the '[:1]' if you
#would like to process the whole document.
for r in records[:1]:
        row += """    <tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
    </tr>
""".format(r.authors,r.title,r.periodical,r.year,r.pubtype)

print("""HTML Table:
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
}}""".format(row))

print("""\n\n\nPaperPile Format:
<html>
<h3>{}</h3>
  {}
  <br>
  <periodical>{}</periodical>, {}
  <pub-type> - {}</pub-type>
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
}}""".format(records[0].title,records[0].authors,records[0].periodical,records[0].year,records[0].pubtype))
