import { apiRequest } from "./Handshake.js";

// document.getElementById("resume-update-sections").addEventListener("submit", function(event) {
//     event.preventDefault();
//     // break this up to just partial sections?? 
//     const formData = new FormData(this);
//     const data = Object.fromEntries(formData.entries());
//     apiRequest("/set_resume_sections", "POST", data)
//         .then(response => {
//             if (response.status === 200) {
//                 alert("Resume updated successfully!");
//             } else {
//                 alert("Failed to update resume.");
//             }
//         })
//         .catch(error => {
//             console.error("Error:", error);
//         });
// });

let activeTabId = "tab1";

document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".tab");
    const contents = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", function () {
            const target = this.getAttribute("data-tab");
            activeTabId = target; 
            console.log(activeTabId);

            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove("active"));
            contents.forEach(c => c.classList.remove("active"));

            // Add active class to the clicked tab and corresponding content
            this.classList.add("active");
            document.getElementById(target).classList.add("active");
        });
    });
});

class ButtonOrganizer {
    constructor(containerSelector) {
        this.container = document.querySelector(containerSelector);
    }

    addButton(id, label, onClick) {
        const button = document.createElement("button");
        button.id = id;
        button.textContent = label;
        button.classList.add("row-btns");
        button.addEventListener("click", onClick);
        this.container.appendChild(button);
    }
}

// Usage Example
document.addEventListener("DOMContentLoaded", () => {
    const buttonOrganizer = new ButtonOrganizer("#buttonContainer");
    buttonOrganizer.addButton("saveBtn", "Save", () => console.log("Save clicked"));
});
