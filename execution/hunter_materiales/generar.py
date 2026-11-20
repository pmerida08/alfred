"""Generador HUNTER: CV + carta (HTML/TXT/PDF) a partir de CV/cartas base ya validados (1 pagina, ATS).

Las bases son candidaturas reales en agents/hunter/candidaturas (TECDATA = ES con marca, ATEXIS = ES sin marca,
Juryo = EN). Cada oferta se describe en un fichero specs_*.py (ver specs_2026-11-04.py). Escribe en candidaturas/,
Empleos/ del vault y .tmp/hunter_outbox/, renderiza PDF con Chrome headless e imprime las paginas: si el CV sale
con 2 paginas, acorta perfil o habilidades y vuelve a generar ese slug.
La fecha de la carta sale de FECHA_ES / FECHA_EN del fichero de specs.
"""
import re, os, shutil, subprocess, sys, html as H
import importlib.util

# Uso: python generar.py specs_AAAA-MM-DD.py [slug ...]
_spec = importlib.util.spec_from_file_location("specs", sys.argv[1])
_mod = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_mod)
OFERTAS = _mod.OFERTAS

# Rutas relativas al repo, válidas en el PC y en el servidor Linux. El vault (Empleos/) y Chrome solo
# existen en el PC: en el servidor se omiten la copia a Empleos/ y el PDF, y se avisa.
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CAND = os.path.join(_ROOT, "agents", "hunter", "candidaturas")
OUTBOX = os.path.join(_ROOT, ".tmp", "hunter_outbox")
EMPLEOS = r"D:\Obsidian\Mi Bóveda\Empleos"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HAS_EMPLEOS = os.path.isdir(EMPLEOS)
HAS_CHROME = os.path.isfile(CHROME)
os.makedirs(OUTBOX, exist_ok=True)
if not HAS_EMPLEOS:
    print("AVISO: sin vault (Empleos/ no existe aquí): no se copia al vault.")
if not HAS_CHROME:
    print("AVISO: sin Chrome: no se generan PDF ni se comprueba que el CV quepa en una página.")

BASE = {
    ("es", True): ("CV-TECDATA-AIEngineerJuniorIAGenerativaAgentes.html", "Carta-TECDATA-AIEngineerJuniorIAGenerativaAgentes.html"),
    ("es", False): ("CV-ATEXIS-ProgrammerAnalyst.html", "Carta-ATEXIS-ProgrammerAnalyst.html"),
    ("en", True): ("CV-Juryo-AIEngineer.html", "Carta-Juryo-AIEngineer.html"),
    ("en", False): ("CV-Juryo-AIEngineer.html", "Carta-Juryo-AIEngineer.html"),
}

PROY = {
 "es": {
  "alfred": ("Alfred — Sistema multi-agente de IA en producción", "May 2026 – Actualidad", "Sistema multi-agente en Python sobre la Claude API, 24/7 en un servidor Linux: agentes especializados con memoria persistente, tool calling e integraciones por API (Gmail, Notion, Google Sheets, Telegram). Lee ofertas, puntúa el encaje y genera documentos de candidatura a medida, como este."),
  "lifevault": ("LifeVault — SaaS de documentos con IA", "Abr 2026 – Jun 2026", "Asistente de IA sobre los documentos del propio usuario: búsqueda semántica con embeddings y chatbot con contexto persistente. TypeScript, React Native, PostgreSQL (Supabase), Netlify CI/CD."),
  "elite": ("Estudiante Élite — Asistente de tutoría con IA", "Ene 2026 – Feb 2026", "Asistente de tutoría con IA para estudiantes de derecho: RAG sobre el temario, memoria de sesión y transcripción de audio con Whisper. React 19 + TypeScript, Supabase, n8n."),
  "streakode": ("Streakode — PWA de práctica diaria de código", "Sep 2026 – Actualidad", "PWA en producción con rachas, XP, rankings y un reto diario cronometrado en servidor. Next.js, TypeScript, Supabase con RLS y pg_cron, tests automáticos, notificaciones de retención por push y email."),
 },
 "en": {
  "alfred": ("Alfred — Multi-agent AI system in production", "May 2026 – Present", "Python multi-agent system on the Claude API running 24/7 on a Linux server: specialised agents with persistent memory, tool calling and API integrations (Gmail, Notion, Google Sheets, Telegram). It reads job postings, scores fit and generates tailored application documents such as this one."),
  "lifevault": ("LifeVault — AI document management SaaS", "Apr 2026 – Jun 2026", "AI assistant over the user's own documents: semantic search with embeddings and a chatbot with persistent context. TypeScript, React Native, PostgreSQL (Supabase), Netlify CI/CD."),
  "elite": ("Estudiante Élite — AI tutoring assistant", "Jan 2026 – Feb 2026", "AI tutoring assistant for law students: RAG over course material, session memory and audio transcription with Whisper. React 19 + TypeScript, Supabase, n8n."),
  "streakode": ("Streakode — Daily coding practice PWA", "Sep 2026 – Present", "Live PWA with streaks, XP, rankings and a daily challenge timed on the server. Next.js, TypeScript, Supabase with RLS and pg_cron, automated tests, retention notifications by push and email."),
 },
}

