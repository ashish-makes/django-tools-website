// Mobile Nav Menu

const mobMenu = document.querySelector(".mobMenu");
const mobMenuBtn = document.getElementById("mobmenuBtn");

mobMenuBtn.addEventListener("click", function mobMenubtoggle() {
  mobMenu.classList.toggle("show")
})

// Tools Dropdown Menu

const toolMenu = document.querySelector(".tools-dropdown-menu");
const toolMenuBtn = document.getElementById("tool-btn");

toolMenuBtn.addEventListener("click", function toolsMenubtoggle() {
  toolMenu.classList.toggle("show")
})

// Contact Form Validation

// const contactForm = document.querySelector('.contact-form');

// if (contactForm) {
//   const nameInput = document.querySelector('#name');
//   const emailInput = document.querySelector('#email');
//   const phoneInput = document.querySelector('#phone');
//   const msgInput = document.querySelector('#msg');
//   const submitButton = document.querySelector('#submit-button');

//   contactForm.addEventListener('submit', function (event) {
//     event.preventDefault();

//     if (nameInput.value.trim() === '') {
//       nameInput.style.borderColor = "red";
//       nameInput.focus();
//       setTimeout(function() {
//         nameInput.style.borderColor = "";
//       }, 2000);
//       return;
//     }

//     if (emailInput.value.trim() === '') {
//       emailInput.style.borderColor = "red";
//       emailInput.focus();
//       setTimeout(function() {
//           emailInput.style.borderColor = "";
//         }, 2000);
//         return;
//     }

//     if (phoneInput.value.trim() === '') {
//       phoneInput.style.borderColor = "red";
//       phoneInput.focus();
//       setTimeout(function() {
//           phoneInput.style.borderColor = "";
//         }, 2000);
//         return;
//     }

//     if (msgInput.value.trim() === '') {
//       msgInput.style.borderColor = "red";
//       msgInput.focus();
//       setTimeout(function() {
//           msgInput.style.borderColor = "";
//         }, 2000);
//         return;
//     }

//     contactForm.submit();
//   });
// }

// Contact Form Validation

const contactform = document.querySelector('.contact-form');

if (contactform) {
  const contactnameInput = contactform.querySelector('#name');
  const contactphoneInput = contactform.querySelector('#phone');
  const contactemailInput = contactform.querySelector('#email');
  const contactmsgInput = contactform.querySelector('#msg');
  const contactNameerrorDiv = document.querySelector('.nameerror-message');
  const contactEmailerrorDiv = document.querySelector('.emailerror-message');
  const contactphoneerrorDiv = document.querySelector('.phoneerror-message');
  const contactmsgerrorDiv = document.querySelector('.msgerror-message');

  contactform.addEventListener('submit', (event) => {
    event.preventDefault();

    // Validate name
    if (contactnameInput.value === '') {
      contactNameerrorDiv.innerHTML = 'Please enter your name.';
      contactnameInput.focus();
      // displayError('Please enter your name.');
      return;
    } else {
      contactNameerrorDiv.innerHTML = '';
    }

    // Validate email
    const emailRegex = /\S+@\S+\.\S+/;
    if (!emailRegex.test(contactemailInput.value)) {
      contactEmailerrorDiv.innerHTML = 'Please enter a valid email address.';
      contactemailInput.focus();
      return;
    } else {
      contactEmailerrorDiv.innerHTML = '';
    }

    // Validate phone number
    const phoneRegex = /^\d{10}$/;
    if (!phoneRegex.test(contactphoneInput.value)) {
      contactphoneerrorDiv.innerHTML = 'Please enter a valid phone number.';
      contactphoneInput.focus();
      return;
    } else {
      contactphoneerrorDiv.innerHTML = '';
    }

    // Validate message
    if (contactmsgInput.value === '') {
      contactmsgerrorDiv.innerHTML = 'Please enter a message.';
      contactmsgInput.focus();
      return;
    } else {
      contactmsgerrorDiv.innerHTML = '';
    }

    // Submit the form
    contactform.submit();
  });
}

// Signup Form Validation

// const signupform = document.querySelector('.signup-form');

// if (signupform) {
//   const signupnameInput = signupform.querySelector('#name');
//   const signupemailInput = signupform.querySelector('#email');
//   const usernameInput = signupform.querySelector('#username');
//   const passwordInput = signupform.querySelector('#password');
//   const passwordInstructions = signupform.querySelector('.password-instructions');
//   const NameerrorDiv = document.querySelector('.nameerror-message');
//   const EmailerrorDiv = document.querySelector('.emailerror-message');
//   const UsernameerrorDiv = document.querySelector('.usernameerror-message');
//   const PassworderrorDiv = document.querySelector('.passworderror-message');

//   signupform.addEventListener('submit', (event) => {
//     event.preventDefault();

//     // Validate name
//     if (signupnameInput.value === '') {
//       NameerrorDiv.innerHTML = 'Please enter your name.';
//       signupnameInput.focus();
//       // displayError('Please enter your name.');
//       return;
//     } else {
//       NameerrorDiv.innerHTML = '';
//     }

//     // Validate email
//     const emailRegex = /\S+@\S+\.\S+/;
//     if (!emailRegex.test(signupemailInput.value)) {
//       EmailerrorDiv.innerHTML = 'Please enter a valid email address.';
//       signupemailInput.focus();
//       return;
//     } else {
//       EmailerrorDiv.innerHTML = '';
//     }

//     // Validate username
//     if (usernameInput.value === '') {
//       UsernameerrorDiv.innerHTML = 'Please enter a username.';
//       usernameInput.focus();
//       return;
//     } else {
//       UsernameerrorDiv.innerHTML = '';
//     }

//     // Validate password
//     const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/;
//     if (!passwordRegex.test(passwordInput.value)) {
//       PassworderrorDiv.innerHTML = 'Please enter a password that meets the following criteria mentioned below.';
//       passwordInput.focus();
//       return;
//     } else {
//       PassworderrorDiv.innerHTML = '';
//     }

//     // Submit the form
//     signupform.submit();
//   });
// }

// Login Form Validation

// const loginform = document.querySelector('.login-form');

// if (loginform) {
//   const loginusernameInput = loginform.querySelector('#username');
//   const loginpasswordInput = loginform.querySelector('#password');
//   const loginUserNameerrorDiv = document.querySelector('.usernameerror-message');
//   const loginPassworderrorDiv = document.querySelector('.passworderror-message');

//   loginform.addEventListener('submit', (event) => {
//     event.preventDefault();

//     // Validate username
//     if (loginusernameInput.value === '') {
//     loginUserNameerrorDiv.innerHTML = 'Please enter username.';
//     loginusernameInput.focus();
//       // displayError('Please enter your name.')
//       return;
//     } else {
//       loginUserNameerrorDiv.innerHTML = '';
//     }

//     // Validate password
//     if (loginpasswordInput.value === '') {
//       loginPassworderrorDiv.innerHTML = 'Please enter your password.';
//       loginpasswordInput.focus();
//       return;
//     } else {
//       loginPassworderrorDiv.innerHTML = '';
//     }

//     // Submit the form
//     loginform.submit();
//   });
// }


// Edit Profile Notification Close Btn

const EditProfileNotif = document.querySelector('.edit-profile');

if (EditProfileNotif) {
const EditCloseBtn = document.querySelector('.edit-prf-close-btn');

EditCloseBtn.addEventListener('click', function() {
  EditProfileNotif.style.display = "none";
})}