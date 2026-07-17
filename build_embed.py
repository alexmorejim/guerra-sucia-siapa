#!/usr/bin/env python3
"""Sincroniza el respaldo embebido de index.html con datos.json.
Uso: python3 build_embed.py
Reescribe el bloque <script id="datos-embed"> con el contenido minificado de datos.json,
para que la página también funcione abierta con doble clic (file://), sin servidor."""
import json, re, pathlib, sys

base = pathlib.Path(__file__).parent
datos = json.loads((base / "datos.json").read_text(encoding="utf-8"))  # valida el JSON
mini = json.dumps(datos, ensure_ascii=False, separators=(",", ":"))

html = (base / "index.html").read_text(encoding="utf-8")
pat = re.compile(r'(<script id="datos-embed"[^>]*>)(.*?)(</script>)', re.S)
if not pat.search(html):
    sys.exit("No se encontró el bloque datos-embed en index.html")
html = pat.sub(lambda m: m.group(1) + "\n" + mini + "\n" + m.group(3), html)
(base / "index.html").write_text(html, encoding="utf-8")
print(f"Embed sincronizado: {len(mini)} bytes desde datos.json")
