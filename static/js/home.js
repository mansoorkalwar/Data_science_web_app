document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("fileInput");
    const dropzone = document.getElementById("uploadDropzone");
    const dropArea = document.querySelector(".file-dropzone");
    const fileName = document.getElementById("fileName");

    const icons = {
        upload: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 13v8"/><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="m8 17 4-4 4 4"/></svg>',
        file: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>',
        browse: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 13h6"/><path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/></svg>',
        chart: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 21v-6"/><path d="M12 21V9"/><path d="M19 21V3"/></svg>',
        shield: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>',
        analyze: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M22 20V7"/></svg>'
    };

    document.querySelector(".upload-icon").innerHTML = icons.upload;
    document.querySelector(".dropzone-icon").innerHTML = icons.file;
    document.querySelector(".browse-icon").innerHTML = icons.browse;
    document.querySelector(".analyze-icon").innerHTML = icons.analyze;
    document.querySelector(".file-stat-icon").innerHTML = icons.file;
    document.querySelector(".chart-stat-icon").innerHTML = icons.chart;
    document.querySelector(".shield-stat-icon").innerHTML = icons.shield;

    const heroStats = document.querySelector(".hero-stats");
    heroStats.innerHTML = `
        <div class="home-capability">
            <span class="capability-icon">⚡</span>
            <span><strong>Fast Analysis</strong><small>Get insights in seconds</small></span>
        </div>
        <div class="home-capability">
            <span class="capability-icon">${icons.shield}</span>
            <span><strong>Secure &amp; Private</strong><small>Your data stays yours</small></span>
        </div>
        <div class="home-capability">
            <span class="capability-icon">${icons.chart}</span>
            <span><strong>Beautiful Visualizations</strong><small>Interactive &amp; professional</small></span>
        </div>
    `;

    const style = document.createElement("style");
    style.textContent = `
        @font-face { font-family: "Inter Local"; src: url("https://raw.githubusercontent.com/mansoorkalwar/Data_science_web_app/main/fonts/static/Inter_18pt-Regular.ttf") format("truetype"); font-weight:400; font-style:normal; font-display:swap; }
        @font-face { font-family: "Inter Local"; src: url("https://raw.githubusercontent.com/mansoorkalwar/Data_science_web_app/main/fonts/static/Inter_18pt-Medium.ttf") format("truetype"); font-weight:500; font-style:normal; font-display:swap; }
        @font-face { font-family: "Inter Local"; src: url("https://raw.githubusercontent.com/mansoorkalwar/Data_science_web_app/main/fonts/static/Inter_18pt-SemiBold.ttf") format("truetype"); font-weight:600; font-style:normal; font-display:swap; }
        @font-face { font-family: "Inter Local"; src: url("https://raw.githubusercontent.com/mansoorkalwar/Data_science_web_app/main/fonts/static/Inter_18pt-Bold.ttf") format("truetype"); font-weight:700; font-style:normal; font-display:swap; }
        .home-page .hero-stats { display:flex; justify-content:flex-start; align-items:stretch; margin-top:34px; }
        .home-page .home-capability { display:flex; align-items:center; gap:10px; padding:0 23px; border-right:1px solid #D7DEDB; }
        .home-page .home-capability:first-child { padding-left:0; }
        .home-page .home-capability:last-child { border-right:0; }
        .home-page .capability-icon { width:24px; height:24px; display:grid; place-items:center; color:#087F5B; font-size:22px; }
        .home-page .capability-icon svg { width:22px; height:22px; display:block; }
        .home-page .home-capability strong,
        .home-page .home-capability small { display:block; }
        .home-page .home-capability strong { color:#253247; font-size:11px; font-weight:600; line-height:1.2; white-space:nowrap; }
        .home-page .home-capability small { margin-top:5px; color:#8A96A5; font-size:9px; line-height:1.2; white-space:nowrap; }
        @media (max-width:900px) { .home-page .hero-stats { justify-content:center; } }
        @media (max-width:560px) { .home-page .hero-stats { flex-direction:column; gap:14px; align-items:flex-start; } .home-page .home-capability { padding:0; border-right:0; } }
    `;
    document.head.appendChild(style);

    function setSelectedFile(file) {
        if (!file) return;
        uploadedFile = file;
        fileName.textContent = `Selected: ${file.name}`;
    }

    fileInput.addEventListener("change", event => {
        setSelectedFile(event.target.files[0]);
    });

    ["dragenter", "dragover"].forEach(type => {
        dropArea.addEventListener(type, event => {
            event.preventDefault();
            dropArea.classList.add("dragover");
        });
    });

    ["dragleave", "drop"].forEach(type => {
        dropArea.addEventListener(type, event => {
            event.preventDefault();
            dropArea.classList.remove("dragover");
        });
    });

    dropArea.addEventListener("drop", event => {
        const file = event.dataTransfer.files[0];
        if (!file) return;
        const extension = file.name.toLowerCase().split(".").pop();
        if (!["csv", "xlsx", "xls", "json"].includes(extension)) {
            alert("Please upload a CSV, Excel, or JSON file.");
            return;
        }
        setSelectedFile(file);
    });

    dropzone.addEventListener("dragover", event => event.preventDefault());
});
