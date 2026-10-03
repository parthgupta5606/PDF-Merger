const pdfInput = document.getElementById("pdfInput");
const pdfList = document.getElementById("pdfList");

let selectedFiles = [];

pdfInput.addEventListener("change", function () {

    const newFiles = Array.from(pdfInput.files);

    selectedFiles = [...selectedFiles, ...newFiles];

    displayFiles();

});


function displayFiles() {

    pdfList.innerHTML = "";

    selectedFiles.forEach((file, index) => {

        const pdfItem = document.createElement("div");
        pdfItem.className = "pdf-item";

        pdfItem.innerHTML = `
    <div class="pdf-header">

        <span class="pdf-name">
            📄 ${file.name}
        </span>

        <button
            type="button"
            class="remove-btn"
            onclick="removeFile(${index})"
        >
            Remove
        </button>

    </div>

    <label class="pages-label">
        Pages to merge:
    </label>

    <input
        type="text"
        class="pages-input"
        name="pages"
        placeholder="Example: 1,3,5-7"
    />
`;

        pdfList.appendChild(pdfItem);
    });


    updateFileInput();
}


function removeFile(index) {

    selectedFiles.splice(index, 1);

    displayFiles();
}


function updateFileInput() {

    const dataTransfer = new DataTransfer();

    selectedFiles.forEach(file => {
        dataTransfer.items.add(file);
    });

    pdfInput.files = dataTransfer.files;
}