import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline
from bs4 import BeautifulSoup
from collections import Counter

with open("Pubs_basedon_TCIA0618.xml","r",encoding="utf8") as f:
    xml = f.read()

soup = BeautifulSoup(xml,"lxml")

y = []
for record in soup.xml.records:
    year = record.dates.year.text.strip()
    y.append(int(year))

counter = Counter(y)

"This pulls the years from the actual publication XML"
years = sorted([int(x) for x in counter.keys()])
count = []
for c in sorted(counter.keys()):
    count.append(counter[c])
total = list(np.cumsum(count))


"Preset data taken from the TCIA Publications page"
"""years = [2010,2011,2012,2013,2014,2015,2016,2017,2018]
count = [11,  15,  21,  47,  76,  116, 140, 134, 67]
total = [11,  26,  47,  94,  170, 286, 426, 560, 627]
"""
data = [count,total]

ax1 = plt.bar(years,count,color="#FF8888",label="Publications")
ax1.set_label("Publications")
plt.ylabel("Peer-Reviewed Publications")

ynew = np.linspace(2010,2018,300)
smooth = spline(years,total,ynew)

ax2 = plt.twinx()
ax2.plot(ynew,smooth,label="Cumulative")

rows = ["Publications","Cumulative"]

table = plt.table(cellText=data,rowLabels=rows,colLabels=years,loc="bottom")

props = table.properties()
cells = props["child_artists"]
for cell in cells:
    cell.set_height(0.1)
    cell.set_width(0.104)

plt.tick_params(axis="x",which="both",bottom=False,top=False,labelbottom=False)
#plt.legend(["Cumulative","Publications"])
plt.legend()
plt.savefig("TCIAGraph.svg",bbox_inches="tight")
