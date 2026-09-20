// Small local enhancement: content remains readable without JavaScript.
const contentSearch = document.querySelector('[data-content-search]');
if (contentSearch) {
  const cards = [...document.querySelectorAll('[data-search]')];
  const count = document.querySelector('.results-count');
  const empty = document.querySelector('[data-no-results]');
  contentSearch.addEventListener('input', () => {
    const query = contentSearch.value.trim().toLowerCase();
    let shown = 0;
    cards.forEach(card => {
      card.hidden = !card.dataset.search.toLowerCase().includes(query);
      if (!card.hidden) shown += 1;
    });
    count.textContent = `${shown} ${shown === 1 ? 'result' : 'results'}`;
    empty.hidden = shown !== 0;
  });
}
