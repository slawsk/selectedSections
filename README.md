Sarah Lawsky / May 2023

The goal here is to put together selected Code and regulations for a tax class.

The problem I was trying to solve is that selected sections Internal Revenue Code and accompanying regulations are key reading for tax courses. There are four problems with commercial selected code and regs books. First, they are expensive: $100 or more for information that is freely available. Second, they are too long: they contain far more sections than any one class needs, because they are trying to meet the needs of a whole range of classes. Third, they are too short: it's very likely that any given professor will want to assign some sections that aren't in a commercially edited book. Fourth, they may go out of date quickly, as the law might change in any given year, and inflation adjustments do change year-to-year.

This program pulls exactly the Code and regulation sections and subsections you want. The notes at the end of the sections are automatically removed. You can  give the students the opportunity to download the full PDF and/or upload it to a self-publishing website like Lulu.com to let them buy if for cost if they prefer a hard copy. Generate a new book for each semester, to stay up to date, and generate different books for different tax classes (basic tax v. partnership tax, etc.). 

To run the program: 

1. Create Excel spreadsheets to provide the information in the format the program can recognize. Use different spreadsheets for the code and the regs. The samples for the [code](https://github.com/slawsk/selectedSections/blob/main/codesectionstouse.xlsx) and [regs](https://github.com/slawsk/selectedSections/blob/main/regsectionstouse.xlsx) have the right format.

2. Download the XML for 26 USC from http://uscode.house.gov/download/download.shtml 

3. Download the relevant regulations in HTML  from https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-1 and, for the 301 regs, https://www.ecfr.gov/current/title-26/chapter-I/subchapter-F/part-301/subpart-ECFR5ffaf3310af6b61?toc=1

4. Run the program in [createCodeandRegs.py](https://github.com/slawsk/selectedSections/blob/main/createCodeAndRegs.py)

The output of this program will be an XML file (for the Code) and an HTML file (for the regs). You will need to convert those files to PDF and stitch them together. You can also download the relevant CSS files from the websites above; I've modified the CSS files I have in this repository to style the documents how I like them.

When I create the selected sections for my course, I also put (1) an [edited table of contents for the whole IRC](https://github.com/slawsk/selectedSections/blob/main/TOCCodeEdited.pdf), (2) the up-to-date inflation-adjusting Revenue Procedure ([2023](https://github.com/slawsk/selectedSections/blob/main/revProcInflation2023.pdf)), and (3) for basic tax, excerpts from Rev. Proc. 87-57, the depreciation tables.

Here's a [a sample of what the completed version could look like--this is for 2023 basic tax classes](https://github.com/slawsk/selectedSections/blob/main/SelectedCodeandRegSectionsFall2022.pdf).

And here's a sample for [Partnership Tax for 2023](https://github.com/slawsk/selectedSections/blob/main/SelectedSectionsPartnershipCodeRegs2023ToUpload.pdf).
