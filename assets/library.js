/* ---------- library catalogue renderer ---------- */
(function(){
  const host = document.getElementById('libHost');
  if (!host || typeof LIBRARY === 'undefined') return;

  const chips = document.createElement('div');
  chips.className = 'lib-tools rv on';
  const all = [{k: 'all', label: 'All shelves'}].concat(
    LIBRARY.order.map(g => ({k: g, label: g + ' · ' + LIBRARY.groups[g].length}))
  );
  chips.innerHTML = all.map((c, i) =>
    `<button class="lib-chip${i === 0 ? ' active' : ''}" data-g="${c.k}">${c.label}</button>`).join('');
  host.before(chips);

  host.innerHTML = LIBRARY.order.map(g => `
    <div class="lib-group" data-g="${g}">
      <h3>${g} <span>${LIBRARY.groups[g].length} BOOKS</span></h3>
      ${LIBRARY.groups[g].map((b, i) => `
        <div class="lib-book" data-scan="${b.scan ? '1' : '0'}">
          <span class="bn">${String(i + 1).padStart(2, '0')}</span>
          <span class="bt">${b.t}</span>
          <span class="bm">${b.scan ? '<span class="scan">SCANNED ORIGINAL</span> · ' : ''}${b.p} PP</span>
        </div>`).join('')}
    </div>`).join('');

  chips.addEventListener('click', e => {
    const btn = e.target.closest('.lib-chip');
    if (!btn) return;
    chips.querySelectorAll('.lib-chip').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    const g = btn.dataset.g;
    host.querySelectorAll('.lib-group').forEach(grp => {
      grp.classList.toggle('hide', g !== 'all' && grp.dataset.g !== g);
    });
  });
})();
