document.querySelectorAll('.subscribe-btn').forEach(button => {
    button.addEventListener('click', function () {
        const eventId = this.getAttribute('data-event-id');
        const formId = `#subscribeForm${eventId}`;
        document.querySelector(formId).submit();
    });
});
