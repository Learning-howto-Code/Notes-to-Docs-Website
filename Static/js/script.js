document.getElementById("file-upload").addEventListener("change", function (event) {
    let fileList = document.getElementById("file-list");
    fileList.innerHTML = ""; // Clear previous list

    for (let file of event.target.files) {
        let listItem = document.createElement("li");
        listItem.textContent = file.name;
        fileList.appendChild(listItem);
    }
});


async function fetchFiles() {
    let response = await fetch("/files");
    let data = await response.json();
    
    let fileList = document.getElementById("file-list");
    fileList.innerHTML = ""; // Clear list

    data.files.forEach(file => {
        let listItem = document.createElement("li");
        listItem.innerHTML = `<a href="/download/${file}" target="_blank">${file}</a>`;
        fileList.appendChild(listItem);
    });
}

// Call fetchFiles() after upload to refresh the list
