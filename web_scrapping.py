#!/usr/bin/python

import bs4, requests, csv

# Get page html content.
url = "https://insideevs.com/reviews/344001/compare-evs/"
page = requests.get(url)
page.raise_for_status()
pageContent = bs4.BeautifulSoup(page.text, 'html.parser')

# Get BEV tables.
tableList = pageContent.find_all("tbody")
fistBevtTable = tableList[0]
secondBevtTable = tableList[1]

# Get BEV header.
firstBevTableHeaderHtmlList = fistBevtTable.find("tr").find_all("strong")
secondBevtTableHeaderHtmlList = secondBevtTable.find("tr").find_all("strong")
firstBevTableHeaderList = []
secondBevtTableHeaderList = []
for header in firstBevTableHeaderHtmlList:
    firstBevTableHeaderList.append(header.contents[0])
for header in secondBevtTableHeaderHtmlList:
    secondBevtTableHeaderList.append(header.contents[0])

# Build new header list.
newHeaderList = []
for header in firstBevTableHeaderList:
    newHeaderList.append(header)
for header in secondBevtTableHeaderList:
    if header not in newHeaderList:
        newHeaderList.append(header)

# Get BEV data.
firstBevTableDataHtmlList = fistBevtTable.find_all("tr")[1:]
firstBevData = []
for row in firstBevTableDataHtmlList:
    rowData = []
    for element in row.find_all("td"):
        rowData.append(element.contents[0])
    rowData[0] = rowData[0].contents[0]
    firstBevData.append(rowData)

secondBevtTableDataHtmlList = secondBevtTable.find_all("tr")[1:]
secondBevData = []
for row in secondBevtTableDataHtmlList:
    rowData = []
    for element in row.find_all("td"):
        rowData.append(element.contents[0])
    rowData[0] = rowData[0].contents[0]
    secondBevData.append(rowData)

# Merge two data.
newBevData = []
for i,row in enumerate(firstBevData):
    newRow = []
    for e in row:
        newRow.append(e)
    for e in secondBevData[i][1:]:
        newRow.append(e)
    newBevData.append(newRow)
    
# Creat HTML file.
htmlHeader = """
<html>
<head>
</head>
<body>
<table>
"""

newTableHeader = "<thead><tr>"
for header in newHeaderList:
     newTableHeader = newTableHeader + "<th>" + header + "</th>"
newTableHeader = newTableHeader + "</tr></thead>"

newTableContent = "<tbody>"
for row in newBevData:
    newTableContent = newTableContent + "<tr>"
    for e in row:
        newTableContent = newTableContent + "<td>" + e + "</td>"
newTableContent = newTableContent + "</tr></tbody>"

htmlFooter = """
</table>
</body>
</html>
"""
htmlContent = htmlHeader + newTableHeader + newTableContent + htmlFooter
with open('newTable.html', 'w') as f:
    f.write(htmlContent)

# Get table data from html file
with open("newTable.html", 'r') as file:
    soup = bs4.BeautifulSoup(file.read(), 'html.parser')

# Creat header list.
headerList = []
for header in soup.find_all("th"):
    headerList.append(header.getText())
# Creat content list.
contentList = []
cnt = 0
contentRow = []
for e in soup.find_all("td"):    
    if cnt<10:
        contentRow.append(e.getText())
        cnt = cnt+1
    elif cnt == 10:
        contentList.append(contentRow)
        contentRow = []
        cnt = 0
        contentRow.append(e.getText())
        cnt = cnt+1
        

with open("car_info_output.csv", 'w') as csvFile:
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(headerList)
    csvWriter.writerows(contentList)
