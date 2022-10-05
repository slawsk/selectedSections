# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 11:10:36 2021

@author: Sarah
"""

#URL: https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-1 , save the HTML file
# For the 301 regs, go to here and save the relevant regs with the appropriate titles (see below): https://www.ecfr.gov/current/title-26/chapter-I/subchapter-F/part-301/subpart-ECFR5ffaf3310af6b61?toc=1


from bs4 import BeautifulSoup
import pandas as pd

#string together all the relevant regulations
filenames = ['title-26.htm','title-26-7701-1.html','title-26-7701-2.html','title-26-7701-3.html']

with open('title-26-all.htm','w',encoding='utf8') as outfile:
    for fname in filenames:
        with open(fname,encoding='utf8') as infile:
            outfile.write(infile.read())

outfile.close()

#create the intro and endtext that allows the css file
introtext = """<!doctype html>
<html>
  <head>
    <link href="regsStyle.css" rel="stylesheet" />
  </head>
  <body>"""
  
endtext = """  </body>
</html>"""


#create the file
df=pd.read_excel('regsectionstousepartnership.xlsx',sheet_name="PartA")

code_sections_list = df['Regulation'].tolist()

file_title = 'Regulations20220910.html'
    
file = open(file_title, 'w',encoding='utf-8')

file.write(introtext)


with open('title-26-all.htm',encoding='utf8') as fp:
    soup = BeautifulSoup(fp,'lxml')


#get rid of the editorial notes
for p in soup.find_all('div',attrs={"class":"editorial-note"}):
    p.decompose()


#include the relevant sections
for item in code_sections_list:
    identifier=f"{item}"
    section_to_add = soup.find('div',attrs={"class":"section",'id':identifier})
    file.write(str(section_to_add))



file.write(endtext)

file.close()

   