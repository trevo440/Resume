import { PromptManager } from './AgentInterface.js';

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

    fetch("/set_job_description", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(bodyJD)  // Ensure body is properly formatted as JSON
    })
    .then(response => response.json())
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
        fetch("/get_resume_sections", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
        })
        .then(response => {
            server_resume = response.json()
        })
        .catch(error => {
            document.getElementById("loading").style.display = "none";
        });

        fetch("/get_job_description", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
        })
        .then(response => {
            server_jd = response.json()
        })
        .catch(error => {
            document.getElementById("loading").style.display = "none";
        });

        await intersectDataJD(PM, server_resume, server_jd);

        fetch("/set_resume_sections", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(newRM)  // Ensure body is properly formatted as JSON
        })
        .then(response => response.json())
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