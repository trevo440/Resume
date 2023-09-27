'''
Created on Sep 25, 2023

@author: trevo

TODO: Throw in random info into Job Desc from database-other-roles-with-the-same-title to "humanize" summary value
'''
#-----------------------------------------------------------------
import PyPDF2 as pdf
import reportlab as rl
from reportlab.pdfgen.canvas import Canvas
import sqlite3

#-----------------------------------------------------------------
#Database
#-----------------------------------------------------------------
conn = sqlite3.connect("Resume\\Collection.db", isolation_level=None)
cur = conn.cursor()

#-----------------------------------------------------------------
#Set parameters
#-----------------------------------------------------------------
COMPANY = ""
JOB_TITLE = ""
JOB_DESC = '''
'''.replace("'", "")
SKILL_LIST = '''
'''.replace("'","")
#----------UPDATE SQL---------------------------------------------
text = f"INSERT INTO jobInfo VALUES ('{COMPANY}', '{JOB_TITLE}', '{JOB_DESC}', '{SKILL_LIST}');"
cur.execute(text)
#-----------------------------------------------------------------
percent = 0.3

page_height = 792.0
page_width = 612.0
#construct-document
resume = Canvas(f"Resume\\Tewert-{JOB_TITLE}-{COMPANY}.pdf", pagesize=(page_width, page_height))
resume.setStrokeColor("#707070")
#-----------------------------------------------------------------
#header (static)
#-----------------------------------------------------------------
resume.setFont("Times-Bold", 18)
resume.drawString(72, page_height-72, f"Trevor Ewert - {JOB_TITLE}")

resume.drawInlineImage("./ln.png", page_width-(2*72), page_height-72, width=25, height=25, preserveAspectRatio=True)
resume.drawInlineImage("./gm-2.png", page_width-(1.5*72), page_height-73, width=30, height=30, preserveAspectRatio=True)

resume.line(72, 712, page_width-72, 712)
#-----------------------------------------------------------------
#professional experience (static)
#-----------------------------------------------------------------
resume.setFont("Times-Roman", 13)
resume.drawString(72, page_height-(72*1.4), "Professional Experience")
resume.line(72, 680, page_width-72, 680)
#-----------------------------------------------------------------
#(dynamic)
curr_head = 675
spacing = 12
#-----------------------------------------------------------------
#job 1
#-----------------------------------------------------------------
resume.setFont("Times-Bold", 10)
resume.drawString(72, curr_head-12, "DATA IMPLEMENTATION ENGINEER, 1UPHEALTH")
resume.setFont("Times-Italic", 11)
resume.drawString(72, curr_head-(spacing*2), "09/2022-06/2023")
resume.setFont("Times-Roman", 10)
resume.drawString(100, curr_head-(spacing*3), "• Create & Manage client-specific environments & data pipelines, ETL Non-FHIR data to HL7")
resume.drawString(100, curr_head-(spacing*4), "• Ownership of “Clinical Connectivity” initiative to focus on retrieving data direct-out-of-EMR")
resume.drawString(100, curr_head-(spacing*5), "• Tech Stack: AWS Suite: S3, RDS, Dynamo, ES, EC2, Cloudwatch, Apache NiFi, Postman, API,")
resume.drawString(100, curr_head-(spacing*6), "  Postgres, Python, SQL, Java, JSON, etc. In-house ETL built on Groovy Script")
resume.line(105, curr_head-(spacing*6 + 10), page_width-72, curr_head-(spacing*6 + 10))
#-----------------------------------------------------------------
#job 2
#-----------------------------------------------------------------
curr_head = curr_head- spacing*6 - 15

resume.setFont("Times-Bold", 10)
resume.drawString(72, curr_head-12, "DATA ENGINEER, CLEARSENSE")
resume.setFont("Times-Italic", 11)
resume.drawString(72, curr_head-(spacing*2), "07/2021 (Contract); 04/2022 (FTE); 09/2022")
resume.setFont("Times-Roman", 10)
resume.drawString(100, curr_head-(spacing*3), "• Working With Database Engines used to create accurate reports for archival services")
resume.drawString(100, curr_head-(spacing*4), "• ETL using Alteryx Designer and Python Dataframes, Report builds using JasperReports")
resume.drawString(100, curr_head-(spacing*5), "• Analytics from disk space/storage usage to schema mapping, info on patients & encounters")
resume.line(105, curr_head-(spacing*5 + 10), page_width-72, curr_head-(spacing*5 + 10))

#-----------------------------------------------------------------
#job 3
#-----------------------------------------------------------------
curr_head = curr_head - spacing*5 - 15

