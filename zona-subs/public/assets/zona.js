// Cabecera común de la zona de subs: nombre y avatar de quien ha entrado, y botón de salir.
// Botón «Menú» del móvil: abre y cierra la navegación.
(() => {
  const b = document.querySelector('.menu-btn'), cab = document.querySelector('header.cab');
  if (!b || !cab) return;
  b.onclick = () => { const abre = !cab.classList.contains('abierto'); cab.classList.toggle('abierto', abre); b.setAttribute('aria-expanded', abre); };
})();
(async () => {
  const h = document.querySelector('header .yo');
  if (!h) return;
  try {
    const yo = await fetch('/api/yo').then(r => r.json());
    h.innerHTML = (yo.avatar ? `<img src="${yo.avatar}" alt="">` : '') + `<span>${yo.nombre.replace(/[<>&]/g, '')}${yo.prueba ? ' (prueba)' : ''}</span> · <a href="/salir">Salir</a>`;
  } catch { /* sin datos, se queda vacío */ }
})();
