$(document).ready(function () {
    // Po załadowaniu dokumentu wykonywana jest funkcja anonimowa
    $('.accept-btn').click(function () {
        // Po kliknięciu na przycisk z klasą 'accept-btn'
        var eventId = $(this).data('event-id');  // Pobierz ID wydarzenia z atrybutu 'data-event-id'
        updateEventStatus(eventId, 'Active');  // Wywołaj funkcję updateEventStatus z podanym ID wydarzenia i nowym statusem 'Active'
    });

    $('.reject-btn').click(function () {
        // Po kliknięciu na przycisk z klasą 'reject-btn'
        var eventId = $(this).data('event-id');  // Pobierz ID wydarzenia z atrybutu 'data-event-id'
        updateEventStatus(eventId, 'Rejected');  // Wywołaj funkcję updateEventStatus z podanym ID wydarzenia i nowym statusem 'Rejected'
    });

    function updateEventStatus(eventId, newStatus) {
        // Funkcja updateEventStatus przyjmuje dwa argumenty: ID wydarzenia i nowy status
        $.ajax({
            url: '/update_event_status/',  // Adres URL, do którego wysyłane jest żądanie POST
            type: 'POST',  // Metoda żądania POST
            data: {
                'event_id': eventId,  // Dane do wysłania: ID wydarzenia
                'new_status': newStatus,  // Dane do wysłania: nowy status
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()  // Token CSRF, pobrany z ukrytego pola formularza
            }, success: function (response) {
                // Funkcja wywoływana po pomyślnym wykonaniu żądania
                if (response.success) {
                    // Jeśli otrzymana odpowiedź zawiera pole 'success' ustawione na True
                    alert('Status wydarzenia został zaktualizowany');  // Wyświetl alert informujący o sukcesie
                    location.reload();  // Przeładuj stronę po pomyślnej aktualizacji
                } else {
                    // Jeśli otrzymana odpowiedź zawiera pole 'success' ustawione na False
                    alert('Wystąpił błąd: ' + response.error);  // Wyświetl alert z informacją o błędzie
                }
            }
        });
    }
});
