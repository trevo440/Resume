import { PromptManager } from './AgentInterface.js';
import { apiRequest } from "./Handshake.js";

let bodyJD = {}; 
let newRM = {};
let server_resume = {};
let server_jd = {};

let step2 = true;

async function getDataJD(PM, jobDesc) {
    bodyJD = await PM.assessJD(jobDesc);
}

async function intersectDataJD(PM, server_resume, server_jd) {
    newRM = await PM.intersect(server_resume, server_jd);
}

document.getElementById("update-job-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    document.getElementById("loading").style.display = "block";

    const apiKey = localStorage.getItem("api_key");
    const jobDesc = document.getElementById("job-desc").value;
    localStorage.setItem("job_description_raw", jobDesc);
    const PM = new PromptManager(apiKey);

    await getDataJD(PM, jobDesc);

    // Example API call
    apiRequest("/set_job_description", "POST", JSON.stringify(bodyJD))
        .then(data => {
            // Store values in localStorage
            document.getElementById("loading").style.display = "none";
            step2 = true;

        })
        .catch(error => {
            document.getElementById("loading").style.display = "none";
            step2 = false;
            console.error("Error:", error);
        }); 

    if (step2) {
        apiRequest("/get_resume_sections", "GET")
            .then(response => {
                server_resume = response
            })
            .catch(error => {
                document.getElementById("loading").style.display = "none";
            });

        apiRequest("/get_job_description", "GET")
            .then(response => {
                server_jd = response
            })
            .catch(error => {
                document.getElementById("loading").style.display = "none";
            });

        await intersectDataJD(PM, server_resume, server_jd);

        apiRequest("/set_resume_sections", "POST", JSON.stringify(newRM))
            .then(data => {
                // Store values in localStorage
                document.getElementById("loading").style.display = "none";
                location.reload();
        
            })
            .catch(error => {
                document.getElementById("loading").style.display = "none";
            });
    }

});

let selectedVersion = 'basic';
function setSelectedVersion() {
    selectedVersion = document.getElementById('resume-version').value;
    const exampleLink = document.getElementById('view-example-link');
    exampleLink.href = `/examples/${selectedVersion}`;
}