# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 11:10:36 2021

@author: Sarah
"""

from bs4 import BeautifulSoup
import pandas as pd

#use the file with the notes removed, created by create26nonotes.py. That's time-consuming to run so it's better just to create it and then tweak what you're producing here.
#You also need a program after this to read the XML it produces and put it into a reasonable form. I have been using Prince because I don't know any better.
#Also notice the CSS file you need: usctitle.css            
        
introtext="""<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet type="text/css" href="usctitle.css"?><uscDoc identifier="/us/usc/t26" xml:lang="en" xmlns="http://xml.house.gov/schemas/uslm/1.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://xml.house.gov/schemas/uslm/1.0 USLM-1.0.15.xsd">
<main>
"""

endingtext = """
</main>
</uscDoc>
"""    

df=pd.read_excel('codesectionstouse.xlsx')

code_sections_list = df['Code'].tolist()
subsections_list=df['Subsection'].tolist()

file_title = 'Selected_Sections.xml'
 
   
file = open(file_title, 'w',encoding='utf-8')

file.write(introtext)

with open('Section_26_No_Notes.xml',encoding='utf8') as fp:
    soup = BeautifulSoup(fp,'xml')


code_structure_dict = {1:'subsection',2:'paragraph',3:'subparagraph'}

for item in code_sections_list:
    index_item = code_sections_list.index(item)
    section_identifier=f"/us/usc/t26/s{item}"
    section_to_add = soup.find('section',{'identifier':section_identifier})
    selected_subsections = subsections_list[index_item]
    if  selected_subsections == 'all':
        file.write(str(section_to_add))
    else:
        list_selected = list(selected_subsections.split(','))
        section_number = section_to_add.num
        section_title = section_to_add.heading
        section_num_and_title = f"<section>{section_number}{section_title}</section>"
        print(section_num_and_title)
        file.write(section_num_and_title)
        for item in list_selected:
            subsection_identifier = section_identifier
            for element in item:
                subsection_identifier = subsection_identifier+(f"/{element}")
            type_section = code_structure_dict[len(item)]
            subsection_to_add = soup.find(type_section,{'identifier':subsection_identifier})
            file.write(str(subsection_to_add))

    
file.write(endingtext)
file.close()

   