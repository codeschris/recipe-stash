const readMore = document.querySelectorAll('.readMore');

readMore.forEach((button) => {
    button.addEventListener('click', () => {
        const recipe = button.nextElementSibling;
        recipe.classList.toggle('hidden');

        if (recipe.classList.contains('hidden')) {
            button.textContent = 'Read More';
        } else {
            button.textContent = 'Read Less';
        }
    });
});