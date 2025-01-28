def ensure_keys_exist(res):
    default_structure = {
        "Contact Information": {
            "full_name": "",
            "phone_number": "",
            "email": "",
            "linkedin": "",
            "website": "",
            "address": "",
        },
        "Summary or Objective": {
            "summary": ["string"]
        },
        "Skills": {
            "skills": []
        },
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