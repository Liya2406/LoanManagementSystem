// scripts.js

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", function (event) {
            const statusSelect = form.querySelector("select[name='action']");
            const action = statusSelect.value;

            if (action === "reject") {
                const comments = form.querySelector("textarea[name='rejection_comments']").value;

                if (!comments) {
                    alert("Please provide rejection comments.");
                    event.preventDefault(); // Prevent form submission
                } else {
                    const confirmSubmit = confirm("Are you sure you want to reject this application?");
                    if (!confirmSubmit) {
                        event.preventDefault(); // Prevent form submission
                    }
                }
            } else {
                const confirmSubmit = confirm("Are you sure you want to change the status?");
                if (!confirmSubmit) {
                    event.preventDefault(); // Prevent form submission
                }
            }
        });
    }
});
