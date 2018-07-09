import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline
from bs4 import BeautifulSoup

with open("Pubs_basedon_TCIA0618.xml","r",encoding="utf8") as f:
    xml = f.read()

soup = BeautifulSoup(xml,"lxml")

d = {}
for record in soup.xml.records:
    year = record.dates.year.text.strip()
    if year not in d:
        d[year] = 0
    else:
        d[year] += 1

years = sorted([int(x) for x in d.keys()])
count = sorted(d.values())
total = list(np.cumsum(count))

#years = [2010,2011,2012,2013,2014,2015,2016,2017,2018]
#count = [11,  15,  21,  47,  76,  116, 140, 134, 67]
#total = [11,  26,  47,  94,  170, 286, 426, 560, 627]

data = [count,total]

plt.bar(years,count,color="#FF8888")

ynew = np.linspace(2010,2018,300)
smooth = spline(years,total,ynew)
plt.plot(ynew,smooth)

plt.gca().yaxis.grid(True)

rows = ["Publications","Cumulative"]

table = plt.table(cellText=data,rowLabels=rows,colLabels=years,loc="bottom")

props = table.properties()
cells = props["child_artists"]
for cell in cells:
    cell.set_height(0.1)
    cell.set_width(0.104)

plt.tick_params(axis="x",which="both",bottom=False,top=False,labelbottom=False)
plt.ylabel("Peer-Reviewed Publications")
plt.legend(["Cumulative","Publications"])
plt.savefig("TCIAGraph.png",bbox_inches="tight")