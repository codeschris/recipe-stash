const readMore = document.getElementById('readMore');
const recipe = document.getElementById('recipe');

readMore.addEventListener('click', () => {
    recipe.classList.toggle('hidden');
})