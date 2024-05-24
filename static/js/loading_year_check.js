document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('year-form');
    let startTime;

    document.querySelectorAll('[name="action"]').forEach(button => {
        button.addEventListener('click', function(event) {
            let isChecked = false;
            document.querySelectorAll('input[type="checkbox"][name="annees[]"]').forEach(function(checkbox) {
                if (checkbox.checked) {
                    isChecked = true;
                }
            });
            if (!isChecked) {
                alert('Veuillez sélectionner au moins une année.');
                event.preventDefault(); // Empêche l'action par défaut
            } else {
                const actionValue = this.value;
                if (actionValue === 'scraping') {
                    startTimer(); // Lancer le timer seulement pour l'action de scraping
                }
                document.getElementById('loadingModal').style.display = 'flex'; // Affiche la modalité seulement si la validation est réussie
            }
        });
    });

    form.addEventListener('submit', function(event) {
        let isChecked = false;
        document.querySelectorAll('input[type="checkbox"][name="annees[]"]').forEach(function(checkbox) {
            if (checkbox.checked) {
                isChecked = true;
            }
        });
        if (!isChecked) {
            alert('Veuillez sélectionner au moins une année.');
            event.preventDefault(); // Empêche la soumission du formulaire
        }
    });

    function startTimer() {
        startTime = new Date(); // Heure de départ
        document.getElementById('timerDisplay').style.display = 'block';
        document.getElementById('modalMessage').textContent = 'Scraping en cours...'; // Change le message de la modal
        updateTimer();
    }

    function updateTimer() {
        const now = new Date();
        const elapsed = now - startTime; // Temps écoulé en millisecondes
        const hours = Math.floor(elapsed / 3600000);
        const minutes = Math.floor((elapsed % 3600000) / 60000);
        const seconds = Math.floor((elapsed % 60000) / 1000);

        document.getElementById('elapsedTime').textContent = 
            `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

        requestAnimationFrame(updateTimer); // Mettre à jour le timer à chaque frame
    }
});
