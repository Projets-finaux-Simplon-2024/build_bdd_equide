    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('year-form');
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
    });