# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:17:14 2019

@author: Lawsky
"""

import functionmodules as fm

FAQ = '''**Frequently Asked Questions**  

**Q: What does this website do?** <br>
A: It generates multiple-choice practice problems for federal income tax and partnership tax. The problems are a random selection of facts, names, and randomly (but thoughtfully) generated numbers about a range of federal income tax topics and partnership tax topics. You decide whether you want to focus on federal income tax or partnership tax, and then you can pick a particular topic within that subject, or you can have the website to pick both a topic and problem within that subject at random. 

**Q: Are the answers also random?** <br>
A: Mostly, no. The multiple-choice answers are based on mistakes people commonly make (though the list of possible answers may include one or more random answer ).

**Q: What happens once I pick an answer?** <br>
A: If you pick a wrong answer, the website usually provides a substantive hint about what you did wrong. A right answer usually returns a full explanation. In many of the explanations of answers both right and wrong, there is a link to the relevant code section. 

**Q: Do the questions repeat?**<br>
A: Eventually--there are not an infinite number of problems--but there are a *lot* of different problems. Setting aside the numbers' changing, which doesn't necessarily provide conceptually different questions, different types of problems toggle a bunch of different facts and relationships between the numbers, all of which change the problem conceptually. For example, for like-kind exchanges, there are five different facts than can toggle (asset is personal use or business use, whether there is debt relief and whom that debt relief favors (someone who provides boot or not), etc.) and four different questions. For installment sales there are even more toggles; for unrestricted property as compensation, many fewer. 

**Q: What is this *for*?**<br>
A: Whatever you want. A professor can use to generate problems for teaching or to give students direct access to it; a student can use it to practice for tax class--whatever works for you. The website is free and is made available under a [Creative Commons Attribution-ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/), which means, roughly, that you can share this or use it for any purpose, just so long as you give appropriate credit, distribute the material so other people can use it under the same terms, and don't create any additional restrictions.

**Q: Does the website take into account inflation adjustments?**<br>
A: Yes. Problems, rate graphs, and rate calculations take into account inflation adjustments.

**Q: What is the point of the Statutes page?** <br>
A: The Statutes page allows people to practice reading and understanding language from the Internal Revenue Code. You don't need any tax knowledge to work these problems, and the problems aren't meant to teach substantive law. Rather, the Statutes page is to help people get more comfortable reading and applying language from the Code.

**Q: But there are a lot of other parts of reading a statute. This is just, like, little word problems.**<br>
A: Yes! The Statutes page may help develop the skill of translating a small amount of technical language into a formula, and it may give students more confidence when it comes to tackling the statute. The Statutes page does not help develop the skill of, for example, following cross-references, or understanding how different portions of the Code interact with each other, or applying canons of construction, or any of the many, many other skills that go into reading, understanding, and interpreting the Code.

**Q: I downloaded a quiz answer sheet, and the file is called "federalincometaxquiz" (normal) but then there is a really long string of numbers after that (less normal)...what is that string of numbers?**<br>
A: That is the [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) of the moment you generated that answer sheet. You can translate that into a more comprehensible date by entering that number into a [converter](https://www.epochconverter.com/). For example, there's a file in my downloads called federalincometaxquiz.1685532778.362058.docx. When I put 1685532778.362058 into the converter, it tells me I generated that quiz on Wednesday, May 31, 2023, at 11:32:58.362 AM Greenwich Mean Time. This approach means, among other things, that every quiz answer sheet you download will have a unique filename.

**Q: I wish this FAQ were much, much longer.**<br>
A: I've got some [great news](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3876486) for you. 

**Q: I found a mistake! I have a suggestion!**<br>
A: If you find an error or have a suggestion, please [let me know](http://www.law.northwestern.edu/faculty/profiles/SarahLawsky/). 


'''

attribution = 'This website is created and maintained by [Sarah Lawsky](http://www.law.northwestern.edu/faculty/profiles/SarahLawsky/), a tax law professor at [Northwestern Pritzker School of Law](http://www.law.northwestern.edu/). The website uses [Dash](https://plot.ly/dash/) and [Python](https://www.python.org/) and is freely available under the [Creative Commons Attribution-ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/).'

quiz_explanation = '''This page generates quizzes for Federal Income Tax. These quizzes likely do not replicate the complexity of actual quizzes or tests you may take, but they may help you drill the basics. 

To take the quiz, enter the number of questions the quiz should have, up to 10; select topics; and click "Generate Quiz." You will receive that many questions, on those topics, generated from the same program that generates the problems on the [Practice Problems page](https://www.lawskypracticeproblems.org/). 

Select your answers for all the questions and then click "Submit Answers." 

The website will tell you how many you got right and supply the correct answers and explanations. You can download the problems and answer key, and you can reset the page to do another quiz.'''


problem_page_intro = f'''Assume that the law for {str(fm.current_year)} applies in all years.
      
Select the problem topic and click "Submit Topic." If no topic is selected, the website picks a random topic.
      
'''

partnership_addl_info = '''To the left of each topic is the number of the subsection of [Wootton & Lawsky, Partnership Taxation](https://www.amazon.com/Exam-Pro-Partnership-Taxation-Objective-ebook/dp/B082B9FBBP/) that corresponds to the topic.'''


codeandregsdownload = f'''
Download a [PDF of selected tax Code and regulation sections](/assets/SelectedCodeandRegSections.pdf) for Federal Income Tax for {fm.current_year}. The sections included in this book are probably, however, not the right sections for your particular class. Make your own Selected Sections book in just three steps!'''

codeandregs = f'''
**Q: What exactly is in this Selected Sections book?**<br>
A: This Selected Sections book includes 
* Certain sections and subsections of the Code and regulations, either the [sections and subsections I use in my class](/assets/CodeAndRegSectionsToUse.xlsx) or the items on the spreadsheet you've uploaded.
* an edited table of contents for the whole IRC,
* the current inflation-adjusting Revenue Procedure ({fm.current_rev_proc}), and 
* excerpts from Rev. Proc. 87-57, the depreciation tables.

**Q: Where is the content coming from?**<br>
A: The Code sections contained in this book are from the [Office of Law Revision Counsel](http://uscode.house.gov/download/download.shtml). The regulation sections are from the [eCFR](https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-1).

**Q: Why did you do this?**<br>
A: Internal Revenue Code and regulation sections are the most important reading for any federal income taxation course. There are four problems with commercial selected Code and regs books. First, commercial selected sections books are expensive: $100 or more for information that is freely available. Second, they are too long: they contain far more sections than any one class needs, because they are trying to meet the needs of a whole range of classes. Third, they are too short: it's very likely that any given professor will want to assign some sections that aren't in a commercially edited book. Fourth, they may go out of date quickly, as the law might change in any given year, and inflation adjustments do change year-to-year. 

In contrast, this Selected Sections is available for free; you can use this website to have the book include exactly the sections and subsections relevant for your class; and it is easy to update as the law and year change.

**Q:I like a hard copy better.**<br>
A: Me too. Luckily, in addition to the "printing out the PDF" option, there are a number of options for nicely-bound hard copies of PDFs print-on-demand for cost, maybe even including your school's bookstore or copy center. For example, you can [buy a bound hard copy of the Selected Sections PDF I linked to above](https://bit.ly/TaxSelectedSections) for cost at Lulu.com, just because I uploaded it there (it doesn't cost anything to upload it, and I don't get any money if you buy it).

**Q:What are those long strings of numbers in the file name of the Selected Sections book I downloaded?**<br>
A: That is the [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) of the moment you generated that Selected Sections book. You can translate that into a more comprehensible date by entering that number into a [converter](https://www.epochconverter.com/). For example, there's a file in my downloads called SelectedSections.1687277065.726598.pdf. When I put 1687277065.726598 into the converter, it tells me I generated that particular Selected Sections book on Tuesday, June 20, 2023 4:04:25.726 PM Greenwich Mean Time.'''

code_template_explanation = '''First, create an Excel spreadsheet listing the Code and regulation sections and subsections you want in your Selected Sections book, and format it so that the program can process it. The simplest way to do this is to download and modify [the spreadsheet with sections and subsections I use in my class](/assets/CodeAndRegSectionsToUse.xlsx)--essentially, use it as a template. (You can download the default spreadsheet by clicking on that link.) Here are some tips:
* The first worksheet of the spreadsheet includes your Code sections, and the second worksheet includes your Regs section.
* Leave the column names as they are: on the Code worksheet, the columns are "Code" and "Subsection"; on the Regs worksheet, the columns are "Regulation" and "Subsection".
* If you want to include all of the subsections for a section, put "all" in the "Subsection" column, or leave it blank.
* If you want to include only some of the subsections, put the ones you want to include in a list in the "Subsection" column, with a comma separating the subsections.
* It doesn't matter what order you enter the sections in; the book will generate in numerical order.
'''

code_upload_explanation = '''Second, upload the Excel spreadsheet with the Code and regulation sections and subsections that you want in your Selected Sections book. 

The computer will automatically start creating your book once you have uploaded your spreadsheet. When the book is ready, you will see a message below providing a link you can click to download your book.'''

be_patient = '''Be patient--the processing can take a minute or so. (The Code and regs are very long.) Do not click on anything else on this page while you are waiting.'''