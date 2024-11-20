document.addEventListener("DOMContentLoaded", function() {
    const navLinks = document.querySelectorAll('.header__menu ul li a');

    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Remove the active class from all items
            navLinks.forEach(l => l.parentElement.classList.remove('active'));

            // Add the active class to the clicked item
            this.parentElement.classList.add('active');
        });
    });
});
