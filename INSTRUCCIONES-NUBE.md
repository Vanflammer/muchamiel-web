# Instrucciones para la actualización diaria (Claude en la nube)

Este repositorio es el **generador** de la web de guías de WoW Forever del streamer Muchamiel: https://muchamielwow.github.io.
La web publicada vive en otro repositorio (`muchamielwow/muchamielwow.github.io`, de Muchamiel). **Tú no subes allí**: una tarea
de ese repositorio copia `web/dist` de aquí cada 30 minutos. Tu trabajo termina con un `git push` a la rama `main` de **este** repositorio.

## Cómo está hecha
- `python comunidad_portal.py` regenera toda la web en `web/dist` partiendo de `web/base-gpt` (tarda 1-2 minutos). Hazlo siempre con `PYTHONIOENCODING=utf-8`.
- Las páginas y noticias se escriben en Python dentro de los generadores:
  - `comunidad_portal.py`: noticias de Forever. Ejemplos a copiar: `novedades29_page`, `dia1_page`, `raciales26_page`; tarjetas `news-card` de la página de noticias; diapositivas `slide(...)` del carrusel (dentro de `slides = [`); la lista `A_MEDIAS` (lo no confirmado) y la página `a_medias_page`. Cada página nueva se llama desde `run`/la lista de páginas (busca `dia1_page()` y añade la tuya debajo).
  - `forever_portal.py`, `cambios_beta.py`, `parche_26oct.py`: notas de parche y cambios de clase.
  - `retail_portal.py`: la parte de WoW Retail (lista `NOTICIAS`).
  - `oficializar_portal.py`: migas de pan de cada sección (busca `'dia-1'` y copia el patrón para una página nueva).
- Inglés: tras generar, `traducciones/en-pendientes.json` lista los textos sin traducir. Traduce **todos** (mismo HTML, mismo orden) y añádelos a `traducciones/en.json` (objeto texto castellano → inglés). Vuelve a generar hasta que la línea `Inglés: X/Y` tenga X = Y.
- Comprobación: `python verificar_portal.py` debe terminar con «ZIP íntegro».

## Reglas de contenido
- **Solo lo confirmado por Blizzard** (notas, mensajes del equipo, pódcast o entrevistas oficiales) va a páginas normales.
- **Lo no confirmado va a «A medias»** (`A_MEDIAS`), con su etiqueta: `juego` (en el juego sin nota oficial), `confirmado` (anunciado sin detalles), `pista` (lo insinúa Blizzard) o `rumor` (datos de la beta, filtraciones).
- Todo con palabras propias: nada copiado literal. No cites ni nombres a youtubers o creadores; como fuente se enlaza a Blizzard o a webs (Wowhead, Icy Veins…).
- Horas en hora de España; si es un evento, añade México y Chile/Argentina con (*). Castellano neutro (evita «coger»).
- Si no hay nada nuevo que merezca la pena, no cambies nada y no hagas commit.
- No toques `MuchamielLockPvP/`, `zona-subs/` (se publica aparte), `web/base-gpt/` (salvo que haga falta para una página), `radar_fuentes.json` ni `publicar.yml`. No borres páginas.

## Fuentes
- Radar (cada hora): https://raw.githubusercontent.com/muchamielwow/muchamielwow.github.io/main/.github/radar/RADAR.md
- Wowhead: su RSS https://www.wowhead.com/news/rss/forever trae el texto completo (la web bloquea la descarga directa).
- Blizzard: https://us.forums.blizzard.com/en/wow/groups/blizzard-tracker/posts.json (mensajes del equipo).
- Vídeos: subtítulos con `pip install yt-dlp` y `python -m yt_dlp --skip-download --write-auto-subs --sub-langs "es.*,en.*" URL`.
