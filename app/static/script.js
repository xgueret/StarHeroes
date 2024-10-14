document.addEventListener('DOMContentLoaded', function () {
    const menuBtn = document.getElementById('menu-btn');
    const contextMenu = document.getElementById('context-menu');

    menuBtn.addEventListener('click', function () {
        if (contextMenu.style.display === 'block') {
            contextMenu.style.display = 'none';
            contextMenu.classList.remove('show'); // Enlever la classe 'show'
        } else {
            contextMenu.style.display = 'block';
            setTimeout(() => {
                contextMenu.classList.add('show'); // Ajouter la classe 'show' pour la transition
            }, 10); // Petit délai pour que le navigateur prenne en compte l'affichage avant l'animation
        }
    });

    // Hide menu if click outside
    document.addEventListener('click', function (event) {
        if (!menuBtn.contains(event.target) && !contextMenu.contains(event.target)) {
            contextMenu.style.display = 'none';
            contextMenu.classList.remove('show'); // Enlever la classe 'show'
        }
    });
});

// Gestion du popup d'ajout
document.getElementById('add-rule-btn').addEventListener('click', function() {
    document.getElementById('add-rule-modal').style.display = 'block';
});

// Gestion du popup d'édition
document.querySelectorAll('.edit-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
        var ruleId = btn.getAttribute('data-id');
        var ruleName = btn.getAttribute('data-name');
        var ruleDescription = btn.getAttribute('data-description');
        document.getElementById('edit-rule-name').value = ruleName;
        document.getElementById('edit-rule-description').value = ruleDescription;
        document.getElementById('edit-rule-form').action = '/parent/rules/edit/' + ruleId;
        document.getElementById('edit-rule-modal').style.display = 'block';
    });
});

// Fermer les popups
document.querySelectorAll('.close').forEach(function(closeBtn) {
    closeBtn.addEventListener('click', function() {
        document.querySelectorAll('.modal').forEach(function(modal) {
            modal.style.display = 'none';
        });
    });
});