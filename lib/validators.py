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

    summary = {"summary": ["Not provided."]}
    skills = {"skills": ["Not provided."]}

    full = {
        "Contact Information": contact,
        "Summary or Objective": summary,
        "Skills": skills,   
    }

DefaultRM = DefaultsRM()

# SECTION CLEANERS
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


    # add the DefaultRM.full logic here for return   

def ensure_rm_keys_exist(res):
    default_structure = {
        "Work Experience": {
            "work_experience": []
        },
        "Education": {
            "education": []
        },
        "Certifications": {
            "certifications": []
        },
        "Projects": {
            "projects": []
        },
        "Awards and Honors": {
            "awards": []
        },
        "Volunteer Experience": {
            "volunteer_experience": []
        },
        "Languages": {
            "languages": []
        },
        "Publications": {
            "publications": []
        }
    }

    def ensure_nested_keys(target, defaults):
        for key, value in defaults.items():
            if key not in target:
                target[key] = value
            elif isinstance(value, dict):
                ensure_nested_keys(target[key], value)

    # Ensure all keys and nested keys exist
    ensure_nested_keys(res, default_structure)

    return res

    
