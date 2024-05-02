document.getElementById('scrapingButton').addEventListener('click', function() {
    document.getElementById('loadingModal').style.display = 'flex';
    // Redirige après un court délai pour permettre à la modale de s'afficher
    setTimeout(function() {
        window.location.href = '/scraping_chevaux_bases';
    }, 500);  // ajustez ce délai si nécessaire
});
