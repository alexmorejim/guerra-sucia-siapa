# Seguimiento casi en tiempo real con Apify

Esto conecta un scraper (Apify) a tu tablero para jalar posts de IG/FB/X de las páginas
vigiladas, con métricas reales, sin scraping casero.

## 1. Crear cuenta y token (una sola vez)
1. Crea cuenta en **https://apify.com** (hay nivel gratis para probar).
2. Ve a **Settings → API & Integrations** y copia tu **API token** (empieza con `apify_api_`).
3. En tu Mac, guárdalo como variable de entorno (NO lo pongas en ningún archivo del repo):
   ```bash
   export APIFY_TOKEN="apify_api_TU_TOKEN"
   ```
   (para que quede permanente, agrégalo a `~/.zshrc`).

## 2. Ajustar a quién rastrear
Edita **`fuentes_seguimiento.json`**: añade/quita cuentas por plataforma (IG, FB, X) con su
URL o handle. Ya vienen precargadas Pulso Jalisco, El Pueblo Vigilante, Jalcirco, Brujas Mx,
Bancada Naranja y Libro Negro.

## 3. Correr
```bash
cd ~/Downloads/guerra-sucia-siapa
python3 apify_ingest.py
git add datos.json index.html && git commit -m "Nuevos posts (Apify)" && git push
```
Los posts nuevos aparecen en el **Feed** del tablero con reacciones/comentarios reales.
Al correr, el script **no duplica** (compara por enlace).

## 4. Automático (opcional)
La **rutina programada** ya corre `apify_ingest.py` automáticamente **si** `APIFY_TOKEN`
está configurado. Así el tablero se actualiza solo cada día (o cambia la frecuencia).

## Notas
- **Costo**: Apify cobra por uso. `resultsLimit` (en la config) controla cuántos posts por
  cuenta; súbelo/bájalo según tu presupuesto. "Tiempo real" = correr más seguido = más costo.
- **Términos**: scrapear IG/FB/X va contra los Términos de Meta/X. Úsalo bajo tu criterio.
- **Si un Actor falla o cambia**: ajusta su `id` en `fuentes_seguimiento.json` (sección
  `actors`) o su input en `build_input()` dentro de `apify_ingest.py`. Alternativas de Actor:
  `apify/instagram-scraper`, `apify/facebook-posts-scraper`, `apidojo/tweet-scraper`.
- **`objetivo` y `tema`** llegan vacíos ("por clasificar"): la rutina o tú los clasifican
  después (a qué figura ataca cada post).
