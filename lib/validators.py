import bleach

class DefaultsRM:
    contact = {
        "full_name": "Not provided",
        "phone_number": "Not provided",
        "email": "Not provided",
        "linkedin": "Not provided",
        "website": "Not provided",
        "address": "Not provided",
    }

    summary = {"summary": ["Not provided"]}
    skills = {"skills": ["Not provided"]}
    work_experience = {
        "work_experience": [{
            "job_title": "Not provided",
            "company_name": "Not provided",
            "location": "Not provided",
            "dates_of_employment": "Not provided",
            "responsibilities": ["Not provided"]
        }]
    }
    education = {
        "education": [{
            "degree": "Not provided",
            "institution_name": "Not provided",
            "location": "Not provided",
            "graduation_date": "Not provided"
        }]
    }

    certifications = {
        "certifications": [{
            "certification_name": "Not provided",
            "issuing_organization": "Not provided",
            "date_issued": "Not provided"
        }]
    }

    projects = {
        "projects": [{
            "project_title": "Not provided",
            "description": "Not provided",
            "technologies_used": ["Not provided"],
            "project_link": "Not provided"
        }]
    }

    awards = {
        "awards": [{
            "award_name": "Not provided",
            "issuing_organization": "Not provided",
            "date_awarded": "Not provided"
        }]
    }

    volunteer_experience = {
        "volunteer_experience": [{
            "role_title": "Not provided",
            "organization_name": "Not provided",
            "location": "Not provided",
            "dates_of_service": "Not provided",
            "responsibilities": ["Not provided"]
        }]
    }
    
    
    languages = {
        "languages": [{
            "language_name": "Not provided",
            "proficiency_level": "Not provided"
        }]
    }

    publications = {
        "publications": [{
            "publication_title": "Not provided",
            "publication_source": "Not provided",
            "date_published": "Not provided",
            "publication_link": "Not provided"
        }]
    }

    full = {
        "Contact Information": contact,
        "Summary or Objective": summary,
        "Skills": skills, 
        "Work Experience": work_experience,
        "Education": education,
        "Certifications": certifications,
        "Projects": projects,
        "Awards and Honors": awards,
        "Volunteer Experience": volunteer_experience,
        "Languages": languages,
        "Publications": publications 
    }

class DefaultsJD:
    job_title = {
        "company_name": "Not provided",
        "position": "Not provided",
    }

    keywords = {
        "technical": [{
            "term": "Not provided",
            "required_years": "Not provided"
        }],
        "soft": [{
            "term": "Not provided",
            "required_years": "Not provided"
        }]
    }

    actions = {
        "email_to": "Not provided",
        "survey": ["Not provided"]
    }

    statements = {
        "quanitfiable": ["Not provided"],
        "ats": ["Not provided"]
    }

    full = {
        "Job Title": job_title,
        "Keywords": keywords,
        "Actions": actions,
        "Statements": statements
    }

# SET DEFAULTS
DefaultRM = DefaultsRM()
DefaultJD = DefaultsJD()

# RESUME SECTION CLEANERS
def clean_rm_contact(contact):
    clean_contact = {}
    for key in DefaultRM.contact.keys():
        val = contact.get(key, None)
        if val is not None:
            clean_contact[key] = bleach.clean(str(val))
        else:
            clean_contact[key] = DefaultRM.contact[key]
    return clean_contact

def clean_rm_summary(summary):
    clean_summary_list = []
    summary_list = summary.get("summary", [])

    if not isinstance(summary_list, list):
        summary_list = DefaultRM.summary["summary"]
    for statement in summary_list:
        clean_summary_list.append(bleach.clean(str(statement)))
    
    return {"summary": clean_summary_list}

def clean_rm_skills(skills):
    clean_skills_list = []
    skills_list = skills.get("skills", [])

    if not isinstance(skills_list, list):
        skills_list = DefaultRM.skills["skills"]
    for skill in skills_list:
        clean_skills_list.append(bleach.clean(str(skill)))
    
    return {"skills": clean_skills_list}

def clean_rm_work_experience(work_experience):
    clean_work_experience_list = []
    work_experience_list = work_experience.get("work_experience", [])

    if not isinstance(work_experience_list, list):
        work_experience_list = DefaultRM.work_experience["work_experience"]
    
    for work_history in work_experience_list:
        if not isinstance(work_history, dict):
            continue
        job_title = bleach.clean(str(work_history.get('job_title', 'Not provided')))
        company_name = bleach.clean(str(work_history.get('company_name', 'Not provided')))
        location = bleach.clean(str(work_history.get('location', 'Not provided')))
        dates_of_employment = bleach.clean(str(work_history.get('dates_of_employment', 'Not provided')))
        responsibilities = [
            bleach.clean(str(responsibility)) for responsibility in \
            work_history.get("responsibilities", ["Not provided"])
        ]
        
        work_history_clean = {
            "job_title": job_title,
            "company_name": company_name,
            "location": location,
            "dates_of_employment": dates_of_employment,
            "responsibilities": responsibilities
        }
        
        clean_work_experience_list.append(work_history_clean)    
    
    return {"work_experience": clean_work_experience_list}

