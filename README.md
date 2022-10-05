Sarah Lawsky

October 2022

The goal here is to put together selected Code and regulations for a tax class. Here are the steps.

1. Download 26 USC from http://uscode.house.gov/download/download.shtml
2. Create a version of this with no annoying notes at the end by running [create26nonotes.py](https://github.com/slawsk/selectedSections/blob/main/create26nonotes.py)
3. Use an Excel file with the code sections you want -- the sample is in [codesectionstouse.xlsx](https://github.com/slawsk/selectedSections/blob/main/codesectionstouse.xlsx) - and run [parse26.py](https://github.com/slawsk/selectedSections/blob/main/parse26.py). This will create an XML file with the sections you want. 
4. Convert that XML file into a PDF.
5. Regulation time! Download URL: https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-1 , save the HTML file. For the 301 regs, go to here and save the relevant regs with the appropriate titles (see below): https://www.ecfr.gov/current/title-26/chapter-I/subchapter-F/part-301/subpart-ECFR5ffaf3310af6b61?toc=1
6. Run [parseregsfromhtml.py](https://github.com/slawsk/selectedSections/blob/main/parseregsfromhtml.py) - the sample source file for the regs you want to use is [regsectionstouse.xlsx](https://github.com/slawsk/selectedSections/blob/main/regsectionstouse.xlsx)
7. The result is HTML - covert that to a PDF however you want.
8. Now put the two PDFs together. I put an edited table of contents and also the up to date inflation adjusting Rev Proc at the beginning - I've added those PDFs to this file too in case you want to use them.
9. You can see a sample of what the completed version looks like in the [SelectedCodeandRegSectionsFall2022.pdf](https://github.com/slawsk/selectedSections/blob/main/SelectedCodeandRegSectionsFall2022.pdf) file.
