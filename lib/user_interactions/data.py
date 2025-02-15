from flask import request, jsonify
from lib.validators import default_and_clean_jd, default_and_cleanse_rm
from lib.security.handshake import handshake_required
from lib.user_interactions.auth_session import session_setter, session_getter
from lib.app_conf import limiter

# JOB DESCRIPTION
@handshake_required
@limiter.limit("5 per minute")
def set_job_description():
    data = request.get_json()
    data = default_and_clean_jd(data)
    session_setter("job_description", data)
    return {"message": "Job description updated"}, 200

@handshake_required
@limiter.limit("50 per minute")
def get_job_description():
    return jsonify(session_getter('job_description'))

# RESUME SECTIONS
@handshake_required
@limiter.limit("5 per minute")
def set_resume_sections():
    data = request.get_json()
    data = default_and_cleanse_rm(data)
    session_setter("resume_sections", data)
    session_setter("resume_provided", True)
    return {"message": "Resume sections updated"}, 200

@handshake_required
@limiter.limit("5 per minute")
def set_partial_resume_sections():
    data = request.get_json()
    temp_resume = session_getter('resume_sections')

    if "summary" in data:
        temp_resume["Summary or Objective"]["summary"] = [x + "." for x in data["summary"].split(".")] 
    if "projects" in data:
        temp_resume["Projects"]["projects"] = data["projects"]    
    if "skills" in data:
        temp_resume["Skills"]["skills"] = data["skills"]
    if "work_experience" in data:
        temp_resume["Work Experience"]["work_experience"] = data["work_experience"]
    
    data = default_and_cleanse_rm(temp_resume)
    session_setter("resume_sections", data)
    session_setter("resume_provided", True)
    return {"message": "Resume sections updated"}, 200

@handshake_required
@limiter.limit("50 per minute")
def get_resume_sections():
    return jsonify(session_getter('resume_sections'))