def clean_rm_education(education):
    clean_education_list = []
    education_list = education.get("education", [])

    if not isinstance(education_list, list):
        education_list = DefaultRM.education["education"]
    
    for edu in education_list:
        if not isinstance(edu, dict):
            continue
        degree = bleach.clean(str(edu.get('degree', 'Not provided')))
        institution_name = bleach.clean(str(edu.get('institution_name', 'Not provided')))
        location = bleach.clean(str(edu.get('location', 'Not provided')))
        graduation_date = bleach.clean(str(edu.get('graduation_date', 'Not provided')))
        
        edu_clean = {
            "degree": degree,
            "institution_name": institution_name,
            "location": location,
            "graduation_date": graduation_date,
        }
        
        clean_education_list.append(edu_clean)    
    
    return {"education": clean_education_list}

def clean_rm_certifications(certifications):
    clean_certifications_list = []
    certifications_list = certifications.get("certifications", [])

    if not isinstance(certifications_list, list):
        certifications_list = DefaultRM.certifications["certifications"]
    
    for cert in certifications_list:
        if not isinstance(cert, dict):
            continue
        certification_name = bleach.clean(str(cert.get('certification_name', 'Not provided')))
        issuing_organization = bleach.clean(str(cert.get('issuing_organization', 'Not provided')))
        date_issued = bleach.clean(str(cert.get('date_issued', 'Not provided')))
        cert_clean = {
            "certification_name": certification_name,
            "issuing_organization": issuing_organization,
            "date_issued": date_issued,
        }
        
        clean_certifications_list.append(cert_clean)    
    
    return {"certifications": clean_certifications_list}

def clean_rm_projects(projects):
    clean_projects_list = []
    projects_list = projects.get("projects", [])

    if not isinstance(projects_list, list):
        projects_list = DefaultRM.projects["projects"]
    
    for project in projects_list:
        if not isinstance(project, dict):
            continue

        project_title = bleach.clean(str(project.get('project_title', 'Not provided')))
        description = bleach.clean(str(project.get('description', 'Not provided')))
        technologies_used = [
            bleach.clean(str(technology)) for technology in \
            project.get("technologies_used", ["Not provided"])
        ]
        project_link = bleach.clean(str(project.get('project_link', 'Not provided')))
        
        project_clean = {
            "project_title": project_title,
            "description": description,
            "technologies_used": technologies_used,
            "project_link": project_link,
        }
        
        clean_projects_list.append(project_clean)    
    
    return {"projects": clean_projects_list}

def clean_rm_awards(awards):
    clean_awards_list = []
    awards_list = awards.get("awards", [])

    if not isinstance(awards_list, list):
        awards_list = DefaultRM.awards["awards"]
    
    for award in awards_list:
        if not isinstance(award, dict):
            continue
        award_name = bleach.clean(str(award.get('award_name', 'Not provided')))
        issuing_organization = bleach.clean(str(award.get('issuing_organization', 'Not provided')))
        date_awarded = bleach.clean(str(award.get('date_awarded', 'Not provided')))
        
        award_clean = {
            "award_name": award_name,
            "issuing_organization": issuing_organization,
            "date_awarded": date_awarded,
        }
        
        clean_awards_list.append(award_clean)    
    
    return {"awards": clean_awards_list}

def clean_rm_volunteer_experience(volunteer_experience):
    clean_volunteer_experience_list = []
    volunteer_experience_list = volunteer_experience.get("volunteer_experience", [])

    if not isinstance(volunteer_experience_list, list):
        volunteer_experience_list = DefaultRM.volunteer_experience["volunteer_experience"]
    
    for volunteer_history in volunteer_experience_list:
        if not isinstance(volunteer_history, dict):
            continue
        role_title = bleach.clean(str(volunteer_history.get('role_title', 'Not provided')))
        organization_name = bleach.clean(str(volunteer_history.get('organization_name', 'Not provided')))
        location = bleach.clean(str(volunteer_history.get('location', 'Not provided')))
        dates_of_service = bleach.clean(str(volunteer_history.get('dates_of_service', 'Not provided')))
        responsibilities = [
            bleach.clean(str(responsibility)) for responsibility in \
            volunteer_history.get("responsibilities", ["Not provided"])
        ]
        
        volunteer_history_clean = {
            "role_title": role_title,
            "organization_name": organization_name,
            "location": location,
            "dates_of_service": dates_of_service,
            "responsibilities": responsibilities
        }
        
        clean_volunteer_experience_list.append(volunteer_history_clean)    
    
    return {"volunteer_experience": clean_volunteer_experience_list}