resume.setFont("Times-Bold", 10)
resume.drawString(72, curr_head-12, "DATA ENGINEER, OPTIMUM HEALTH IT")
resume.setFont("Times-Italic", 11)
resume.drawString(72, curr_head-(spacing*2), "04/2021 – 04/2022")
resume.setFont("Times-Roman", 10)
resume.drawString(100, curr_head-(spacing*3), "• 3-month Training covering topics related to Health IT, Architecture/Warehousing, Analytics, ETL")
resume.drawString(100, curr_head-(spacing*4), "• Programming languages including Python, SQL, Java, HTML, and JavaScript")
resume.drawString(100, curr_head-(spacing*5), "• Contractor - Data Engineer I with CLEARSENSE (see above for job details)")
resume.line(72, curr_head-(spacing*5 + 10), page_width-72, curr_head-(spacing*5 + 10))

#-----------------------------------------------------------------
#education
#-----------------------------------------------------------------
curr_head = curr_head - spacing*5 - 15

resume.setFont("Times-Roman", 13)
resume.drawString(72, curr_head - spacing-8, "Education")
resume.line(72, curr_head -spacing -18, page_width-72, curr_head- spacing -18)

curr_head = curr_head-spacing-23

resume.setFont("Times-Bold", 9)
resume.drawString(72, curr_head-12, "UNIVERSITY OF MINNESOTA DULUTH; BACHELOR OF ARTS: MANAGEMENT INFORMATION SYSTEMS")
resume.setFont("Times-Italic", 9)
resume.drawString(100, curr_head-(spacing*2), "08/2019-08/2021; cum laude ~ with distinction")

resume.setFont("Times-Bold", 9)
resume.drawString(72, curr_head-(spacing*4), "NORMANDALE COMMUNITY COLLEGE; ASSOCIATE OF ARTS: LIBERAL AND GENERAL STUDIES")
resume.setFont("Times-Italic", 9)
resume.drawString(100, curr_head-(spacing*5), "08/2017-05/2019; PSEO")

resume.setFont("Times-Bold", 9)
resume.drawString(72, curr_head-(spacing*7), "CONTINUED EDUCATION")
resume.setFont("Times-Roman", 9)
resume.drawString(100, curr_head-(spacing*8), "High Performance Leadership - Professional Development Academy, Issued Apr 2023")
resume.drawString(100, curr_head-(spacing*9), "Digital Health Certificate Program - CHIME, Issued Jun 2021")
resume.drawString(100, curr_head-(spacing*10), "Lean Six Sigma White Belt Certification - Baldrige Foundation, Issued Jun 2021")

resume.setFont("Times-Bold", 9)
resume.drawString(72, curr_head-(spacing*12), "UDEMY")
resume.setFont("Times-Roman", 9)
resume.drawString(100, curr_head-(spacing*13), "Java SE 8, Agile, Health Data, Data Analyst, Data Warehouse, Microsoft Excel w/ Power Query & DAX, SQL, Python,") 
resume.drawString(100, curr_head-(spacing*14), "Spring Boot, SwiftUI.")

resume.line(72, curr_head-(spacing*14 + 10), page_width-72, curr_head-(spacing*14 + 10))

#-----------------------------------------------------------------
#Projects
#-----------------------------------------------------------------
curr_head = curr_head-(spacing*14 + 10)

resume.setFont("Times-Roman", 13)
resume.drawString(72, curr_head - spacing-8, "Accomplishments")
resume.line(72, curr_head -spacing -18, page_width-72, curr_head- spacing -18)

curr_head = curr_head-spacing-23

resume.setFont("Times-Bold", 10)
resume.drawString(72, curr_head-12, "INITIATIVE: Create a Database Searching Tool")
resume.setFont("Times-Roman", 10)
resume.drawString(100, curr_head-(spacing*2), "• Used department-wide through installation into third party ETL applications (Alteryx)")
resume.drawString(100, curr_head-(spacing*3), "• UPPER and special character search. Meta-data, schema-level, and foreign key filtering")
resume.drawString(100, curr_head-(spacing*4), "• Application lifecycle management; Agile development. Integration & version control")
resume.line(105, curr_head-(spacing*4 + 10), page_width-72, curr_head-(spacing*4 + 10))

curr_head=curr_head-(spacing*4+10)

resume.setFont("Times-Bold", 10)
resume.drawString(72, curr_head-(spacing*2) + 5, "Department Python SME: 7+ Year(s) as a Python Hobbyist, 1+ Year(s) as an Xcode Dev")
resume.setFillColor("#707070")
resume.setFont("Times-Italic", 10)
resume.drawString(72, curr_head-(spacing*3) + 5, "Community Event Organizer for Chess Club")


#-----------------------------------------------------------------
#Role Summary
#-----------------------------------------------------------------
curr_head = 720
resume.showPage()
resume.setStrokeColor("#707070")


