document.getElementById("convert").addEventListener("click", async function() {
    try {
        const response = await fetch("/convert", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();
        
        if (data.results) {
            const resultsContainer = document.getElementById("results-container");
            resultsContainer.innerHTML = ""; // Clear previous results
            
            data.results.forEach(result => {
                const filename = Object.keys(result)[0];
                const text = result[filename].text;
                
                const resultHtml = `
                    <div class="result-item">
                        <div class="filename">📄 ${filename}</div>
                        <div class="extracted-text">${text}</div>
                    </div>
                `;
                resultsContainer.innerHTML += resultHtml;
            });
        }
    } catch (error) {
        console.error("Conversion error:", error);
        alert("Conversion failed: " + error.message);
    }
});

async function fetchFiles() {
    let response = await fetch("/uploads/files"); // Update route
    let data = await response.json();
    let fileList = document.getElementById("file-list");
    fileList.innerHTML = ""; // Clear previous list

    data.files.forEach(file => {
        let listItem = document.createElement("li");
        listItem.innerHTML = `<a href="/uploads/download/${file}" target="_blank">${file}</a>`;
        fileList.appendChild(listItem);
    });
}

// Load files on page load
fetchFiles();