def clean_rm_languages(languages):
    clean_languages_list = []
    languages_list = languages.get("languages", [])

    if not isinstance(languages_list, list):
        languages_list = DefaultRM.languages["languages"]
    
    for language in languages_list:
        if not isinstance(language, dict):
            continue
        language_name = bleach.clean(str(language.get('language_name', 'Not provided')))
        proficiency_level = bleach.clean(str(language.get('proficiency_level', 'Not provided')))
        
        language_clean = {
            "language_name": language_name,
            "proficiency_level": proficiency_level,
        }
        
        clean_languages_list.append(language_clean)    
    
    return {"languages": clean_languages_list}

def clean_rm_publications(publications):
    clean_publications_list = []
    publications_list = publications.get("publications", [])

    if not isinstance(publications_list, list):
        publications_list = DefaultRM.publications["publications"]
    
    for publication in publications_list:
        if not isinstance(publication, dict):
            continue
        publication_title = bleach.clean(str(publication.get('publication_title', 'Not provided')))
        publication_source = bleach.clean(str(publication.get('publication_source', 'Not provided')))
        date_published = bleach.clean(str(publication.get('date_published', 'Not provided')))
        publication_link = bleach.clean(str(publication.get('publication_link', 'Not provided')))
        
        publication_clean = {
            "publication_title": publication_title,
            "publication_source": publication_source,
            "date_published": date_published,
            "publication_link": publication_link,
        }
        
        clean_publications_list.append(publication_clean)    
    
    return {"publications": clean_publications_list}

def clean_jd_job_title(job_title):
    clean_job_title = {}
    for key in DefaultJD.job_title.keys():
        val = job_title.get(key, None)
        if val is not None:
            clean_job_title[key] = bleach.clean(str(val))
        else:
            clean_job_title[key] = DefaultRM.contact[key]
    return clean_job_title

def clean_jd_keywords(keywords):
    technical_clean = []
    soft_clean = []
    technical = keywords.get("technical", [{"term": "Not provided", "required_years": "Not provided"}])
    if not isinstance(technical, list):
        technical = [{"term": "Not provided", "required_years": "Not provided"}]

    soft = keywords.get("soft", [{"term": "Not provided", "required_years": "Not provided"}])
    if not isinstance(technical, list):
        soft = [{"term": "Not provided", "required_years": "Not provided"}]
    
    for dictionary_tech in technical:
        if not isinstance(dictionary_tech, dict):
            continue
        term = bleach.clean(str(dictionary_tech.get("term", "Not provided")))
        required_years = bleach.clean(str(dictionary_tech.get("required_years", "Not provided")))
        technical_clean.append({
            "term": term,
            "required_years": required_years
        })

    for dictionary_soft in soft:
        if not isinstance(dictionary_soft, dict):
            continue
        term_soft = bleach.clean(str(dictionary_soft.get("term", "Not provided")))
        required_years_soft = bleach.clean(str(dictionary_soft.get("required_years", "Not provided")))
        soft_clean.append({
            "term": term_soft,
            "required_years": required_years_soft
        })
    
    return {
        "technical": technical_clean,
        "soft": soft_clean
    }


def clean_jd_actions(actions):
    email_to = bleach.clean(str(actions.get("email_to", "Not provided")))
    survey = [bleach.clean(str(link)) for link in actions.get("survey", ["Not provided"])]    

    return {
        "email_to": email_to,
        "survey": survey
    }

def clean_jd_statements(statements):
    quantifiable = [bleach.clean(str(stmt)) for stmt in statements.get("quantifiable", ["Not provided"])]
    ats = [bleach.clean(str(stmt)) for stmt in statements.get("ats", ["Not provided"])]

    return {
        "quantifiable": quantifiable,
        "ats": ats
    }

