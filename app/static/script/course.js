function login() {
    // Redirect to the login page
    window.location.href = "{{ url_for('login') }}";
}

function creat_course() {
    // Redirect to the logout page
    window.location.href = "{{ url_for('create_course') }}";
}

function openModal() {
    document.querySelector('.modal').style.display = 'block';
  }
  
  function closeCourse() {
    document.querySelector('.modal').style.display = 'none';
  }

// for the course_view template
function openPage(pageName, elmnt, color) {
  // Hide all elements with class="tabcontent" by default */
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Remove the background color of all tablinks/buttons
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "";
  }

  // Show the specific tab content
  document.getElementById(pageName).style.display = "block";

  // Add the specific color to the button used to open the tab content
  elmnt.style.backgroundColor = color;
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();

document.addEventListener("DOMContentLoaded", function() {
  // Bind click events to course cards
  const courseCards = document.querySelectorAll('.course-card');
  courseCards.forEach(function(card) {
      card.addEventListener('click', function() {
          const courseId = card.id.replace('course-', ''); // Get the course ID from the div's ID
          console.log('Course ID:', courseId); // Log to check if the ID is being captured
          courseView(courseId);
      });
  });
});

function courseView(course_id) {
  // Redirect to the course view page
  console.log('Redirecting to course view for course ID:', course_id); // Log for debugging
  window.location.href = "{{ url_for('course_view', course_id='') }}" + course_id;
}
