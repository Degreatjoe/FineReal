const contentTypeSelect = document.getElementById("content_type");
const pageOptions = document.getElementById("pageOptions");
const videoOptions = document.getElementById("videoOptions");

contentTypeSelect.addEventListener("change", () => {
    if (contentTypeSelect.value === "page") {
        pageOptions.classList.remove("hidden");
        videoOptions.classList.add("hidden");
    } else if (contentTypeSelect.value === "video") {
        videoOptions.classList.remove("hidden");
        pageOptions.classList.add("hidden");
    }
});

// Initialize form state
if (contentTypeSelect.value === "page") {
    pageOptions.classList.remove("hidden");
    videoOptions.classList.add("hidden");
} else {
    pageOptions.classList.add("hidden");
    videoOptions.classList.remove("hidden");
}

ClassicEditor
.create(document.querySelector('#editor'))
.catch(error => {
    console.error(error);
});