# CLEAN ALL
def default_and_cleanse_rm(res):
    if not isinstance(res, dict):
        return DefaultRM.full
    
    # CONTACT INFO
    contact = res.get("Contact Information", None)
    if contact is not None:
        if not isinstance(contact, dict):
            contact = DefaultRM.contact
        else:
            contact = clean_rm_contact(contact)              
    else:
        contact = DefaultRM.contact

    # SUMMARY OR OBJECTIVE
    summary = res.get("Summary or Objective", None)
    if summary is not None:
        if not isinstance(summary, dict):
            summary = DefaultRM.summary
        else:
            summary = clean_rm_summary(summary)              
    else:
        summary = DefaultRM.summary

    # SKILLS
    skills = res.get("Skills", None)
    if skills is not None:
        if not isinstance(skills, dict):
            skills = DefaultRM.skills
        else:
            skills = clean_rm_skills(skills)              
    else:
        skills = DefaultRM.skills

    # WORK EXPERIENCE
    work_experience = res.get("Work Experience", None)
    if work_experience is not None:
        if not isinstance(work_experience, dict):
            work_experience = DefaultRM.work_experience
        else:
            work_experience = clean_rm_work_experience(work_experience)              
    else:
        work_experience = DefaultRM.work_experience

    # EDUCATION
    education = res.get("Education", None)
    if education is not None:
        if not isinstance(education, dict):
            education = DefaultRM.education
        else:
            education = clean_rm_education(education)              
    else:
        education = DefaultRM.education

    # CERTIFICATIONS
    certifications = res.get("Certifications", None)
    if certifications is not None:
        if not isinstance(certifications, dict):
            certifications = DefaultRM.certifications
        else:
            certifications = clean_rm_certifications(certifications)              
    else:
        certifications = DefaultRM.certifications

    # PROJECTS
    projects = res.get("Projects", None)
    if projects is not None:
        if not isinstance(projects, dict):
            projects = DefaultRM.projects
        else:
            projects = clean_rm_projects(projects)              
    else:
        projects = DefaultRM.projects

    # AWARDS AND HONORS
    awards = res.get("Awards and Honors", None)
    if awards is not None:
        if not isinstance(awards, dict):
            awards = DefaultRM.awards
        else:
            awards = clean_rm_awards(awards)              
    else:
        awards = DefaultRM.awards

    # VOLUNTEER EXPERIENCE
    volunteer_experience = res.get("Volunteer Experience", None)
    if volunteer_experience is not None:
        if not isinstance(volunteer_experience, dict):
            volunteer_experience = DefaultRM.volunteer_experience
        else:
            volunteer_experience = clean_rm_volunteer_experience(volunteer_experience)              
    else:
        volunteer_experience = DefaultRM.volunteer_experience

    # LANGUAGES
    languages = res.get("Languages", None)
    if languages is not None:
        if not isinstance(languages, dict):
            languages = DefaultRM.languages
        else:
            languages = clean_rm_languages(languages)              
    else:
        languages = DefaultRM.languages

    # PUBLICATIONS
    publications = res.get("Publications", None)
    if publications is not None:
        if not isinstance(publications, dict):
            publications = DefaultRM.publications
        else:
            publications = clean_rm_publications(publications)              
    else:
        publications = DefaultRM.publications


    return {
        "Contact Information": contact,
        "Summary or Objective": summary,
        "Skills": skills, 
        "Work Experience": work_experience,
        "Education": education,
        "Certifications": certifications,
        "Projects": projects,
        "Awards and Honors": awards,
        "Volunteer Experience": volunteer_experience,
        "Languages": languages,
        "Publications": publications 
    } 

def default_and_clean_jd(cur):
    if not isinstance(cur, dict):
        return DefaultJD.full 
   
    # JOB TITLE
    job_title = cur.get("Job Title", None)
    if job_title is not None:
        if not isinstance(job_title, dict):
            job_title = DefaultJD.job_title
        else:
            job_title = clean_jd_job_title(job_title)              
    else:
        job_title = DefaultJD.job_title

    # KEYWORDS
    keywords = cur.get("Keywords", None)
    if keywords is not None:
        if not isinstance(keywords, dict):
            keywords = DefaultJD.keywords
        else:
            keywords = clean_jd_keywords(keywords)              
    else:
        keywords = DefaultJD.keywords
   
    # ACTIONS
    actions = cur.get("actions", None)
    if actions is not None:
        if not isinstance(actions, dict):
            actions = DefaultJD.actions
        else:
            actions = clean_jd_actions(actions)              
    else:
        actions = DefaultJD.actions

    # STATEMENTS
    statements = cur.get("Statements", None)
    if statements is not None:
        if not isinstance(statements, dict):
            statements = DefaultJD.statements
        else:
            statements = clean_jd_statements(statements)              
    else:
        statements = DefaultJD.statements
   
    return {
        "Job Title": job_title,
        "Keywords": keywords,
        "Actions": actions,
        "Statements": statements
    }