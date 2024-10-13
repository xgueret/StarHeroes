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