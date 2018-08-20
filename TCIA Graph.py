from bs4 import BeautifulSoup
from collections import Counter
from scipy.interpolate import spline
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

with open("Pubs_basedon_TCIA0618.xml","r",encoding="utf8") as f:
    xml = f.read()

soup = BeautifulSoup(xml,"lxml")

y = []
for record in soup.xml.records:
    year = record.dates.year.text.strip()
    y.append(int(year))

counter = Counter(y)

years = sorted([int(x) for x in counter.keys()])
count = []
for c in sorted(counter.keys()):
    count.append(counter[c])
total = list(np.cumsum(count))

ax1 = plt.figure().add_subplot(111)
ax1.bar(years,count,color="#FF8888",label="Publications")
plt.ylabel("Peer-Reviewed Publications")

ynew = np.linspace(min(years),max(years),100)
smooth = spline(years,total,ynew)

ax2 = plt.twinx()
ax2.plot(ynew,smooth,label="Cumulative")

rows = ["Publications","Cumulative"]
table = plt.table(cellText=[count,total],rowLabels=rows,colLabels=years,loc="bottom")

props = table.properties()
cells = props["child_artists"]
for cell in cells:
    cell.set_height(0.1)
    cell.set_width(0.104)

red = mpatches.Patch(color="#FF8888",label="Publications")
blue = mpatches.Rectangle((0,0),1,8,color="#1F77B4",label="Cumulative")
plt.legend(handles=[red,blue])

plt.savefig("TCIAGraph.svg",bbox_inches="tight")
