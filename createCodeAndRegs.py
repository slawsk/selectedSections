# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 05:59:26 2022

@author: Sarah
"""

from bs4 import BeautifulSoup
import pandas as pd

###After downloading files for regulations, fix the problem in 1.704-2(m) and 1.751-1(g) that the /div is in the wrong place and the regulations don't print.


def create26NoNotes(source26File,outputTitle):
    #URL: https://uscode.house.gov/download/download.shtml
    #The specific URL for Title 26 is https://uscode.house.gov/download/releasepoints/us/pl/117/214/xml_usc26@117-214.zip
    file = open(outputTitle, 'w',encoding='utf-8')
    with open(source26File,encoding='utf8') as fp:
        soup = BeautifulSoup(fp,'xml')
    to_remove = ["note","notes","sourceCredit"]
    for r in to_remove:
        for p in soup.find_all(r):
            p.decompose()
    file.write(str(soup))
    file.close()
    
def parse26(source26,sectionsToUse,outputTitle):
    introtext="""<?xml version="1.0" encoding="utf-8"?>
    <?xml-stylesheet type="text/css" href="usctitle.css"?><uscDoc identifier="/us/usc/t26" xml:lang="en" xmlns="http://xml.house.gov/schemas/uslm/1.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://xml.house.gov/schemas/uslm/1.0 USLM-1.0.15.xsd">
    <main>
    """
    
    endingtext = """
    </main>
    </uscDoc>
    """    

    df=pd.read_excel(sectionsToUse)
    
    code_sections_list = df['Code'].tolist()
    subsections_list=df['Subsection'].tolist()
    
    file_title = outputTitle
     
       
    file = open(file_title, 'w',encoding='utf-8')
    
    file.write(introtext)
    
    with open(source26,encoding='utf8') as fp:
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

def createRegsFile(sourceRegsTitle):
    #URL: https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-1 , save the HTML file
    # for the 15a installment sale regs, https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-15a
    # For the 301 regs, go to here and save the relevant regs with the appropriate titles (see below): https://www.ecfr.gov/current/title-26/chapter-I/subchapter-F/part-301/subpart-ECFR5ffaf3310af6b61
    
    #string together all the relevant regulations
    filenames = ['title-26-reg.htm','title-26-reg-15a.htm']
    
    reg_string = ''
    
    for fname in filenames:
        print(fname)
        with open(fname,encoding='utf8') as infile:
            data = infile.read()
            reg_string = reg_string+data
        
    soup = BeautifulSoup(reg_string,'lxml')
    
    #get rid of the editorial notes
    for p in soup.find_all('div',attrs={"class":"editorial-note"}):
        p.decompose()
    
    file = open(sourceRegsTitle,'w',encoding='utf8')
    file.write(str(soup))
    file.close()
        
def parseRegs(sourceRegs,sectionsToUse,outputTitle):

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
    df=pd.read_excel(sectionsToUse)
    
    code_sections_list = df['Regulation'].tolist()
    subsections_list=df['Subsection'].tolist()
    
    file_title = outputTitle
        
    file = open(file_title, 'w',encoding='utf-8')
    
    file.write(introtext)
    
    
    with open(sourceRegs,encoding='utf8') as fp:
        soup = BeautifulSoup(fp,'lxml')
    
    
    #include the relevant sections
    for item in code_sections_list:
        index_item = code_sections_list.index(item)
        section_identifier=f"{item}"
        section_to_add = soup.find('div',attrs={"class":"section",'id':section_identifier})
        selected_subsections = subsections_list[index_item]
        if  selected_subsections == 'all':
            file.write(str(section_to_add))
        else:
            list_selected = list(selected_subsections.split(','))
            section_num_and_title = section_to_add.find('h4')
            file.write(str(section_num_and_title))
            for item in list_selected:
                for element in item:
                    subsection_identifier = f"p-{section_identifier}({element})"
                subsection_to_add = soup.find('div',{'id':subsection_identifier})
                file.write(str(subsection_to_add))
    
    file.write(endtext)
    
    file.close()

def createCode(source26,Sec26NoNotesTitle,codeSectionsToUse,codeOutputTitle):
    parse26(source26,codeSectionsToUse,Sec26NoNotesTitle)
    create26NoNotes(Sec26NoNotesTitle,codeOutputTitle)

def createRegs(sourceRegsTitle,regSectionsToUse,regOutputTitle):
    createRegsFile(sourceRegsTitle)
    parseRegs(sourceRegsTitle,regSectionsToUse,regOutputTitle)

def createCodeAndRegs(source26,Sec26NoNotesTitle,codeSectionsToUse,codeOutputTitle,sourceRegsTitle,regSectionsToUse,regOutputTitle):
    createCode(source26,Sec26NoNotesTitle,codeSectionsToUse,codeOutputTitle)
    parseRegs(sourceRegsTitle,regSectionsToUse,regOutputTitle)
    
#createCodeAndRegs('usc26.xml','Section26NoNotes.xml','codesectionstouse.xlsx','SelectedSections20230226.xml','title-26-reg.htm','regsectionstouse.xlsx','SelectedRegulations20230223.html')

createRegs('title-26-all.htm','regsectionstouse.xlsx','SelectedRegulations20230226.html')
#createCode('usc26.xml','Section26NoNotes.xml','codesectionstousepartnership.xlsx','SelectedPshipSections20221226.xml')