/* Global */
import { PromptManager } from './AgentInterface.js';

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

    // Wait for getData to complete before proceeding
    await getData(PM, resumeText);

    /* 
        > Send updated resume sections to Redis Session
        > We don't need to store this info but we could 
    */
    fetch("/set_resume_sections", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)  // Ensure body is properly formatted as JSON
    })
    .then(response => response.json())
    .then(data => {
        // Store values in localStorage
        localStorage.setItem("api_key", apiKey);
        localStorage.setItem("resume_text", resumeText);
        localStorage.setItem("job_description_raw", '');
        document.cookie = "requested_values_set=1; path=/; max-age=3600";
        
        alert(data.message);
        window.location.href = "/";
    })
    .catch(error => {
        console.error("Error:", error);
    });    
});
