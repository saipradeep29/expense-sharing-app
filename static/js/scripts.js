document.addEventListener("DOMContentLoaded", function() {
    // Toggle visibility of a section
    const toggleButton = document.getElementById('toggle-button');
    const toggleSection = document.getElementById('toggle-section');

    if (toggleButton && toggleSection) {
        toggleButton.addEventListener('click', function() {
            if (toggleSection.style.display === 'none') {
                toggleSection.style.display = 'block';
            } else {
                toggleSection.style.display = 'none';
            }
        });
    }

    // Flash message timeout
    setTimeout(function() {
        const flashMessages = document.querySelectorAll('.flash');
        flashMessages.forEach(function(message) {
            message.style.display = 'none';
        });
    }, 3000);
});
