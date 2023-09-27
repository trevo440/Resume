'''
Created on Sep 27, 2023

@author: trevo
'''
import sqlite3
#-----------------------------------------------------------------
#Database
#-----------------------------------------------------------------
conn = sqlite3.connect("C:\\Users\\trevo\\Downloads\\Resume\\Collection.db", isolation_level=None)
cur = conn.cursor()


import re
cur.execute("Select Skills from jobInfo")
key_skills = re.sub(r'[^\x00-\x7F]', ' ', re.sub("[0-9]", "", "\n".join([x[0] for x in cur.fetchall() if x[0] is not None]).replace("\n", " ")))
#----------------------------------------------------------------
#scoring function
#----------------------------------------------------------------
from rake_nltk import Rake

r = Rake(max_length=4)

r.extract_keywords_from_text(key_skills)
restrict_words = ("etc", "weve", "sound", "thorough", "also", "companies", "working", "degree", "one",
                  "experience", "including", "must", "part", "world", "well", "year", "trusted", "around", "specifically", "work", 
                  "apply", "object", "strong", "university", "proficiency"
                  )

key_dict = {x[1].replace(",", "").replace(".","").replace(")", "").replace("skills", ""):x[0] for x in r.get_ranked_phrases_with_scores() if 1 < x[0] <= 7 and not any(value in x[1] for value in restrict_words)}

i = 1
for k, v in key_dict.items():
    print(f"{i} | {k}:{v}")
    i += 1
