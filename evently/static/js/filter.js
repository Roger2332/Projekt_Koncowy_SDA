// Toggle filters visibility and load them immediately
const toggleFiltersButton = document.getElementById('toggleFilters');
const filterSection = document.getElementById('filterSection');

toggleFiltersButton.addEventListener('click', function () {
    if (filterSection.style.display === 'none') {
        filterSection.style.display = 'block';
    } else {
        filterSection.style.display = 'none';
    }
});

// Automatically load filters when toggle button is clicked
toggleFiltersButton.addEventListener('click', function () {
    if (filterSection.innerHTML.trim() === '') {
        // Fetch filters content via AJAX or other method if necessary
        // Example: Replace with actual AJAX call if data needs to be loaded dynamically
        setTimeout(() => {
            filterSection.innerHTML = `{% include 'search_form_list.html' %}`;
        }, 500); // Adjust timeout as needed based on your application's loading time
    }
});