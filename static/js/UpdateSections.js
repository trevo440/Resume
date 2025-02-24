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

document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".tab");
    const contents = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", function () {
            const target = this.getAttribute("data-tab");

            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove("active"));
            contents.forEach(c => c.classList.remove("active"));

            // Add active class to the clicked tab and corresponding content
            this.classList.add("active");
            document.getElementById(target).classList.add("active");
        });
    });
});