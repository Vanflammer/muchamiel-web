// Markdown sencillo para las guías: títulos (#, ##, ###), negrita, cursiva, enlaces, listas, citas y párrafos.
// Primero se escapa todo el HTML: lo que escribe el administrador no puede meter código en la página.
window.md = function (texto) {
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const linea = s => esc(s)
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/\*(.+?)\*/g, '<i>$1</i>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  const out = [];
  let lista = null;
  const cierra = () => { if (lista) { out.push(`</${lista}>`); lista = null; } };
  for (const l of String(texto || '').split(/\r?\n/)) {
    let m;
    if ((m = l.match(/^(#{1,3})\s+(.*)/))) { cierra(); const n = m[1].length + 1; out.push(`<h${n}>${linea(m[2])}</h${n}>`); }
    else if ((m = l.match(/^\s*[-*]\s+(.*)/))) { if (lista !== 'ul') { cierra(); out.push('<ul>'); lista = 'ul'; } out.push(`<li>${linea(m[1])}</li>`); }
    else if ((m = l.match(/^\s*\d+[.)]\s+(.*)/))) { if (lista !== 'ol') { cierra(); out.push('<ol>'); lista = 'ol'; } out.push(`<li>${linea(m[1])}</li>`); }
    else if ((m = l.match(/^>\s?(.*)/))) { cierra(); out.push(`<blockquote>${linea(m[1])}</blockquote>`); }
    else if (l.trim() === '') cierra();
    else { cierra(); out.push(`<p>${linea(l)}</p>`); }
  }
  cierra();
  return out.join('');
};
