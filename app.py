
# -*- coding: utf-8 -*-
from lib.app_conf import app
from lib.index.base import home, get_started
from lib.user_interactions.data import (
    set_job_description,
    get_job_description,
    set_resume_sections,
    set_partial_resume_sections,
    get_resume_sections
)
from lib.pdf.download import download_pdf
from lib.pdf.example import view_example
from lib.user_interactions.email import validate_verification_email
from lib.user_interactions.account import sign_user_in, register_user, logout

app.route('/', methods=['GET'])(home)
app.route('/get-started', methods=['GET'])(get_started)

app.route('/set_job_description', methods=['POST'])(set_job_description)
app.route('/get_job_description', methods=['GET'])(get_job_description)
app.route('/set_resume_sections', methods=['POST'])(set_resume_sections)
app.route('/set_partial_resume_sections', methods=['POST'])(
    set_partial_resume_sections
)
app.route('/get_resume_sections', methods=['GET'])(get_resume_sections)

app.route('/download_pdf')(download_pdf)
app.route('/examples/<string:version>')(view_example)

app.route('/validate_email_code', methods=['POST'])(validate_verification_email)
app.route("/sign_user_in", methods=['POST'])(sign_user_in)
app.route("/register_user", methods=['POST'])(register_user)
app.route('/logout')(logout)

if __name__ == '__main__':
    app.run(debug=True)
