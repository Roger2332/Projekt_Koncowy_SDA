$(document).ready(function() {
    $('.accept-btn').click(function() {
        var eventId = $(this).data('event-id');
        updateEventStatus(eventId, 'Active');
    });

    $('.reject-btn').click(function() {
        var eventId = $(this).data('event-id');
        updateEventStatus(eventId, 'Rejected');
    });

    function updateEventStatus(eventId, newStatus) {
        $.ajax({
            url: '/update_event_status/',
            type: 'POST',
            data: {
                'event_id': eventId,
                'new_status': newStatus,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    alert('Status wydarzenia został zaktualizowany');
                    location.reload();
                } else {
                    alert('Wystąpił błąd: ' + response.error);
                }
            }
        });
    }
});
