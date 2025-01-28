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

jd_prompt = """
"Given the following job description, extract the relevant sections and organize them into a valid json string format. The json should follow this specific structure:

Job Title:
company_name: The name of the company.
position: The name of the position listed.
Keywords:

technical: A list of technical keywords, each containing:
term: The technical keyword.
required_years: The minimum required time for showcasing the skill.
soft: A list of soft-skill keywords, each containing:
term: the soft-skill keyword.
required_years: The minimum required time for showcasing the skill.
Actions:

email_to: A recruiter/listed email to send your resume to.
survey: A list of any additional link(s) to forms related to the application. 
Statements:

quantifiable: A list of metrics which align with the responsibilities of this position.
ats: A condensed list of the responsibilities, as if one was currently working this role, to be listed in their resume.
Return only the json string with the specified keys and content. Use "Not provided" in place of any empty values.

Job Description: 
"""

intersect_prompt = """
Given the following Resume JSON, and Job Requirements JSON:
> IGNORE THE Actions of Requirements
> DO NOT ALTER THE STRUCTURE OR KEYS OF THE Resume JSON
> Intersect various work_experience responsibility statements with the following:
    > Job Requirements Quanifiable Metrics (use high-performance scores, and real numbers.)
    > Job Requirements Keywords (If required_years, attempt to place in a prior and current job)
> Add some amount of Job Requirements ATS Responsibilities statements
    > These can be in work_experience responsibility, summary, or projects.

Return only the updated Resume JSON json string with the specified keys and content. Use "Not provided" in place of any empty values.

"""

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

        
    def assess_jd(self, job_description) -> dict:
        job_description = self.cleaner.no_quote(job_description)
        instruct = jd_prompt + job_description

        completion = self.OpenAIclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Execute these instructions: {str(instruct)}" },
            ]
        )

        response = completion.choices[0].message.content 
        response = self.cleaner.ensure_gpt_format(response)

        return json.loads(response)
    
    def intersect(self, resume_sections, job_description) -> dict:
        instruct = intersect_prompt + "Resume JSON: " + str(resume_sections) \
            + "\n" + "Job Requirements JSON: " + str(job_description)

        completion = self.OpenAIclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Execute these instructions: {str(instruct)}" },
            ]
        )

        response = completion.choices[0].message.content 
        response = self.cleaner.ensure_gpt_format(response)

        return json.loads(response)

    
   