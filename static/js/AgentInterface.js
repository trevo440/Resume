/* PROMPT(S) */
const resumePrompt = `
"Given the following resume text, extract the relevant sections and organize them into a valid JSON string format. The JSON should follow this specific structure:

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
Return only the JSON string with the specified keys and content. Use "Not provided" in place of any empty values.

Resume Text: 
`;

const jdPrompt = `
"Given the following job description, extract the relevant sections and organize them into a valid JSON string format. The JSON should follow this specific structure:

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
Return only the JSON string with the specified keys and content. Use "Not provided" in place of any empty values.

Job Description: 
`;

const intersectPrompt = `
Given the following Resume JSON, and Job Requirements JSON, update content sections to evaluate higher in comparing the two:

> ENSURE ALL CHARACTERS IN NEED OF ESCAPING ARE ESCAPED.
> Add some amount of Job Requirements ATS Responsibilities statements

The resulting JSON should follow this specific structure:

summary: An UPDATED Summary that instersects both the quantifiable metrics (use high-performance scores, and real numbers.) and keywords.

skills: A list of skills, including programming languages, tools, and other technical or soft skills. Any missing keywords should go in here.

work_experience: An UPDATED list of job entries, FROM Resume JSON, INTERSECTED with Job Requirements JSON. You are NOT to make any new entries in this field, but MUST pull from existing.

projects: A list of projects which partially match the Responsibilities of this role, each containing:
project_title: The title of the project.
description: A brief description of the project. Ensure it aligns with some Job Requirements JSON Statements.ats statement(s).
technologies_used: A list of technologies used in the project. Use keywords here.

Return ONLY the JSON string with the specified keys and content. Use "Not provided" in place of any empty values.

`;
import { Cleanser } from './Cleanser.js';
/* Interface with OpenAI - update for model selection later */
export class PromptManager {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.cleaner = new Cleanser();
        
        // effective enough default
        const modelString = localStorage.getItem("model_version");
        const [provider, model] = modelString.includes(":") ? modelString.split(":") : ["openai","gpt-4o-mini"];
        
        this.provider = provider;
        this.model = model;
        if (this.provider === "openai") {
            this.endpoint = 'https://api.openai.com/v1/chat/completions';
        } else { 
            this.endpoint = ''
        }
    }

    async pullResume(resumeText) {
        resumeText = this.cleaner.noQuote(resumeText);
        const instruct = `${resumePrompt}${resumeText}\n\n{\n    \"task\": \"GPT Response to be usable in programming loop\",\n    \"details\": \"Return a valid JSON string in the correct format only and NOTHING ELSE. Include ALL keys, even if they are empty.\" \n},`;
    
        const gpt_response = {
            model: this.model,
            messages: [{ role: "system", content: instruct }]
        };
    
        try {
            const response = await this.fetchCompletion(gpt_response);
            if (!response || !response.choices || response.choices.length === 0) {
                throw new Error("Invalid response from OpenAI API");
            }
    
            let responseContent = response.choices[0].message.content;
            if (!responseContent) {
                throw new Error("GPT response is empty");
            }
    
            responseContent = this.cleaner.ensureGptFormat(responseContent);
            return JSON.parse(responseContent);

        } catch (error) {
            console.error("Error in pullResume:", error);
            return {};
        }
    }
    

    async pullResume(resumeText) {
        resumeText = this.cleaner.noQuote(resumeText);
        const instruct = `${resumePrompt}${resumeText}\n\n{\n    \"task\": \"GPT Response to be usable in programming loop\",\n    \"details\": \"Return a valid JSON string in the correct format only and NOTHING ELSE. Include ALL keys, even if they are empty.\" \n},`;

        const gpt_response = {
            model: this.model,
            messages: [{ role: "system", content: instruct }]
        };

        const response = await this.fetchCompletion(gpt_response);
        let responseContent = response.choices[0].message.content;
        responseContent = this.cleaner.ensureGptFormat(responseContent);
        return JSON.parse(responseContent);
    }

    async assessJD(jobDescription) {
        jobDescription = this.cleaner.noQuote(jobDescription);
        const instruct = `${jdPrompt}${jobDescription}`;

        const data = {
            model: this.model,
            messages: [{ role: "system", content: `Execute these instructions: ${instruct}` }]
        };

        const response = await this.fetchCompletion(data);
        let responseContent = response.choices[0].message.content;
        responseContent = this.cleaner.ensureGptFormat(responseContent);
        return JSON.parse(responseContent);
    }

    async intersect(resumeSections, jobDescription) {
        const instruct = `${intersectPrompt}Resume JSON: ${JSON.stringify(resumeSections)}\nJob Requirements JSON: ${JSON.stringify(jobDescription)}`;

        const data = {
            model: this.model,
            messages: [{ role: "system", content: `Execute these instructions: ${instruct}` }]
        };

        const response = await this.fetchCompletion(data);
        let responseContent = response.choices[0].message.content;
        responseContent = this.cleaner.ensureGptFormat(responseContent);
        console.log(responseContent);
        return JSON.parse(responseContent);
    }

    async fetchCompletion(data) {
        /* any additional functionality for 
           each vendor will go here */
        const response = await fetch(this.endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Error fetching completion: ${response.statusText}`);
        }

        return response.json();
    }
}

export default PromptManager;

