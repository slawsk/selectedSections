# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 11:10:36 2021

@author: Sarah
"""

#The usc26.xml is from http://uscode.house.gov/download/download.shtml

from bs4 import BeautifulSoup

file_title = 'Section_26_No_Notes.xml'
 
file = open(file_title, 'w',encoding='utf-8')

with open('usc26.xml',encoding='utf8') as fp:
    soup = BeautifulSoup(fp,'xml')

to_remove = ["note","notes","sourceCredit"]

for r in to_remove:
    for p in soup.find_all(r):
        p.decompose()


file.write(str(soup))

file.close()

   