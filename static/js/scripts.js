// JavaScript for the Loan Management System

// Function to handle active menu item
document.querySelectorAll('.sidebar nav a').forEach(link => {
    link.addEventListener('click', function() {
        document.querySelectorAll('.sidebar nav a').forEach(item => item.classList.remove('active'));
        this.classList.add('active');
    });
});

// Function to handle View Offers button clicks
document.querySelectorAll('.loan-card .button').forEach(button => {
    button.addEventListener('click', function() {
        alert('Viewing offers for ' + this.closest('.loan-card').querySelector('h3').textContent);
    });
});

// Function to handle logout
document.querySelector('.sidebar .logout').addEventListener('click', function() {
    alert('You have logged out.');
    // Add actual logout functionality here
});
