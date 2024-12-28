// Open the modal
function openContent(button) {
  var moduleId = button.getAttribute("data");
  document.querySelector('input[name="id"]').value = moduleId;
  document.getElementById("contentModal").style.display = 'block';
}

// Close the modal
function closeModals() {
  const modal = document.getElementById("contentModal").style.display = 'none';
  // if (modal) {
  //   modal.style.display = "none"; // Hide the modal
  // }
}

// Optionally, add event listener to close modal when clicking outside
window.onclick = function(event) {
  const modals = document.querySelectorAll('.modal');
  modals.forEach(modal => {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  });
}


// Toggle content options based on selection
function toggleContentOptions() {
  const contentType = document.getElementById("content_type").value;
  const pageOptions = document.getElementById("pageOptions");
  const videoOptions = document.getElementById("videoOptions");

  if (contentType === "page") {
      pageOptions.classList.remove("hidden");
      videoOptions.classList.add("hidden");
  } else if (contentType === "video") {
      videoOptions.classList.remove("hidden");
      pageOptions.classList.add("hidden");
  } else {
      pageOptions.classList.add("hidden");
      videoOptions.classList.add("hidden");
  }
}

// Close modal when clicking outside of it
window.onclick = function(event) {
  const modal = document.getElementById("contentModal");
  if (event.target === modal) {
      closeModal();
  }
}

function opencourseForm() {
    document.getElementById('modals-Content').style.display = 'block';
}
  
function closeCourse() {
    document.getElementById('modals-Content').style.display = 'none';
}


let acc = document.getElementsByClassName("accordion");

for (let i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    // Toggle the "active" class on the clicked accordion
    this.classList.toggle("active");

    // Find the parent .module-card and get all .panel elements within it
    let parentModule = this.closest(".module-card");  // Find the closest .module-card
    let panels = parentModule.querySelectorAll(".panel"); // Find all .panel elements inside it

    // Toggle the visibility of all panels
    for (let j = 0; j < panels.length; j++) {
      // Check if the panel is visible, then hide it, otherwise show it
      if (panels[j].style.display === "block") {
        panels[j].style.display = "none";
      } else {
        panels[j].style.display = "block";
      }
    }
  });
}
