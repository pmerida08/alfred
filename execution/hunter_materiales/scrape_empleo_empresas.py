"""Localiza el apartado de empleo en la web de cada empresa y clasifica como se deja el CV.

Uso: python scrape_empleo_empresas.py empresas.csv salida.json
CSV de entrada: nombre,dominio,ciudad,ccaa. Solo lee paginas publicas; no envia nada.
La clasificacion es orientativa: los sitios renderizados con JS hay que comprobarlos en el navegador.
"""
import csv, json, re, sys
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
      "Accept-Language": "es-ES,es;q=0.9"}
LINK = re.compile(r"emple|trabaj|career|carrera|jobs?\b|[uú]nete|join[- ]?(us|the)|talent|vacante|candidat|ofertas|work[- ]with", re.I)
FUERTE = re.compile(r"trabaja|career|empleo|[uú]nete|jobs?\b|join[- ]?us", re.I)
RUTAS = ["/careers", "/empleo", "/trabaja-con-nosotros", "/unete", "/jobs", "/talento"]
ATS = {"greenhouse.io": "Greenhouse", "lever.co": "Lever", "workable.com": "Workable", "teamtailor.com": "Teamtailor",
       "ashbyhq.com": "Ashby", "personio.": "Personio", "factorialhr.com/job": "Factorial", "myworkdayjobs": "Workday",
       "successfactors": "SuccessFactors", "smartrecruiters.com": "SmartRecruiters", "bamboohr.com": "BambooHR",
       "recruitee.com": "Recruitee", "join.com": "JOIN", "hrbf.": "HRBF", "talentclue": "TalentClue", "sesametime": "Sesame",
       "icims.com": "iCIMS", "breezy.hr": "Breezy", "jobs.lever": "Lever", "gem.com": "Gem", "softgarden": "Softgarden"}
ESPONT = re.compile(r"espont[aá]ne|autocandidatura|d[eé]janos tu cv|env[ií]anos tu (cv|curr)|m[aá]ndanos tu cv|open application|general application|bolsa de (empleo|trabajo)|no encuentras", re.I)


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.file_inputs, self.forms = [], 0, 0
        self._a, self._txt = None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self._a, self._txt = a["href"], []
        elif tag == "form":
            self.forms += 1
        elif tag == "input" and (a.get("type") or "").lower() == "file":
            self.file_inputs += 1

    def handle_data(self, data):
        if self._a is not None:
            self._txt.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._a is not None:
            self.links.append((self._a, " ".join("".join(self._txt).split())))
            self._a = None


def get(url):
    try:
        r = requests.get(url, headers=UA, timeout=15, allow_redirects=True)
        if r.status_code == 200 and "html" in r.headers.get("content-type", ""):
            r.encoding = r.apparent_encoding if not r.encoding or r.encoding.lower() == "iso-8859-1" else r.encoding
            return r.url, r.text
        return r.url, None
    except requests.RequestException:
        return url, None


def parse(html):
    p = Parser()
    try:
        p.feed(html)
    except Exception:
        pass
    return p


def analiza(html):
    p = parse(html)
    ats = sorted({n for k, n in ATS.items() if k in html.lower()})
    mails = sorted({m.lower() for m in re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", html)
                    if not re.search(r"\.(png|jpg|svg|webp|gif)$|sentry|wixpress|example|domain\.", m, re.I)})
    return {"file_inputs": p.file_inputs, "forms": p.forms, "ats": ats, "emails": mails[:4], "espontanea": bool(ESPONT.search(html))}


def procesa(e):
    r = dict(e, web=None, empleo=None, via="sin_web")
    home_url, home = get("https://" + e["dominio"])
    if home is None:
        home_url, home = get("https://www." + e["dominio"])
    if home is None:
        return r
    r["web"] = home_url
    cand = {}
    for href, txt in parse(home).links:
        if href.startswith(("mailto:", "tel:", "#", "javascript:")):
            continue
        if LINK.search(txt) or LINK.search(href):
            score = 2 * bool(FUERTE.search(txt)) + bool(FUERTE.search(href))
            cand[urljoin(home_url, href)] = max(score, cand.get(urljoin(home_url, href), 0))
    urls = [u for u, _ in sorted(cand.items(), key=lambda kv: -kv[1])][:3]
    if not urls:
        base = f"{urlparse(home_url).scheme}://{urlparse(home_url).netloc}"
        urls = [base + x for x in RUTAS]
    mejor, mejor_pts = None, -1
    for u in urls:
        fin, html = get(u)
        if html is None:
            continue
        a = analiza(html)
        pts = 4 * bool(a["file_inputs"]) + 3 * bool(a["ats"]) + 2 * a["espontanea"] + bool(a["emails"]) + bool(FUERTE.search(fin))
        if pts > mejor_pts:
            mejor, mejor_pts = dict(a, url=fin), pts
    if not mejor:
        r["via"] = "sin_apartado"
        return r
    r.update(empleo=mejor["url"], file_inputs=mejor["file_inputs"], ats=mejor["ats"], emails=mejor["emails"], espontanea=mejor["espontanea"])
    r["via"] = "formulario_cv" if mejor["file_inputs"] else "ats" if mejor["ats"] else "email" if mejor["emails"] else "pagina_sin_form"
    return r


def main():
    with open(sys.argv[1], encoding="utf-8") as fh:
        empresas = list(csv.DictReader(fh))
    with ThreadPoolExecutor(10) as ex:
        res = list(ex.map(procesa, empresas))
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    for r in res:
        print(f"{r['via']:16} {r['nombre'][:22]:22} {r.get('empleo') or r.get('web') or '-'} {','.join(r.get('ats') or [])} {'ESP' if r.get('espontanea') else ''}")


main()
