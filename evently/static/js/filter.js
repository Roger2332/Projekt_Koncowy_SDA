// Pobierz element przycisku, który będzie przełączał widoczność sekcji filtrowania
document.getElementById('toggleFilters').addEventListener('click', function () {
    // Pobierz element sekcji filtrowania
    var filterSection = document.getElementById('filterSection');

    // Sprawdź aktualny styl wyświetlania sekcji filtrowania
    if (filterSection.style.display === 'none') {
        // Jeśli sekcja jest ukryta (display === 'none'), pokaż ją (display === 'block')
        filterSection.style.display = 'block';
    } else {
        // Jeśli sekcja jest widoczna (display !== 'none'), ukryj ją (display === 'none')
        filterSection.style.display = 'none';
    }
});