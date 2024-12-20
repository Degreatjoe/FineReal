// for the user icon open
function extend() {
  document.getElementById("user_info").style.display = "block";
}
//  for user-icon close
function closeModal() {
  document.getElementById("user_info").style.display = "none";
}


// for navigation
function toggleMenu() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('active');
}


// for signup password checking
const passwordField = document.getElementById('password');
const confirmPasswordField = document.getElementById('confirm_password');
const submitBtn = document.getElementById('submitBtn');
const passwordStrengthBar = document.getElementById('passwordStrengthBar');

// Confirm Password Validation
confirmPasswordField.addEventListener('input', () => {
  if (confirmPasswordField.value === passwordField.value) {
    confirmPasswordField.setCustomValidity('');
  } else {
    confirmPasswordField.setCustomValidity('Passwords do not match');
  }
});

// Password Validation and Feedback
passwordField.addEventListener('input', function () {
  const password = this.value;

  // Feedback Elements
  const lengthFeedback = document.getElementById('lengthFeedback');
  const uppercaseFeedback = document.getElementById('uppercaseFeedback');
  const lowercaseFeedback = document.getElementById('lowercaseFeedback');
  const numberFeedback = document.getElementById('numberFeedback');
  const specialCharFeedback = document.getElementById('specialCharFeedback');

  // Validation Checks
  const isLengthValid = password.length >= 8;
  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

  // Update Feedback
  lengthFeedback.classList.toggle('invalid', !isLengthValid);
  lengthFeedback.classList.toggle('valid', isLengthValid);

  uppercaseFeedback.classList.toggle('invalid', !hasUppercase);
  uppercaseFeedback.classList.toggle('valid', hasUppercase);

  lowercaseFeedback.classList.toggle('invalid', !hasLowercase);
  lowercaseFeedback.classList.toggle('valid', hasLowercase);

  numberFeedback.classList.toggle('invalid', !hasNumber);
  numberFeedback.classList.toggle('valid', hasNumber);

  specialCharFeedback.classList.toggle('invalid', !hasSpecialChar);
  specialCharFeedback.classList.toggle('valid', hasSpecialChar);

  // Password Strength Bar
  const strengthScore = [isLengthValid, hasUppercase, hasLowercase, hasNumber, hasSpecialChar].filter(Boolean).length;
  passwordStrengthBar.style.width = `${(strengthScore / 5) * 100}%`;
  passwordStrengthBar.style.backgroundColor = strengthScore === 5 ? 'green' : strengthScore >= 3 ? 'orange' : 'red';

  // Enable/Disable Submit Button
  submitBtn.disabled = !(isLengthValid && hasUppercase && hasLowercase && hasNumber && hasSpecialChar);
});



function openModal() {
  document.querySelector('.modal').style.display = 'block';
}

function closeModal() {
  document.querySelector('.modal').style.display = 'none';
}