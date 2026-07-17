# Rutina de actualización — instrucciones

Objetivo: mantener el tablero al día ingiriendo reportes de monitoreo nuevos.

## Flujo del equipo
1. Deja el nuevo reporte de monitoreo (`.docx`) en la carpeta `reportes/`.
2. Haz commit y push (o espera a la rutina programada).

## Qué hace la rutina en cada corrida
1. Entra al repositorio (local: `~/Downloads/guerra-sucia-siapa`; o clónalo por SSH: `git@github.com:alexmorejim/guerra-sucia-siapa.git`).
2. `git pull` para tener lo último.
3. Lee `procesados.json` y lista los `.docx` de `reportes/` que **no** estén ahí (reportes nuevos).
4. Por cada reporte nuevo, extrae sus publicaciones y agrégalas a `datos.json`:
   - Cada publicación: `{id, plataforma, pagina, fecha (ISO), tema, titulo, alcance, enlace, mensaje, react{...}, com_rep, com_acc, auth, compartidas, objetivo}`.
   - No dupliques (compara por `enlace` o `titulo`+`pagina`).
   - Actualiza personajes/pauta/financiamiento si el reporte trae datos nuevos.
   - Cubre **cualquier tema**, no solo SIAPA.
5. Actualiza `meta.actualizado` con la fecha/hora actual (ISO, zona -06:00).
6. Añade el nombre de cada reporte procesado a `procesados.json`.
7. Ejecuta `python3 build_embed.py` (sincroniza el respaldo embebido).
8. `git add -A && git commit && git push`. GitHub Pages republica solo.
9. Si NO hay reportes nuevos, no cambies nada y termina.

## Nota
La rutina no scrapea Facebook/Instagram/X (las plataformas lo bloquean). Depende de los
reportes que el equipo deja en `reportes/`. Para pauta por actor, usar la Biblioteca de
Anuncios de Meta.
