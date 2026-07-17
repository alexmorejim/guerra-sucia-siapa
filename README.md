# Guerra Sucia SIAPA — Tablero de monitoreo

Tablero web (dinámico) para el monitoreo de desinformación en redes sociales contra Morena
y figuras aliadas de la 4T en Jalisco (tema deuda de agua UdeG–SIAPA).

## Cómo funciona

- **`index.html`** — la página. No se edita para actualizar datos. Lee `datos.json`, se
  **auto-refresca cada hora** y muestra la fecha de "última actualización". Trae una copia
  de respaldo embebida, así que también abre con doble clic (sin servidor).
- **`datos.json`** — todos los números (publicaciones, reacciones, alcance, comentarios,
  personajes, financiamiento). **Actualizar el tablero = actualizar este archivo.**
- **`reportes/`** — aquí se dejan los documentos de monitoreo nuevos (.docx). La rutina de
  actualización los lee para regenerar `datos.json`.

## Actualización automática (rutina de Claude)

Una rutina programada de Claude corre en cadencia y:
1. Busca el reporte más reciente en `reportes/`.
2. Extrae los datos y reescribe `datos.json` (y el bloque de respaldo en `index.html`).
3. Actualiza el campo `meta.actualizado` con la fecha/hora.
4. Hace `commit` y `push` al repositorio → GitHub Pages publica la nueva versión.

El flujo de trabajo del equipo: **subir el nuevo .docx de monitoreo a `reportes/`** y la
rutina se encarga del resto.

## Publicar en GitHub Pages (una sola vez)

Desde esta carpeta:

```bash
# 1. Crear el repositorio en GitHub (github.com/new) — por ejemplo: guerra-sucia-siapa
# 2. Conectar y subir:
git remote add origin https://github.com/TU_USUARIO/guerra-sucia-siapa.git
git branch -M main
git push -u origin main
```

Luego en GitHub: **Settings → Pages → Source: Deploy from a branch → Branch: `main` / root → Save.**

En 1–2 minutos el tablero queda en:
`https://TU_USUARIO.github.io/guerra-sucia-siapa/`

## Actualizar los datos a mano (opcional)

Editar `datos.json`, cambiar `meta.actualizado`, y:

```bash
git add datos.json && git commit -m "Actualiza datos" && git push
```

GitHub Pages republica automáticamente.
