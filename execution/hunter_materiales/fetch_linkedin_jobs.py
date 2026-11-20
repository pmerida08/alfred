import sys, re, html, urllib.request, os, time
os.makedirs("jobs", exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"
for jid in sys.argv[1:]:
    try:
        req = urllib.request.Request(f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{jid}", headers={"User-Agent": UA})
        t = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    except Exception as e:
        print(jid, "ERR", e); continue
    title = re.search(r'topcard__title[^>]*>([\s\S]*?)<', t)
    comp = re.search(r'topcard__org-name-link[^>]*>([\s\S]*?)<', t)
    loc = re.search(r'topcard__flavor topcard__flavor--bullet[^>]*>([\s\S]*?)<', t)
    m = re.search(r'show-more-less-html__markup[^>]*>([\s\S]*?)</div>', t)
    d = m.group(1) if m else ""
    d = re.sub(r'<br\s*/?>|</(p|li|h\d)>', '\n', d); d = re.sub(r'<li[^>]*>', '- ', d); d = re.sub(r'<[^>]+>', ' ', d)
    d = html.unescape(d); d = re.sub(r'[ \t]+', ' ', d); d = re.sub(r'\n\s*\n+', '\n', d).strip()
    crit = [html.unescape(x.strip()) for x in re.findall(r'description__job-criteria-text[^>]*>([\s\S]*?)</span>', t)]
    head = " | ".join(html.unescape((x.group(1) if x else "").strip()) for x in (title, comp, loc))
    open(f"jobs/{jid}.txt", "w", encoding="utf-8").write(f"{head}\nCRIT: {crit}\nURL: https://www.linkedin.com/jobs/view/{jid}/\n\n{d}\n")
    print(jid, head[:100], len(d))
    time.sleep(0.5)
