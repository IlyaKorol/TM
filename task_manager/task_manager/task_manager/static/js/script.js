document.addEventListener('DOMContentLoaded', function() {
            var dueDateInput = document.getElementById('due_date');
            var today = new Date().toISOString().split('T')[0];
            dueDateInput.setAttribute('min', today);
        });

