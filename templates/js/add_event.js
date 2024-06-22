        document.getElementById('event_form').addEventListener('click', function() {
            var addEventDiv = document.getElementById('add_event_new');
            if (addEventDiv.classList.contains('hidden')) {
                addEventDiv.classList.remove('hidden');
            } else {
                addEventDiv.classList.add('hidden');
            }
        });