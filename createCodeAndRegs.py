# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 05:59:26 2022

@author: Sarah
"""

from bs4 import BeautifulSoup
import pandas as pd
import os
import functionmodules as fm
import convertfile
import cchardet
import time
import re
import fitz
import json

current_year = fm.current_year

import pdfkit

all_code_title_xml = f'CodeNoNotes_{current_year}.xml'
all_code_title_html = f'CodeNoNotes_{current_year}.html'
all_regs_title = f'RegsNoNotes_{current_year}.html'

    
begin_no_range_1 = 611
end_no_range_1 = 700

begin_no_range_2 = 801
end_no_range_2 = 861
   
begin_no_range_3 = 1352
end_no_range_3 = 1411

begin_no_range_4 = 2001
end_no_range_4 = 6000

begin_no_range_5 = 6300
end_no_range_5 = 7655

absolute_max = 7702

def find_the_code_section(x):
    return x.split('.', 1)[1].split('-',1)[0]

def find_code_for_usc_26(x):
    return x.rsplit('/', 1)[1][1:]

def find_the_number(x):
    if isinstance(x, int):
        return x
    else:
        return int(re.sub("[^0-9]", "", x))

###AT LEAST ANNUALLY, OR WHEN LAW CHANGES
###Download the files for the code and regulations.
###After downloading files for regulations, fix the problem in 1.704-2(m) and 1.751-1(g) that the /div is in the wrong place and the regulations don't print.
###Run create_clean_files()
###Add the current updated Revenue Procedure to FilesForBook
###Update the introduction to FilesForBook (this can be automated to some extent)

#TO RUN ANNUALLY

def create26NoNotes():
    #URL: https://uscode.house.gov/download/download.shtml
    #The specific URL for Title 26 is https://uscode.house.gov/download/releasepoints/us/pl/117/214/xml_usc26@117-214.zip
    #file = open(all_code_title_xml, 'w',encoding='utf-8')
    with open('USC_26_New/GovernmentDownloads/usc26.xml',encoding='utf8') as fp:
        soup = BeautifulSoup(fp,'xml')
    to_remove = ["note","notes","sourceCredit"]
    for r in to_remove:
        for p in soup.find_all(r):
            p.decompose()
            
    div_elements = soup.find_all('section')
    div_library={}
    for div in div_elements:
        
        div_id = find_the_number(find_code_for_usc_26(div.get("identifier"))) # Get the ID attribute as an integer (default to 0 if ID is missing or not numeric)

        if (div_id >= begin_no_range_1 and div_id < end_no_range_1) or (div_id >= begin_no_range_2 and div_id < end_no_range_2) or (div_id >= begin_no_range_3 and div_id < end_no_range_3) or (div_id >= begin_no_range_4 and div_id < end_no_range_4) or (div_id >= begin_no_range_5 and div_id < end_no_range_5) or div_id > absolute_max :
                    div.decompose()  # Remove the div element
    
        else:
            
            section_number = div.num
            section_title = div.heading
            section_number_and_title = f"<section>{section_number}{section_title}</section>"
            
            subsection_elements = div.find_all('subsection')
            new_dict = {}
            new_dict['num_title_string']=section_number_and_title
            
            
            if subsection_elements:
                for item in subsection_elements:
                    subsection_number = item.get("identifier").rsplit('/', 1)[1]
                    new_dict[subsection_number]=str(item)
            
            else:
                for tag in div.find_all(['num', 'heading']):
                    tag.decompose()
                new_dict['all']=str(div)
            
            div_library[find_code_for_usc_26(div.get("identifier"))]=new_dict
    
    with open('CodeDictionary.txt','w',encoding='utf-8') as txt_file:
       txt_file.write(json.dumps(div_library))

#this creates the Regs files with no notes; use this as the input for creating the Code and regs. Run this annually.
def createRegsFile():
    #URL: https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-1 , save the HTML file
    # for the 15a installment sale regs, https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-15a
    # For the 301 regs, go to here and save the relevant regs with the appropriate titles (see below): https://www.ecfr.gov/current/title-26/chapter-I/subchapter-F/part-301/subpart-ECFR5ffaf3310af6b61
    
    #string together all the relevant regulations
    reg_string = ''
    directory = 'USC_26_New/GovernmentDownloads/RegFiles'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        with open(f,encoding='utf8') as infile:
            data = infile.read()
            reg_string = reg_string+data
        
    soup = BeautifulSoup(reg_string,'lxml')
    
    #get rid of the editorial notes
    for p in soup.find_all('div',attrs={"class":"editorial-note"}):
        p.decompose()


    div_library = {}
    div_elements = soup.find_all("div", attrs={"class": "section"})
    for div in div_elements:
        div_id = find_the_number(find_the_code_section(div.get("id"))) # Get the ID attribute as an integer (default to 0 if ID is missing or not numeric)

        if (div_id >= begin_no_range_1 and div_id < end_no_range_1) or (div_id >= begin_no_range_2 and div_id < end_no_range_2) or (div_id >= begin_no_range_3 and div_id < end_no_range_3) or (div_id >= begin_no_range_4 and div_id < end_no_range_4) or (div_id >= begin_no_range_5 and div_id < end_no_range_5) or div_id > absolute_max :
            div.decompose()  # Remove the div element
            
        else:
            div_library[str(div.get("id"))]=str(div) 

    with open('RegDictionary.txt','w',encoding='utf-8') as txt_file:
        txt_file.write(json.dumps(div_library))
    

def create_clean_files():
    create26NoNotes()
    createRegsFile()

#Pull the sections that you want from the code and the regs. Run these on the files that have no notes, that you have created by running create_clean_files  

def remove_spaces(x):
    if isinstance(x, str):
        return x.replace(" ","")
    else:
        return 'all'

def process_code_excel(sectionsToUse):
    code_df=pd.read_excel(sectionsToUse,sheet_name = 0)
    
    #get rid of empty rows
    code_df = code_df[code_df['Code'].notna()]
    
    
    #remove spaces from the subsections list
    code_df['SubsectionClean']=code_df['Subsection'].apply(lambda x: remove_spaces(x) )
    
    #sort the columns, noting that some of them are numbers and some are strings
    code_df['NumberToSort']=code_df['Code'].apply(lambda x: find_the_number(x))
    
    code_df = code_df.sort_values(by=['NumberToSort'])
    
    return code_df

def process_regs_excel(sectionsToUse):
    
    regs_df=pd.read_excel(sectionsToUse,sheet_name = 1)
    
    #get rid of empty rows
  
    regs_df = regs_df[regs_df['Regulation'].notna()]
    
    #get the sections and specific reg from the overall regulation
    regs_df['Intro']=regs_df['Regulation'].apply(lambda x: x.split('.', 1)[0])
    regs_df['Section']=regs_df['Regulation'].apply(lambda x: x.split('.', 1)[1].split('-',1)[0])
    regs_df['Specific']=regs_df['Regulation'].apply(lambda x: int(x.split('.', 1)[1].split('-',1)[1]))

    #remove spaces from the subsections list
    regs_df['SubsectionClean']=regs_df['Subsection'].apply(lambda x: remove_spaces(x) )
    
    #sort the columns, noting that some of them are numbers and some are strings
    regs_df['NumberToSort']=regs_df['Section'].apply(lambda x: find_the_number(x))
     
    regs_df = regs_df.sort_values(by=['NumberToSort','Specific'])
 
    
    return regs_df

def parse26(sectionsToUse,outputTitle):
   
    introtext = '<root>'
    endingtext = '</root>'
   
    df=process_code_excel(sectionsToUse)
    
    code_sections_list = df['Code'].tolist()
    subsections_list=df['SubsectionClean'].tolist()
    listified = [x.split(",") for x in subsections_list]

   
    lookupdict = dict(zip(code_sections_list,listified))
 
    with open('USC_26_New/CodeDictionary.txt','r',encoding='utf8') as fp:
        codestring = fp.read()
    code_dict = json.loads(codestring)
    
    textstring = ""
    #include the relevant sections
    for item in code_sections_list:
        subsection_dict = code_dict[str(item)]
        textstring += subsection_dict['num_title_string']
        selected_subsections = lookupdict[item]
        if selected_subsections[0] in ['all','All',""]:
            selected_subsections = list(subsection_dict.keys())[1:]
        for subsection in selected_subsections:
            textstring+=subsection_dict[subsection]
        
    file = open(outputTitle, 'w',encoding='utf-8')
    file.write(introtext)
    file.write(textstring)
    file.write(endingtext)
    file.close()



def replace_text_in_file(file_path, old_text, new_text):
    with open(file_path, 'r') as file:
        content = file.read()

    modified_content = content.replace(old_text, new_text)

    with open(file_path, 'w') as file:
        file.write(modified_content)    

def convert_to_html(inputtitle,outputtitle):
    convertfile.convert_file_to_html(inputtitle, outputtitle)
    
def convert_code_to_html(inputtitle,outputtitle,timenum):
    interim_title = f'saved_code/interim_{timenum}.html'
    
    convertfile.convert_file_to_html(inputtitle,interim_title)
    
    replace_dict = {'Thephaseoutamount':"The phaseout amount",'Thephaseoutpercentageis':'The phaseout percentage is', 'applicablerecovery': 'applicable recovery','periodis':'period is'}
    
    with open(interim_title, 'r',encoding='utf-8') as file:
        content = file.read()
    
    for item in replace_dict.keys():
        content = content.replace(item,replace_dict[item])
    
    with open(outputtitle, 'w',encoding='utf-8') as file:
        file.write(content)   
        
        
def parseRegs(sectionsToUse,outputTitle):

    #create the intro and endtext that allows the css file
    introtext = """<!doctype html>
    <html>
      <head>
      <meta charset="UTF-8">
        <link href="../USC_26_New/regsStyle.css" rel="stylesheet" />
      </head>
      <body>"""
      
    endtext = """  </body>
    </html>"""
    
    
    #create the file
    df=process_regs_excel(sectionsToUse)
    
    reg_sections_list = df['Regulation'].tolist()
    subsections_list=df['SubsectionClean'].tolist()
    listified = [x.split(",") for x in subsections_list]

    lookupdict = dict(zip(reg_sections_list,listified))
   
    with open('USC_26_New/RegDictionary.txt','r',encoding='utf8') as fp:
        regstring = fp.read()
    reg_dict = json.loads(regstring)
    
    textstring = introtext
    #include the relevant sections
    for item in reg_sections_list:
        selected_subsections = lookupdict[item]
        if selected_subsections[0] in ['all','All',""]:        
            textstring += reg_dict[item]
        else:
            soup = BeautifulSoup(reg_dict[item],'lxml')
            section_identifier=f"{item}"
            section_num_and_title = soup.find('h4')
            textstring += (str(section_num_and_title))
            for subsection in selected_subsections:
                subsection_identifier = f"p-{section_identifier}({subsection})"
                subsection_to_add = soup.find('div',{'id':subsection_identifier})
                textstring += (str(subsection_to_add))
    
    textstring += endtext
        
    file = open(outputTitle, 'w',encoding='utf-8')
    file.write(textstring)
    file.close()

def createSelectedCodeRegsHTML(sectionsToUse,timenum):
    parse26(sectionsToUse,f'saved_code/codefillertitle.{timenum}.xml')
    convert_code_to_html(f'saved_code/codefillertitle.{timenum}.xml',f'saved_code/codefillertitle.{timenum}.html',f'{timenum}')
    parseRegs(sectionsToUse,f'saved_code/regfillertitle.{timenum}.html')

def convert_to_pdf(input_html, output_pdf):
    options = {
  "enable-local-file-access": None,
  'encoding':'UTF-8',
  'dpi':200,
  'page-size': 'Letter',
  'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'minimum-font-size': '22',
    
}
    # Convert to PDF with pdfkit
    pdfkit.from_file(input_html, output_pdf,options=options)

def add_page_numbers(input_path, output_path):
    # Open the PDF file
    pdf = fitz.open(input_path)
    
    font_size = 10  # Replace with your desired font size
    font_name = "TiRo"

    # Iterate over each page
    for i, page in enumerate(pdf):
        #page_number = i + 1  
        # Get the page number
        if i >= 2:
            page_number = i - 1 # The idea here is actually i + 1 (because i starts at 0) - 2 (because we are skipping the first two pages)

        # Get the dimensions of the page
            page_width = page.rect.width
            page_height = page.rect.height
    
            # Calculate the position for the page number
            x = page_width / 2 - 20  # Adjust the position horizontally
            y = page_height - 20  # Adjust the position vertically
    
            # Create a new annotation object for the page number
            annot = page.add_freetext_annot((x, y, x + 40, y + 20), str(page_number))
            
            annot.update(fontname=font_name, fontsize=font_size)

    # Save the modified PDF to the output path
    pdf.save(output_path)
    pdf.close()

def merge_pdfs(file_paths, output_path):
    merger = fitz.open()

    for file_path in file_paths:
        pdf = fitz.open(file_path)
        merger.insert_pdf(pdf)

    merger.save(f'{output_path}.pdf')
    merger.close()  

def create_code_book(bookname,sectionsToUse,timenum):
    
    #create the HTML files with just the code and regulation sections that you want
    
    
    createSelectedCodeRegsHTML(sectionsToUse,timenum)
    code_name = f'saved_code/04B currentcode.{timenum}.pdf'
    reg_name = f'saved_code/05B currentregs.{timenum}.pdf'
    #convert the code html to PDF
    
    convert_to_pdf(f'saved_code/codefillertitle.{timenum}.html',code_name) 
    
   
   
    #convert the reg html to PDF
    convert_to_pdf(f'saved_code/regfillertitle.{timenum}.html',reg_name)
    
    path_short = 'USC_26_New/FilesForBook'    
    dir_list = sorted(os.listdir(path_short))
    
    dir_list_2 = [f'{path_short}/{x}' for x in dir_list]
    
    dir_list_2.insert(-1,code_name)
    dir_list_2.append(reg_name)
    
    #merge all the PDFs to create the whole book   
    merge_pdfs(dir_list_2,f'saved_code/nopagenumbers.{timenum}')

    #add the page numbers    
    add_page_numbers(f'saved_code/nopagenumbers.{timenum}.pdf', f'{bookname}.pdf')
    
# this function is if you want to play around with this without generating the whole files first--it's just checking to see what the merger version looks like
def create_book_from_files(code_html,reg_html):
    code_name = 'saved_code/04B currentcode.pdf'
    reg_name = 'saved_code/05B currentregs.pdf'
    #convert the code html to PDF
    
    convert_to_pdf(code_html,code_name) 
    
    #convert the reg html to PDF
    
    convert_to_pdf(reg_html,reg_name)
    
    path_short = 'USC_26_New/FilesForBook'    
    dir_list = sorted(os.listdir(path_short))
    
    dir_list_2 = [f'{path_short}/{x}' for x in dir_list]
    
    dir_list_2.insert(-1,code_name)
    dir_list_2.append(reg_name)
    
    #merge all the PDFs to create the whole book
    
    merge_pdfs(dir_list_2,'pdftitle')


   

#convert_code_to_html('saved_code/codehtmltest.xml','saved_code/codehtmltest2.html','12356')
 
#parse26('USC_26_New/CodeAndRegSectionsToUse.xlsx','codefillertitle.xml')
#convert_code_to_html('codefillertitle.xml','codefillertitle.html',6)
#create26NoNotes()
  
#createCodeAndRegs('usc26.xml','Section26NoNotes.xml','codesectionstouse.xlsx','SelectedSections20230226.xml','title-26-reg.htm','regsectionstouse.xlsx','SelectedRegulations20230223.html')

#createRegs('title-26-all.htm','regsectionstouse.xlsx','SelectedRegulations20230226.html')
#createCode('usc26.xml','Section26NoNotes.xml','codesectionstousepartnership.xlsx','SelectedPshipSections20221226.xml')

#createRegsFile()