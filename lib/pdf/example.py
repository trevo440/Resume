from flask import render_template
from lib.pdf.example_data import example as res

def view_example(version):
    contact_information = res['Contact Information']
    summary_or_objective = res['Summary or Objective']
    skills = res['Skills']
    work_experience = res['Work Experience']
    education = res['Education']
    certifications = res['Certifications']
    projects = res['Projects']
    awards_and_honors = res['Awards and Honors']
    volunteer_experience = res['Volunteer Experience']
    languages = res['Languages']
    publications = res['Publications']

    return render_template(
        f'styled_resumes/{version}.html', 
        contact_information = contact_information,
        summary_or_objective = summary_or_objective,
        skills = skills,
        work_experience = work_experience,
        education = education,
        certifications = certifications,
        projects = projects,
        awards_and_honors = awards_and_honors,
        volunteer_experience = volunteer_experience,
        languages = languages,
        publications = publications
    )