# ------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------

import json
import demjson3
from lib.data_cleaners import Cleanser


# ------------------------------------------------------------
# PROMPT(S)
# ------------------------------------------------------------
resume_prompt = """
"Given the following resume text, extract the relevant sections and organize them into a valid json string format. The json should follow this specific structure:

Contact Information:

full_name: The full name of the person.
phone_number: The phone number.
email: The email address.
linkedin: The LinkedIn profile URL.
website: The personal website or portfolio URL.
address: The address.
Summary or Objective:

summary: A list of summary or objective statements describing the candidate's career goals, skills, or background.
Skills:

skills: A list of skills, including programming languages, tools, and other technical or soft skills.
Work Experience:

work_experience: A list of job entries, each containing:
job_title: The job title.
company_name: The name of the company.
location: The location of the company.
dates_of_employment: The start and end dates of employment.
responsibilities: A list of job responsibilities.
Education:

education: A list of educational qualifications, each containing:
degree: The degree obtained.
institution_name: The name of the institution.
location: The location of the institution.
graduation_date: The date of graduation.
Certifications:

certifications: A list of certifications, each containing:
certification_name: The name of the certification.
issuing_organization: The name of the organization that issued the certification.
date_issued: The date the certification was issued.
Projects:

projects: A list of projects, each containing:
project_title: The title of the project.
description: A brief description of the project.
technologies_used: A list of technologies used in the project.
project_link: A URL to the project's repository or demo (if applicable).
Awards and Honors:

awards: A list of awards, each containing:
award_name: The name of the award.
issuing_organization: The organization that issued the award.
date_awarded: The date the award was given.
Volunteer Experience:

volunteer_experience: A list of volunteer positions, each containing:
role_title: The title of the volunteer position.
organization_name: The name of the organization.
location: The location of the organization.
dates_of_service: The dates the person served as a volunteer.
responsibilities: A list of responsibilities held during the volunteer position.
Languages:

languages: A list of languages spoken, each containing:
language_name: The name of the language.
proficiency_level: The level of proficiency in the language (e.g., fluent, intermediate).
Publications:

publications: A list of publications, each containing:
publication_title: The title of the publication.
publication_source: The source where the publication appeared (e.g., journal, website).
date_published: The date of publication.
publication_link: A URL to the publication (if applicable).
Return only the json string with the specified keys and content. Use "Not provided" in place of any empty values.

Resume Text: 
"""

jd_instructions = [
    {
        "task": "Utilize this job description to produce values that will help get a candidate through an ATS, without including niche-industry-specifics.",
        "details": "Your response should fit into a Python dictionary of \
                    {'keywords': ['keyword_1', 'keyword_phrase 2', etc.], \
                    'job_title': 'name_of_job', \
                    'job_task': {'JOB_TO_USE_1 (get this from supplied jobs above)': ['phrased_for_missing_details', etc], 'JOB_TO_USE_2': ['other_phrases_for_missing_details', etc]} \
                    } - limit job tasks to 3, and try to make sure there is enough context to help improve with scoring. Format the job tasks as sentences, with capital first letter and ending with a period."
    },
    {
        "task": "GPT Response to be usable in programming loop",
        "details": "Return the Python dictionary in the correct format only and NOTHING ELSE. Include ALL keys, even if they are empty."
    },
] 

class PromptManager:

    def __init__(self, OpenAIclient):
        self.OpenAIclient = OpenAIclient
        self.cleaner = Cleanser()

    def pull_resume(self, resume_text) -> dict:
        resume_text = self.cleaner.no_quote(resume_text)
        instruct = resume_prompt + resume_text + """\n\n{
            "task": "GPT Response to be usable in programming loop",\
            "details": "Return a valid json string in the correct format only and NOTHING ELSE. Include ALL keys, even if they are empty." \
        },"""
        completion = self.OpenAIclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": instruct},
            ]
        )
        response = completion.choices[0].message.content 
        response = self.cleaner.ensure_gpt_format(response)
        data = demjson3.decode(response, strict=False)

        return data

        
    def assess_jd(self, resume_text, job_description) -> dict:
        jd_instructions.append(
            {
                "resume_text": resume_text,
                "job_description": job_description
            }
        )

        completion = self.OpenAIclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Execute these instructions: {str(jd_instructions)}" },
            ]
        )

        response = completion.choices[0].message.content 
        response = response.strip("```python").strip("```").replace("'", '"')
        return json.loads(response)

    
   