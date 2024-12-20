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