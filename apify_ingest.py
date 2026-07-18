#!/usr/bin/env python3
"""
Integración Apify -> datos.json (seguimiento casi en tiempo real).

Qué hace:
  1. Lee fuentes_seguimiento.json (cuentas a rastrear por plataforma).
  2. Llama a los Actors de Apify (Instagram / Facebook / X) con tu token.
  3. Transforma los posts al esquema del tablero y los mete a datos.json (sin duplicar).
  4. Actualiza meta.actualizado y ejecuta build_embed.py.

Requisitos:
  - Cuenta de Apify (nivel gratis sirve para probar): https://apify.com
  - Token de API en la variable de entorno APIFY_TOKEN (NO lo pongas en ningún archivo del repo):
        export APIFY_TOKEN="apify_api_xxx"
  - Uso:  python3 apify_ingest.py

Nota: scrapear IG/FB/X va contra los Términos de Meta/X; úsalo bajo tu criterio.
Los esquemas de los Actors cambian con el tiempo: si un Actor falla, ajusta su id o su
input en fuentes_seguimiento.json / en build_input().
"""
import os, sys, json, urllib.request, urllib.error, pathlib

BASE = pathlib.Path(__file__).parent
TOKEN = os.environ.get("APIFY_TOKEN", "").strip()


def run_actor(actor_id, run_input, timeout=300):
    """Corre un Actor de Apify y devuelve los items del dataset (lista de dicts)."""
    url = (f"https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items"
           f"?token={TOKEN}&timeout={timeout}")
    data = json.dumps(run_input).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout + 30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"  ! Actor {actor_id} HTTP {e.code}: {e.read().decode('utf-8')[:200]}")
    except Exception as e:
        print(f"  ! Actor {actor_id} error: {e}")
    return []


def build_input(plataforma, cuentas, limit):
    """Arma el input de cada Actor. Ajusta aquí si cambian los esquemas."""
    if plataforma == "instagram":
        return {"directUrls": [c["url"] for c in cuentas],
                "resultsType": "posts", "resultsLimit": limit}
    if plataforma == "facebook":
        return {"startUrls": [{"url": c["url"]} for c in cuentas], "resultsLimit": limit}
    if plataforma == "x":
        return {"twitterHandles": [c["handle"] for c in cuentas], "maxItems": limit}
    return {}


def g(d, *keys):
    """Primer valor no vacío entre varias llaves posibles."""
    for k in keys:
        v = d.get(k)
        if v not in (None, "", []):
            return v
    return None


def to_post(item, plataforma, nombre_default):
    """Mapea un item de Apify al esquema de post del tablero (campos con fallback)."""
    texto = g(item, "caption", "text", "postText", "message") or ""
    url = g(item, "url", "postUrl", "link") or None
    enlace = url.replace("https://", "").replace("http://", "") if url else None
    likes = g(item, "likesCount", "likes", "likeCount", "reactionsCount")
    coments = g(item, "commentsCount", "comments", "replyCount")
    shares = g(item, "sharesCount", "shares", "retweetCount")
    fecha = g(item, "timestamp", "time", "createdAt", "date")
    pagina = g(item, "ownerUsername", "pageName", "username", "authorName") or nombre_default
    titulo = (texto[:90] + "…") if len(texto) > 90 else (texto or f"Publicación de {pagina}")
    plat = {"instagram": "Instagram", "facebook": "Facebook", "x": "X (Twitter)"}[plataforma]
    return {
        "plataforma": plat, "pagina": pagina, "fecha": fecha, "tema": "por clasificar",
        "titulo": titulo, "alcance": None, "enlace": enlace, "mensaje": texto,
        "react": {"like": int(likes)} if isinstance(likes, (int, float)) else {},
        "com_rep": int(coments) if isinstance(coments, (int, float)) else 0,
        "com_acc": None, "auth": None,
        "compartidas": int(shares) if isinstance(shares, (int, float)) else 0,
        "objetivo": None, "fuente": url, "origen": "apify",
    }


def main():
    if not TOKEN:
        sys.exit("Falta APIFY_TOKEN. Haz:  export APIFY_TOKEN=\"apify_api_xxx\"  y vuelve a correr.")
    cfg = json.loads((BASE / "fuentes_seguimiento.json").read_text(encoding="utf-8"))
    datos = json.loads((BASE / "datos.json").read_text(encoding="utf-8"))
    posts = datos["posts"]
    vistos = {p.get("enlace") for p in posts if p.get("enlace")}
    next_id = max((p["id"] for p in posts), default=0) + 1
    nuevos = 0

    for plataforma, cuentas in cfg["cuentas"].items():
        if not cuentas:
            continue
        actor = cfg["actors"].get(plataforma)
        print(f"→ {plataforma}: {len(cuentas)} cuenta(s) vía {actor}")
        items = run_actor(actor, build_input(plataforma, cuentas, cfg.get("resultsLimit", 10)))
        default_name = cuentas[0]["nombre"]
        for it in items:
            post = to_post(it, plataforma, default_name)
            if post["enlace"] and post["enlace"] in vistos:
                continue          # ya existe
            post["id"] = next_id; next_id += 1
            if post["enlace"]:
                vistos.add(post["enlace"])
            posts.append(post); nuevos += 1
        print(f"   {len(items)} items · {nuevos} nuevos acumulados")

    if nuevos:
        # sello de actualización (usa la hora del sistema; -06:00 Guadalajara)
        import datetime
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-6)))
        datos["meta"]["actualizado"] = now.strftime("%Y-%m-%dT%H:%M:%S-06:00")
        (BASE / "datos.json").write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        os.system(f'python3 "{BASE / "build_embed.py"}"')
        print(f"✓ {nuevos} publicaciones nuevas agregadas a datos.json")
    else:
        print("Sin publicaciones nuevas.")


if __name__ == "__main__":
    main()
