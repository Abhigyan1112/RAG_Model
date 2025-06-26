const dropArea = document.getElementById("form-label");
const inputFile = document.getElementById("formFile");
const fileName = document.getElementById("file-name");

fileName.addEventListener("change", ()=>{
    if (inputFile.files.length > 0) {
        fileName.innerHTML ="<p>"+ inputFile.files[0].name +"</p>";
    }
});

dropArea.addEventListener("dragover", (e)=>{
    e.preventDefault();
    dropArea.classList.add("highlight");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("highlight");
});

dropArea.addEventListener("drop", (e)=>{
    e.preventDefault();
    dropArea.classList.remove("highlight");

    if (e.dataTransfer.files.length > 0) {
        inputFile.files = e.dataTransfer.files;
        inputFile.dispatchEvent(new Event("change"));
    }
    dropArea.style.backgroundColor = "rgb(255, 175, 188)";
});