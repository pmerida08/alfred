FECHA_ES = "Montilla, 8 de noviembre de 2026"
FECHA_EN = "Montilla, Córdoba (Spain) · 8 November 2026"

OFERTAS = [
# 1 ------------------------------------------------------------------
{
 "slug": "Logicalis-IABackendDeveloper", "lang": "es", "wm": True,
 "empresa": "Logicalis Spain", "puesto_ref": "IA & Backend Developer (remoto)",
 "subtitulo": "IA & Backend Developer · Agentes, sistemas multi-agente y Python",
 "perfil": "Desarrollador backend en Python especializado en agentes de IA (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026). Diseño y mantengo un sistema multi-agente en producción sobre la Claude API: orquestación de agentes especializados, tool calling, servidores MCP, gestión de estado y memoria, y lógica determinista que decide qué acciones necesitan confirmación humana. Git, tests automáticos y CI/CD. Disponible en remoto. Inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Agentes e IA", ["Sistemas multi-agente", "Orquestación de LLMs", "Tool calling", "MCP", "Gestión de estado y memoria", "RAG", "Claude API", "OpenAI API"]),
    ("Backend", ["Python", "APIs REST", "Webhooks", "Node.js", "PHP", "Laravel"]),
    ("Datos", ["PostgreSQL", "Supabase", "SQL", "MySQL"]),
    ("Ingeniería", ["Git", "Tests automáticos (Vitest)", "CI/CD", "Linux", "n8n (workflows)"]),
 ],
 "bullets": ["sync", "laravel", "proxmox", "paneles"],
 "proyectos": ["alfred", "elite", "lifevault", "streakode"],
 "saludo": "Estimado equipo de Logicalis:",
 "parrafos": [
  "Me presento a la oferta de IA & Backend Developer. El núcleo del puesto, diseñar agentes y sistemas multi-agente, integrarlos en servicios y APIs y combinar IA generativa con lógica determinista y reglas de negocio, es exactamente lo que hago en mis proyectos. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Alfred es mi sistema multi-agente en Python sobre la Claude API, en producción 24/7 en un servidor Linux: agentes especializados que un orquestador activa según el tema, con tool calling, servidores MCP, memoria persistente e integraciones por API con Gmail, Notion, Google Sheets y Telegram. Las reglas deterministas deciden qué puede hacer cada agente sin preguntar y qué exige confirmación humana. Estudiante Élite añade RAG con memoria de sesión, y con n8n he montado workflows que combinan pasos de IA y pasos fijos.",
  "Me atrae que sean proyectos de larga duración centrados en agentes, con un equipo del que aprender arquitectura. Para ser claro: no he usado LangChain ni LangGraph en producción, porque mis agentes llaman directamente a las APIs, y no tengo experiencia con Kubernetes ni con arquitectura hexagonal o DDD aplicadas en empresa; mi experiencia en empresa son cuatro meses.",
  "Puedo incorporarme de inmediato. Me encantaría enseñarles cómo está montado Alfred en una entrevista.",
 ],
},
# 2 ------------------------------------------------------------------
{
 "slug": "INFINIT-FullStackSoftwareEngineer", "lang": "en", "wm": False,
 "empresa": "INFINIT", "puesto_ref": "Full Stack Software Engineer (Madrid, hybrid)",
 "subtitulo": "Full Stack Software Engineer · Product-first, AI-assisted delivery",
 "perfil": "Full stack developer (Higher VET in Web Application Development, 2025; Master's in Generative AI and Innovation, 2026) who owns features end to end: a live Next.js and Supabase PWA with automated tests and continuous deployment, and a Python multi-agent system running 24/7. I develop daily with agentic coding tools (Claude Code with MCP, subagents and hooks) to ship fast without dropping quality. Willing to work from Madrid. English B2 (Cambridge, 2025).",
 "skills": [
    ("Full stack", ["TypeScript", "React", "Next.js", "Node.js", "Python", "REST APIs", "PHP", "Laravel"]),
    ("Data", ["PostgreSQL", "Supabase (RLS, cron jobs)", "SQL", "MySQL"]),
    ("Delivery", ["Git", "GitHub pull requests", "Vitest (automated tests)", "CI/CD (Vercel, Netlify)", "Linux", "Monitoring and logging"]),
    ("Agentic development", ["Claude Code", "MCP", "Subagents and hooks", "Claude API", "OpenAI API", "RAG"]),
 ],
 "bullets": ["laravel", "sync", "paneles", "proxmox"],
 "proyectos": ["streakode", "alfred", "lifevault", "elite"],
 "saludo": "Dear INFINIT team,",
 "parrafos": [
  "I am applying for the Full Stack Software Engineer role. Two things in your description match how I work: owning a feature from requirements to deployment and monitoring, and using agentic coding to deliver faster without lowering standards. I hold a Higher VET in Web Application Development (2025) and a Master's in Generative AI and Innovation (2026).",
  "Streakode is a live PWA I built alone with Next.js, TypeScript and Supabase: a server-timed daily challenge, PostgreSQL with row-level security and scheduled jobs, automated tests, continuous deployment and retention notifications by push and email. I decided what to build and what to cut. Alfred, my multi-agent system in Python on the Claude API, runs 24/7 on a Linux server I deploy and monitor. At the Agencia de Digitalización Andaluza I maintained a production management system in Laravel and SQL.",
  "Building AI products for small business owners on top of a banking core is a product I would like to help shape. To be transparent: I have not designed systems at fintech scale, and my company experience is four months, so I would be the most junior engineer on the team and would rely on code review to grow quickly.",
  "I can start immediately in Madrid. I would be glad to walk you through my code in an interview.",
 ],
},
# 3 ------------------------------------------------------------------
{
 "slug": "TECHUniversidad-IngenieroIAGenerativa", "lang": "es", "wm": True,
 "empresa": "TECH Universidad", "puesto_ref": "Ingeniero/a de IA Generativa (Taco, Tenerife)",
 "subtitulo": "Ingeniero de IA Generativa · RAG, LLMs y Python",
 "perfil": "Desarrollador de IA generativa (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) con pipelines RAG en producción: ingesta de documentos, chunking, embeddings y recuperación sobre PostgreSQL con búsqueda vectorial. Integro LLMs en Python con tool calling y memoria en un sistema multi-agente 24/7, y he construido un asistente educativo con RAG sobre un temario. Me traslado a Tenerife. Inglés B2 (Cambridge, 2025).",
 "skills": [
    ("IA generativa", ["RAG", "Embeddings", "Chunking", "Búsqueda vectorial (Supabase)", "Claude API", "OpenAI API", "Gemini API", "Whisper", "Tool calling"]),
    ("Python y datos", ["Python", "APIs REST", "PostgreSQL", "SQL", "Supabase"]),
    ("Desarrollo", ["TypeScript", "React", "Next.js", "n8n"]),
    ("Producción", ["Linux", "Git", "CI/CD", "Tests automáticos"]),
 ],
 "bullets": ["sync", "paneles", "laravel", "proxmox"],
 "proyectos": ["elite", "alfred", "lifevault", "streakode"],
 "saludo": "Estimado equipo de TECH:",
 "parrafos": [
  "Me presento a la oferta de Ingeniero/a de IA Generativa. Desarrollar pipelines RAG para mejorar la atención al usuario en una universidad digital es muy cercano a lo que ya he construido para estudiantes. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Estudiante Élite es un asistente de tutoría para estudiantes de derecho con RAG sobre el temario, memoria de sesión y transcripción de audio con Whisper. LifeVault aplica búsqueda semántica con embeddings sobre documentos del usuario: ingesta, troceado, vectores en PostgreSQL y recuperación. Alfred, mi sistema multi-agente en Python sobre la Claude API, integra LLMs con herramientas y memoria persistente y funciona 24/7 en un servidor Linux.",
  "Me atrae aplicar la IA a la atención de miles de alumnos en una institución que ofrece becas y plan de carrera. Para ser claro: no tengo los dos o tres años de experiencia que piden (en empresa son cuatro meses), no he entrenado ni ajustado modelos con PyTorch o TensorFlow y no he usado LangChain, Pinecone ni FAISS; mi fuerte es la integración de LLMs y RAG en producto.",
  "Puedo incorporarme de inmediato y trasladarme a Taco, Tenerife. Me encantaría enseñarles estos asistentes funcionando en una entrevista.",
 ],
},
# 4 ------------------------------------------------------------------
{
 "slug": "JTI-AINativeSoftwareEngineer", "lang": "en", "wm": True,
 "empresa": "JTI", "puesto_ref": "AI Native Software Engineer, Microsoft Delivery Center (Madrid)",
 "subtitulo": "AI Native Software Engineer · AI-first development with agentic tools",
 "perfil": "Software developer who works AI-first every day (Higher VET in Web Application Development, 2025; Master's in Generative AI and Innovation, 2026). I build and test with agentic coding tools (Claude Code with MCP, subagents and hooks), and I run my own multi-agent system on the Claude API in production. Full stack in TypeScript, React, Next.js and Python, with Git, pull requests, automated tests and CI/CD. Willing to work from Madrid. English B2 (Cambridge, 2025).",
 "skills": [
    ("AI-first engineering", ["Claude Code", "MCP", "Subagents and hooks", "AI-assisted testing", "Claude API", "OpenAI API", "Agentic AI"]),
    ("Software", ["TypeScript", "JavaScript", "React", "Next.js", "Python", "Node.js", "REST APIs", "PHP", "Laravel"]),
    ("DevOps", ["Git", "GitHub pull requests", "CI/CD (Vercel, Netlify)", "Vitest", "Linux"]),
    ("Data & cloud", ["PostgreSQL", "Supabase", "SQL", "AWS Academy (cloud foundations)"]),
 ],
 "bullets": ["laravel", "sync", "paneles", "proxmox"],
 "proyectos": ["alfred", "streakode", "lifevault", "elite"],
 "saludo": "Dear JTI team,",
 "parrafos": [
  "I am applying for the AI Native Software Engineer role at the Microsoft Delivery Center. You describe the role as an evolution of the software engineer for people who apply AI across the whole development lifecycle, and that is how I have learned to build software. I hold a Higher VET in Web Application Development (2025) and a Master's in Generative AI and Innovation (2026).",
  "I develop daily with Claude Code, using MCP servers, subagents and hooks to generate code, write tests and review changes, and I keep a log of the agent's mistakes so the workflow improves over time. That is how I built Streakode, a live Next.js and TypeScript PWA with automated tests and continuous deployment. Alfred, my multi-agent system on the Claude API, runs 24/7 in production. At the Agencia de Digitalización Andaluza I maintained a production system in Laravel and SQL.",
  "The change-champion side of the role appeals to me: knowing where AI-assisted development works and where it fails is exactly what I would like to help other engineers adopt. To be transparent: my experience in enterprise delivery is four months, I have used GitHub Copilot less than Claude Code, and I have not worked with Azure DevOps or GitHub SpecKit.",
  "I can start immediately in Madrid. I would be glad to show you this workflow live in an interview.",
 ],
},
]
