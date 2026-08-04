// ============================================================
// Customer Churn Intelligence & Prediction Platform
// Main JavaScript
// ============================================================

document.addEventListener("DOMContentLoaded", function () {

    // ------------------------------------------------------------
    // Mobile Navigation
    // ------------------------------------------------------------

    const menuButton = document.getElementById("menuButton");
    const navLinks = document.getElementById("navLinks");

    if (menuButton && navLinks) {
        menuButton.addEventListener("click", function () {
            navLinks.classList.toggle("active");
        });
    }


    // ------------------------------------------------------------
    // Close mobile menu after clicking a link
    // ------------------------------------------------------------

    if (navLinks) {
        const links = navLinks.querySelectorAll("a");

        links.forEach(function (link) {
            link.addEventListener("click", function () {
                navLinks.classList.remove("active");
            });
        });
    }


    // ------------------------------------------------------------
    // File Upload Display
    // ------------------------------------------------------------

    const fileInput = document.getElementById("fileInput");
    const fileName = document.getElementById("fileName");

    if (fileInput && fileName) {
        fileInput.addEventListener("change", function () {

            if (fileInput.files.length > 0) {
                fileName.textContent = fileInput.files[0].name;
            } else {
                fileName.textContent = "No file selected";
            }

        });
    }


    // ------------------------------------------------------------
    // Drag & Drop CSV Upload
    // ------------------------------------------------------------

    const uploadArea = document.getElementById("uploadArea");

    if (uploadArea && fileInput) {

        uploadArea.addEventListener("dragover", function (event) {
            event.preventDefault();
            uploadArea.classList.add("drag-over");
        });

        uploadArea.addEventListener("dragleave", function () {
            uploadArea.classList.remove("drag-over");
        });

        uploadArea.addEventListener("drop", function (event) {

            event.preventDefault();
            uploadArea.classList.remove("drag-over");

            const files = event.dataTransfer.files;

            if (files.length > 0) {
                fileInput.files = files;

                if (fileName) {
                    fileName.textContent = files[0].name;
                }
            }
        });
    }


    // ------------------------------------------------------------
    // Form Loading State
    // ------------------------------------------------------------

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const submitButton = form.querySelector(
                'button[type="submit"], input[type="submit"]'
            );

            if (submitButton) {

                submitButton.disabled = true;

                const originalText = submitButton.textContent;

                submitButton.textContent = "Processing...";

                // Prevent button from remaining disabled forever
                setTimeout(function () {
                    submitButton.disabled = false;
                    submitButton.textContent = originalText;
                }, 10000);
            }
        });

    });


    // ------------------------------------------------------------
    // Number Input Validation
    // ------------------------------------------------------------

    const numberInputs = document.querySelectorAll(
        'input[type="number"]'
    );

    numberInputs.forEach(function (input) {

        input.addEventListener("input", function () {

            if (input.value < 0) {
                input.value = 0;
            }

        });

    });


    // ------------------------------------------------------------
    // Animated Counters
    // ------------------------------------------------------------

    const counters = document.querySelectorAll(".counter");

    counters.forEach(function (counter) {

        const target = parseFloat(counter.dataset.target);

        if (isNaN(target)) {
            return;
        }

        let current = 0;
        const duration = 1000;
        const steps = 50;
        const increment = target / steps;

        const interval = setInterval(function () {

            current += increment;

            if (current >= target) {
                current = target;
                clearInterval(interval);
            }

            counter.textContent = Number.isInteger(target)
                ? Math.round(current)
                : current.toFixed(1);

        }, duration / steps);

    });


    // ------------------------------------------------------------
    // Risk Level Styling
    // ------------------------------------------------------------

    const riskElements = document.querySelectorAll(".risk-level");

    riskElements.forEach(function (element) {

        const risk = element.textContent.trim().toLowerCase();

        element.classList.remove(
            "low-risk",
            "medium-risk",
            "high-risk"
        );

        if (risk.includes("low")) {
            element.classList.add("low-risk");
        }

        else if (risk.includes("medium")) {
            element.classList.add("medium-risk");
        }

        else if (risk.includes("high")) {
            element.classList.add("high-risk");
        }

    });


    // ------------------------------------------------------------
    // Smooth Scrolling
    // ------------------------------------------------------------

    const anchors = document.querySelectorAll('a[href^="#"]');

    anchors.forEach(function (anchor) {

        anchor.addEventListener("click", function (event) {

            const targetId = anchor.getAttribute("href");

            if (targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (target) {

                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }

        });

    });


    // ------------------------------------------------------------
    // Console Message
    // ------------------------------------------------------------

    console.log(
        "Customer Churn Intelligence & Prediction Platform loaded successfully."
    );

});
