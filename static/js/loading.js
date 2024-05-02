document.querySelectorAll('[name="action"]').forEach(button => {
    button.addEventListener('click', function(event) {
        document.getElementById('loadingModal').style.display = 'flex';
    });
});
