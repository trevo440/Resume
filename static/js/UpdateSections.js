import { apiRequest } from "./Handshake.js";

document.getElementById("resume-update-sections").addEventListener("submit", function(event) {
    event.preventDefault();
    // break this up to just partial sections?? 
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());
    apiRequest("/set_resume_sections", "POST", data)
        .then(response => {
            if (response.status === 200) {
                alert("Resume updated successfully!");
            } else {
                alert("Failed to update resume.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
});