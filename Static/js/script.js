document.getElementById("convert").addEventListener("click", async function() {
    try {
        const response = await fetch("/convert", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error("Server responded with an error.");
        }

        const data = await response.json();
        
        if (data.results && data.results.length > 0) {
            const resultsContainer = document.getElementById("results-container");
            resultsContainer.innerHTML = ""; // Clear previous results
            
            data.results.forEach(result => {
                const filename = Object.keys(result)[0];
                const extractedText = result[filename].document_text || "No text extracted."; // Ensure correct key
                
                const resultHtml = `
                    <div class="result-item">
                        <h3>📄 ${filename}</h3>
                        <p>${extractedText}</p>
                    </div>
                `;
                resultsContainer.insertAdjacentHTML("beforeend", resultHtml);
            });
        } else {
            alert("No text extracted. Try again.");
        }
    } catch (error) {
        console.error("Conversion error:", error);
        alert("Conversion failed: " + error.message);
    }
});

// Fetch uploaded files on page load
async function fetchFiles() {
    try {
        const response = await fetch("/uploads/files"); 
        if (!response.ok) throw new Error("Failed to fetch file list.");

        const data = await response.json();
        const fileList = document.getElementById("file-list");
        fileList.innerHTML = ""; // Clear previous list

        data.files.forEach(file => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `<a href="/uploads/download/${file}" target="_blank">${file}</a>`;
            fileList.appendChild(listItem);
        });
    } catch (error) {
        console.error("File fetch error:", error);
    }
}

// Load files on page load
fetchFiles();
