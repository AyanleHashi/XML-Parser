# XML-Parser
A script that extracts publication data from the Cancer Imaging Archive publication list (last updated June 2018) and formats it into HTML.

Requirements:

  * `pip install bs4`
  
  * `pip install ftfy`
  
  * `pip install lxml`
  
  * `pip install matplotlib`
  
  * `pip install scipy`

Instructions
----
1. Download and extract the repository
2. Run citationandurlgetter.py to query Google Scholar for citation counts and website links
 * Caution: this script may take up to 2 hours to run
3. Run XML-Parser.py to generate the HTML page
 * The output will appear in a new file called "Publications.html"
4. (Optional) Run TCIA Graph.py to generate a graph of publications over time in an SVG file