BULLETS = {
 "es": {
  "sync": "Flujos de sincronización automática entre sistemas internos mediante API, eliminando la gestión manual de datos y sus errores.",
  "laravel": "Desarrollo y mantenimiento de un sistema de gestión en producción con Laravel, JavaScript y SQL: nuevas funciones, depuración y corrección de incidencias en código existente.",
  "paneles": "Paneles en tiempo real con datos actualizados diariamente mediante automatización de ingesta y reporte.",
  "proxmox": "Lideré la migración a máquinas virtuales Linux en Proxmox, reduciendo el tiempo de despliegue en 4 días.",
 },
 "en": {
  "sync": "Built automated synchronisation flows between internal systems via API, removing manual data handling and its errors.",
  "laravel": "Maintained and extended a production management system in Laravel, JavaScript and SQL: new features, debugging and fixes in existing code.",
  "paneles": "Delivered real-time dashboards refreshed daily through automated data ingestion and reporting.",
  "proxmox": "Led the migration to Linux virtual machines on Proxmox, cutting deployment time by 4 days.",
 },
}

def esc(s):
    return H.escape(s, quote=False)

def strip_watermark(doc):
    doc = re.sub(r'\s*<div class="watermark">.*?</div>', '', doc, flags=re.S)
    doc = re.sub(r'\s*\.watermark\s*\{[^}]*\}', '', doc)
    doc = re.sub(r'\s*\.watermark span\s*\{[^}]*\}', '', doc)
    return doc

def add_watermark(doc, lang, ref_doc):
    if 'class="watermark"' in doc:
        return doc
    css = "\n".join(re.findall(r'\.watermark[^{]*\{[^}]*\}', ref_doc))
    doc = doc.replace("</style>", css + "\n  </style>", 1)
    wm = ('<div class="watermark">Candidatura preparada con <span>Alfred</span> &middot; Agente de Inteligencia Artificial Personal</div>' if lang == "es"
          else '<div class="watermark">Application prepared with <span>Alfred</span> &middot; Personal AI Agent</div>')
    return doc.replace("</body>", wm + "\n</body>", 1)

def build_cv(o):
    lang, wm = o["lang"], o["wm"]
    doc = open(os.path.join(CAND, BASE[(lang, wm)][0]), encoding="utf-8").read()
    doc = re.sub(r'(<div class="subtitulo">).*?(</div>)', lambda m: m.group(1) + esc(o["subtitulo"]) + m.group(2), doc, count=1)
    doc = re.sub(r'(<div class="perfil"><div class="titulo-seccion">[^<]*</div><p>).*?(</p>)', lambda m: m.group(1) + esc(o["perfil"]) + m.group(2), doc, count=1, flags=re.S)
    skills = "\n".join(f'<p><span class="skill-cat">{esc(c)}:</span> {esc(" · ".join(items))}</p>' for c, items in o["skills"])
    doc = re.sub(r'(<div class="skills-lista">).*?(</div></div>)', lambda m: m.group(1) + "\n" + skills + "\n" + m.group(2), doc, count=1, flags=re.S)
    bl = "\n".join(f"<li>{esc(BULLETS[lang][k])}</li>" for k in o.get("bullets", ["sync", "laravel", "paneles", "proxmox"]))
    doc = re.sub(r'(<ul class="job-bullets">).*?(</ul>)', lambda m: m.group(1) + "\n" + bl + "\n" + m.group(2), doc, count=1, flags=re.S)
    if lang == "en":
        doc = re.sub(r'(<div class="job-cabecera"><span class="job-titulo">)[^<]*', r'\1Web Developer', doc)
    proys = []
    for k in o["proyectos"]:
        n, f, d = PROY[lang][k]
        d = o.get("proy_desc", {}).get(k, d)
        proys.append(f'<div class="proyecto"><div class="proyecto-nombre">{esc(n)} <span class="proyecto-fecha">· {esc(f)}</span></div><div class="proyecto-desc">{esc(d)}</div></div>')
    doc = re.sub(r'(<div class="proyectos-lista">).*?(</div></div>\s*<div><div class="titulo-seccion">(?:Educación|Education))', lambda m: m.group(1) + "\n" + "\n".join(proys) + "\n" + m.group(2), doc, count=1, flags=re.S)
    ref = open(os.path.join(CAND, BASE[("es", True)][0]), encoding="utf-8").read()
    doc = add_watermark(doc, lang, ref) if wm else strip_watermark(doc)
    return doc

