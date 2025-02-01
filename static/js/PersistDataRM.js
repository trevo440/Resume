/* Global */
import { PromptManager } from './AgentInterface.js';
import { apiRequest } from "./Handshake.js";

let body = {}; 

async function getData(PM, resumeText) {
    body = await PM.pullResume(resumeText);
}

/* Form Submission */
document.getElementById("user-base-info").addEventListener("submit", async function(event) {
    event.preventDefault();

    const apiKey = document.getElementById("api_key").value;
    const resumeText = document.getElementById("resume_text").value;
    const PM = new PromptManager(apiKey);
    document.getElementById("resume-submit").style.display = "none";
    document.getElementById("loading-dots").style.display = "flex";
    
    await getData(PM, resumeText);

    apiRequest("/set_resume_sections", "POST", body)
        .then(data => {
            localStorage.setItem("api_key", apiKey);
            localStorage.setItem("resume_text", resumeText);
            localStorage.setItem("job_description_raw", '');
            window.location.href = "/";
        })
        .catch(error => {
            console.error("Error:", error);
        });    
});
