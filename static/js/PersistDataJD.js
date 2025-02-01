import { PromptManager } from './AgentInterface.js';
import { apiRequest } from "./Handshake.js";

let bodyJD = {}; 
let newRM = {};
let server_resume;
let server_jd;

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

    try {
        await apiRequest("/set_job_description", "POST", bodyJD);
        step2 = true;
    } catch (error) {
        document.getElementById("loading").style.display = "none";
        step2 = false;
        console.error("Error:", error);
        return;
    }

    if (step2) {
        try {
            server_resume = await apiRequest("/get_resume_sections", "GET").then(res => res.json());
            // console.log("Fetched resume sections:", server_resume);

            server_jd = await apiRequest("/get_job_description", "GET").then(res => res.json());
            // console.log("Fetched job description:", server_jd);

            await intersectDataJD(PM, server_resume, server_jd);
            console.log("New Resume Match:", newRM);

            await apiRequest("/set_partial_resume_sections", "POST", newRM);
            document.getElementById("loading").style.display = "none";
            location.reload();
        
        } catch (error) {
            document.getElementById("loading").style.display = "none";
            console.error("Error fetching data:", error);
        }
    }
});

let selectedVersion = 'basic';
function setSelectedVersion() {
    selectedVersion = document.getElementById('resume-version').value;
    const exampleLink = document.getElementById('view-example-link');
    exampleLink.href = `/examples/${selectedVersion}`;
}
