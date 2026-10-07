document.documentElement.classList.add('js');
const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#navigation');
toggle?.addEventListener('click', () => {
  const expanded = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(expanded));
  nav.classList.toggle('is-open', expanded);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') {
    toggle.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
    toggle.focus();
  }
});
const search = document.querySelector('#pub-search');
if (search) {
  const type = document.querySelector('#pub-type');
  const year = document.querySelector('#pub-year');
  const rows = [...document.querySelectorAll('#publications .publication')];
  const filter = () => {
    const query = search.value.trim().toLowerCase();
    let count = 0;
    for (const row of rows) {
      const visible = row.textContent.toLowerCase().includes(query)
        && (!type.value || row.dataset.type === type.value)
        && (!year.value || row.dataset.year === year.value);
      row.hidden = !visible;
      count += Number(visible);
    }
    document.querySelector('#pub-count').textContent = `${count} publication${count === 1 ? '' : 's'}`;
    document.querySelector('#pub-empty').hidden = count > 0;
  };
  search.addEventListener('input', filter);
  type.addEventListener('change', filter);
  year.addEventListener('change', filter);
}