if JOB_DESC:

    resume.line(72, curr_head, page_width-72, curr_head)
    resume.setFont("Times-Roman", 13)
    resume.drawString(72, curr_head - spacing-8, "Role Description")
    resume.line(72, curr_head -spacing -18, page_width-72, curr_head- spacing -18)
    
    curr_head = curr_head-spacing - 18
    
    import spacy
    from spacy.lang.en.stop_words import STOP_WORDS
    from string import punctuation
    from heapq import nlargest
    
    def summarize(text, per):
        nlp = spacy.load('en_core_web_sm')
        doc= nlp(text)
        tokens=[token.text for token in doc]
        word_frequencies={}
        for word in doc:
            if word.text.lower() not in list(STOP_WORDS):
                if word.text.lower() not in punctuation:
                    if word.text not in word_frequencies.keys():
                        word_frequencies[word.text] = 1
                    else:
                        word_frequencies[word.text] += 1
        max_frequency=max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word]=word_frequencies[word]/max_frequency
        sentence_tokens= [sent for sent in doc.sents]
        sentence_scores = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if sent not in sentence_scores.keys():                            
                        sentence_scores[sent]=word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent]+=word_frequencies[word.text.lower()]
        select_length=int(len(sentence_tokens)*per)
        summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
        final_summary=[word.text for word in summary]
        summary=''.join(final_summary)
        return summary
    
    resume_text = summarize(JOB_DESC, percent)
    
    import textwrap
    import re
    resume.setFont("Times-Roman", 10)
    wrap_list = resume_text
    wrap_list = re.sub(' +', ' ', wrap_list).rstrip()
    wrap_list = [textwrap.fill(i, 110, fix_sentence_endings=True).replace('.', '\n') for i in wrap_list.replace('. ', '\n').split('\n')]
    i = 1
    
    master_list = []
    for item in wrap_list:
        for value in item.split('\n'):
            master_list.append(value)
            
    print(master_list)
    for item in master_list:
        if item not in ("", "\n", ):
            if item[-1] == ".":
                item = item[0:-1]
            if item[0].isupper():
                item = "• " + item
            else:
                item = "  " + item
            resume.drawString(72, curr_head-(spacing*i) + -6, item)
            i += 1
    
    curr_head = curr_head-(spacing*i) - 11
 
import random   
if SKILL_LIST or True:
    
    TECH_SKILL_DICT = {}
    with open(".\keywords.txt", "r") as f:
        TECH_SKILL_DICT = {x:round(random.uniform(7.0, 9.9), 1) for x in f.read().split("\n")}
    
    def common(a, skill_string):
        common = []
        for item in a:
            if item.lower() in skill_string.lower():
                common.append(item)
        return common
               
    tech = common(TECH_SKILL_DICT.keys(), SKILL_LIST)
    
    import random
    
    if len(tech) <= 4:
        tech += random.sample(TECH_SKILL_DICT.keys(), 2)
    if len(tech) >= 7: 
        tech = random.sample(tech, 6)
        
    
    tech = {k:v for k,v in TECH_SKILL_DICT.items() if k in tech}
    
    resume.line(72, curr_head, page_width-72, curr_head)
    resume.setFont("Times-Roman", 13)
    resume.drawString(72, curr_head - spacing-8, "Related Skills")
    resume.line(72, curr_head -spacing -18, page_width-72, curr_head- spacing -18)
    
    curr_head = curr_head - spacing - 18
    
    resume.setFont("Courier", 9)
    
    i = 1
    for k, v in tech.items():
        format_num = round(v)
        resume.drawString(72, curr_head - ( i*2*spacing), f"|{'=' * format_num}{' '*(10-format_num)}| {k} {v}/10")
        i += 1
    
#      rate on a single decimal scale, multiply by 10, add equal number of spaces [||||||||  ]     |-▐▐▐▐▐▐▐▐   -| Communication 7.7/10
#                                                                                                  |-▐▐▐▐▐▐     -| Listening 4.3/10
#                                                                                                  |-▐▐▐▐▐▐▐▐▐▐ -| Python 9/10
#-----------------------------------------------------------------
#Save contents
#-----------------------------------------------------------------
resume.save()
#-----------------------------------------------------------------
#update meta-info & add hyperlinks
#-----------------------------------------------------------------
reader = pdf.PdfReader(f"Resume\\Tewert-{JOB_TITLE}-{COMPANY}.pdf")
writer = pdf.PdfWriter()
writer.append_pages_from_reader(reader)
writer.add_metadata({"/Title": f"{JOB_TITLE} Resume, for {COMPANY}", 
                    "/Author":"Trevor Ewert",
                    "/AddInfo": "Some Sections of this Resume have been dynamically generated using NLP, custom designed software by Author \
                    To Learn More, view the project here: https://github.com/trevo440/Resume/blob/main/resume-updater.py"
                    })

writer.add_uri(0, "https://www.linkedin.com/in/trevor-ewert-24459a13b/",
    rect=(page_width-(2*72), page_height-72, page_width-(2*72)+25, page_height-72+25)
    )

writer.add_uri(0, "mailto:trevorewert01@gmail.com",
    rect=(page_width-(1.5*72), page_height-70, page_width-(1.5*72)+30, page_height-72+25)
    )

with open(f"C:\\Users\\trevo\\Downloads\\Resume\\Tewert-{JOB_TITLE}-{COMPANY}.pdf", "wb") as fp:
    writer.write(fp)
    
conn.close()
