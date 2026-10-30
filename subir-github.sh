#!/usr/bin/env bash
# Sube web/dist a muchamielwow.github.io. Desde el 16-10 el repositorio tiene una tarea de GitHub (.github/) que actualiza
# datos/avisos-blizzard.json por su cuenta: por eso primero se trae lo de GitHub y nunca se borra .github.
set -e
cd "$(dirname "$0")"
G=github-pages
# 29-10: primero se guarda el generador en github.com/Vanflammer/muchamiel-web (lo usa la tarea diaria en la nube y,
# cada 30 min, la tarea «Publicar la web» del GitHub de Muchamiel copia de ahí web/dist). Si no se guardara, esa tarea
# devolvería la web a la versión anterior.
[ -d ../MuchamielLockPvP ] && cp -r ../MuchamielLockPvP/. MuchamielLockPvP/  # la copia del addon para la nube, al día
git add -A && { git diff --cached --quiet || git commit -q -m "${1:-Actualización de la web}

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"; }
{ git pull -q --rebase && git push -q; } || echo "AVISO: no se pudo guardar el generador en github.com/Vanflammer/muchamiel-web"
git -C $G fetch -q origin && git -C $G reset -q --hard origin/main
# marcas/ es de Muchamiel (su media kit, que sube él desde GitHub): no se borra ni se pisa (Van 16-10).
find $G -mindepth 1 -maxdepth 1 ! -name .git ! -name .nojekyll ! -name .github ! -name marcas -exec rm -rf {} +
cp -r web/dist/. $G/
rm -f $G/_worker.js $G/_routes.json $G/_fuentes.html
cp avisos_blizzard.py $G/.github/avisos_blizzard.py
cp youtube_directo.py $G/.github/youtube_directo.py
cp avisos.yml $G/.github/workflows/avisos.yml  # la tarea de GitHub: su fuente está aquí (el reset de arriba la pisaría)
cp actualizar_talentos.py $G/.github/actualizar_talentos.py  # 16-10: talentos de la calculadora cada 6 h
cp talentos.yml $G/.github/workflows/talentos.yml
cp MANUAL-WEB-github.md $G/.github/README.md  # 29-10: manual de la web, se ve en la portada del repositorio
cp radar.py $G/.github/radar.py  # 29-10: radar de novedades para la IA de Muchamiel
cp radar.yml $G/.github/workflows/radar.yml
cp publicar.yml $G/.github/workflows/publicar.yml
cp momentos.py $G/.github/momentos.py  # 30-10: mejores momentos de cada directo (chat de Twitch)
cp momentos.yml $G/.github/workflows/momentos.yml
mkdir -p $G/.github/radar
[ -f $G/.github/radar/fuentes.json ] || cp radar_fuentes.json $G/.github/radar/fuentes.json  # las fuentes son de Muchamiel: solo la primera vez
git -C $G add -A
git -C $G commit -q -m "${1:-Actualización de la web}

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || echo "sin cambios"
git -C $G push -q
git -C $G log --oneline -1
