// Wybierz wszystkie przyciski o klasie '.subscribe-btn' i dodaj do nich nasłuchiwanie kliknięcia
document.querySelectorAll('.subscribe-btn').forEach(button => {
    button.addEventListener('click', function () {
        // Pobierz identyfikator wydarzenia z atrybutu 'data-event-id' klikniętego przycisku
        const eventId = this.getAttribute('data-event-id');
        
        // Zbuduj identyfikator formularza na podstawie eventId
        const formId = `#subscribeForm${eventId}`;
        
        // Znajdź formularz o odpowiednim id i wyślij go
        document.querySelector(formId).submit();
    });
});