def build_carta(o):
    lang, wm = o["lang"], o["wm"]
    doc = open(os.path.join(CAND, BASE[(lang, wm)][1]), encoding="utf-8").read()
    fecha = getattr(_mod, "FECHA_ES", "Montilla, 4 de noviembre de 2026") if lang == "es" else getattr(_mod, "FECHA_EN", "Montilla, Córdoba (Spain) · 4 November 2026")
    doc = re.sub(r'(<div class="meta">).*?(</div>)', lambda m: m.group(1) + fecha + m.group(2), doc, count=1)
    doc = re.sub(r'(<div class="destinatario"><div class="empresa">).*?(</div><div class="puesto">).*?(</div>)',
                 lambda m: m.group(1) + esc(o["empresa"]) + m.group(2) + ("Referencia: " if lang == "es" else "Re: ") + esc(o["puesto_ref"]) + m.group(3), doc, count=1)
    body = f'<p class="saludo">{esc(o["saludo"])}</p>\n' + "\n".join(f"      <p>{esc(p)}</p>" for p in o["parrafos"]) + "\n      "
    doc = re.sub(r'<p class="saludo">.*?(<div class="firma">)', lambda m: body + m.group(1), doc, count=1, flags=re.S)
    desp = "Un cordial saludo," if lang == "es" else "Best regards,"
    doc = re.sub(r'(<div class="firma">)[^<]*(<br>)', lambda m: m.group(1) + desp + m.group(2), doc, count=1)
    ref = open(os.path.join(CAND, BASE[("es", True)][1]), encoding="utf-8").read()
    doc = add_watermark(doc, lang, ref) if wm else strip_watermark(doc)
    txt = o["saludo"] + "\n\n" + "\n\n".join(o["parrafos"]) + f"\n\n{desp}\nPablo Mérida Velasco\n" + ("664 549 627" if lang == "es" else "+34 664 549 627") + " · pablomerida03@gmail.com\n"
    return doc, txt

def pdf(html_path, pdf_path):
    import pypdf
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", "file:///" + html_path.replace("\\", "/")],
                   capture_output=True, timeout=90)
    return len(pypdf.PdfReader(pdf_path).pages)

only = set(sys.argv[2:])
for o in OFERTAS:
    if only and o["slug"] not in only:
        continue
    slug = o["slug"]
    words = sum(len(p.split()) for p in o["parrafos"])
    cv = build_cv(o)
    carta, txt = build_carta(o)
    files = {f"CV-{slug}.html": cv, f"Carta-{slug}.html": carta, f"Carta-{slug}.txt": txt}
    for name, content in files.items():
        with open(os.path.join(CAND, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
    pages = {"CV": "?", "Carta": "?"}
    outs = list(files)
    if HAS_CHROME:
        for kind in ("CV", "Carta"):
            hp = os.path.join(CAND, f"{kind}-{slug}.html")
            pages[kind] = pdf(hp, os.path.join(CAND, f"{kind}-{slug}.pdf"))
        outs += [f"CV-{slug}.pdf", f"Carta-{slug}.pdf"]
    for name in outs:
        if HAS_EMPLEOS:
            shutil.copy2(os.path.join(CAND, name), os.path.join(EMPLEOS, name))
        shutil.copy2(os.path.join(CAND, name), os.path.join(OUTBOX, name))
    print(f"{slug}: CV {pages['CV']}p, carta {pages['Carta']}p, {words} palabras, cv {len(cv)//1024}KB")
