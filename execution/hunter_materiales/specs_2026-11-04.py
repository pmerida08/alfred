ES_IA = [
    ("IA generativa", ["Agentes y tool calling", "RAG", "Embeddings", "Prompt engineering", "MCP", "Claude API", "OpenAI API", "Gemini API", "Sistemas multiagente", "Whisper"]),
    ("Lenguajes & datos", ["Python", "SQL", "PostgreSQL", "MySQL", "TypeScript", "JavaScript", "PHP"]),
    ("Ingeniería", ["APIs REST", "JSON", "Git", "Pull requests en GitHub", "Linux", "Vitest (tests automáticos)", "CI/CD (Netlify)"]),
    ("Frameworks", ["n8n", "Supabase", "Next.js", "React", "Node.js", "Laravel"]),
]
EN_IA = [
    ("AI & agents", ["Claude API", "OpenAI API", "Gemini API", "Tool calling", "Structured outputs", "Agent memory", "Multi-agent flows", "MCP", "RAG", "Embeddings", "Whisper"]),
    ("Code", ["Python", "TypeScript", "JavaScript", "Node.js", "Next.js", "React", "PostgreSQL", "SQL", "Webhooks", "REST APIs"]),
    ("Shipping", ["Git", "GitHub pull requests", "Vitest (automated tests)", "CI/CD (Netlify, Vercel)", "Supabase", "Linux"]),
]

OFERTAS = [
# 1 ------------------------------------------------------------------
{
 "slug": "NTTDATA-AIDeveloper", "lang": "es", "wm": True,
 "empresa": "NTT DATA Europe & Latam", "puesto_ref": "AI Developer (Bilbao)",
 "subtitulo": "AI Developer · Agentes de IA, integración de LLMs y RAG en Python",
 "perfil": "Desarrollador (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que construye agentes de IA en Python: orquestación de agentes especializados, integración de LLMs (Claude, OpenAI, Gemini), diseño de prompts, tools y RAG con embeddings. Mantengo en producción un sistema multi-agente que genera documentos HTML a medida y he trabajado sobre código existente en producción. Disponible para incorporarme en Bilbao. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": ES_IA, "proyectos": ["alfred", "lifevault", "elite", "streakode"],
 "saludo": "Estimado equipo de NTT DATA:",
 "parrafos": [
  "Me presento al puesto de AI Developer para la plataforma de agentes que analiza código legacy y genera documentación y propuestas de arquitectura. Es el tipo de sistema que construyo: agentes especializados en Python sobre LLMs, con tools propias, control del contexto y salidas en Markdown y HTML. Salgo del Máster en IA Generativa e Innovación (2026), tras el CFGS en Desarrollo de Aplicaciones Web.",
  "Alfred, mi sistema multi-agente sobre la Claude API, orquesta agentes con memoria persistente y tool calling, integrados por API con Gmail, Notion, Google Sheets y Telegram, y genera documentos HTML a medida (este CV, por ejemplo). En LifeVault y Estudiante Élite implementé RAG con embeddings y memoria de sesión. En mis cuatro meses en la Agencia de Digitalización Andaluza trabajé sobre un sistema de gestión ya en producción (Laravel, JavaScript, SQL), lo que me obligó a leer y entender código ajeno antes de cambiarlo.",
  "Me atrae que el producto sea una herramienta para desarrolladores: optimizar el contexto, reducir tokens y diseñar prompts por caso de uso es justo lo que más he trabajado. Para ser transparente: no llego a los dos años de experiencia profesional que piden, mis agentes están construidos directamente sobre la API y no con LangChain, y mi Java es el de la formación.",
  "Puedo incorporarme de inmediato y trasladarme a Bilbao. Quedo a su disposición para una entrevista.",
 ],
},
# 2 ------------------------------------------------------------------
{
 "slug": "NTTDATA-JuniorFrontendDeveloperJS", "lang": "es", "wm": False,
 "empresa": "NTT DATA Europe & Latam", "puesto_ref": "Junior Frontend Developer (JavaScript) - Barcelona",
 "subtitulo": "Junior Frontend Developer · JavaScript, TypeScript y React",
 "perfil": "Desarrollador frontend junior (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) con JavaScript y TypeScript: interfaces en React y Next.js, consumo de APIs REST y mantenimiento de código existente. En la Agencia de Digitalización Andaluza mantuve y amplié un sistema de gestión en producción con JavaScript, Laravel y SQL, resolviendo peticiones de mejora e incidencias. Disponible para incorporarme en Barcelona. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Frontend", ["JavaScript", "TypeScript", "React", "Next.js", "HTML5", "CSS3", "Tailwind CSS", "Diseño responsive"]),
    ("Backend & datos", ["Node.js", "PHP", "Laravel", "APIs REST", "JSON", "SQL", "PostgreSQL", "MySQL", "Supabase"]),
    ("Ingeniería", ["Git", "Pull requests en GitHub", "Vitest (tests automáticos)", "CI/CD (Netlify, Vercel)", "Linux"]),
    ("IA", ["Claude API", "OpenAI API", "Gemini API", "RAG", "n8n"]),
 ],
 "bullets": ["laravel", "paneles", "sync", "proxmox"],
 "proyectos": ["streakode", "lifevault", "alfred", "elite"],
 "saludo": "Estimado equipo de NTT DATA:",
 "parrafos": [
  "Me presento al puesto de Junior Frontend Developer (JavaScript) en Barcelona. El trabajo que describen, mantener y hacer evolucionar el frontend de una web y resolver peticiones de mejora, es el que hice en mi primer empleo y el que hago a diario en mis proyectos. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "En la Agencia de Digitalización Andaluza mantuve un sistema de gestión en producción con JavaScript, Laravel y SQL: nuevas funciones, depuración y corrección de incidencias sobre código que no era mío, además de paneles con datos actualizados a diario. Fuera del trabajo mantengo Streakode, una PWA en producción con Next.js y TypeScript con tests automáticos, y LifeVault, con React Native y Supabase.",
  "Me atrae empezar en un equipo grande con proyectos estables y formación continua, y la flexibilidad entre oficina y teletrabajo que ofrecen. Mi experiencia profesional es corta (cuatro meses), así que valoro especialmente el acompañamiento de un equipo con más recorrido.",
  "Puedo incorporarme de inmediato y trasladarme a Barcelona. Quedo a su disposición para una entrevista.",
 ],
},
# 3 ------------------------------------------------------------------
{
 "slug": "Justnet-ProgramadorFullStack", "lang": "es", "wm": False,
 "empresa": "Justnet Systems", "puesto_ref": "Programador full stack (Barcelona, presencial)",
 "subtitulo": "Desarrollador Full-Stack · React, TypeScript, Node.js y APIs REST",
 "perfil": "Desarrollador full-stack (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) con React (hooks y componentes funcionales) y TypeScript en frontend y backend, APIs con Node.js y PHP/Laravel, y bases de datos PostgreSQL y MySQL. He trabajado sobre código existente en producción, añadiendo funciones y corrigiendo incidencias, y mantengo aplicaciones propias con tests automáticos y CI/CD. Disponible para trabajar presencial en Barcelona. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Frontend", ["React (hooks, componentes funcionales)", "TypeScript", "JavaScript", "Next.js", "React Native", "HTML5", "CSS3"]),
    ("Backend & APIs", ["Node.js", "APIs REST", "JSON", "PHP", "Laravel", "Supabase", "Webhooks"]),
    ("Datos", ["PostgreSQL", "MySQL", "SQL", "Diseño de esquemas", "RLS"]),
    ("Ingeniería", ["Git", "Pull requests en GitHub", "Vitest (tests automáticos)", "CI/CD (Netlify, Vercel)", "Linux"]),
 ],
 "bullets": ["laravel", "sync", "paneles", "proxmox"],
 "proyectos": ["streakode", "lifevault", "alfred", "elite"],
 "saludo": "Estimado equipo de Justnet Systems:",
 "parrafos": [
  "Me presento al puesto de Programador full stack. Buscan React con hooks, TypeScript en frontend y backend, APIs con Node.js y capacidad para trabajar sobre código existente: es mi stack diario. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Streakode es una PWA en producción con Next.js y TypeScript sobre Supabase (PostgreSQL con RLS y pg_cron), con tests automáticos y notificaciones por push y email. En LifeVault construí la app con React Native y TypeScript y su backend en Supabase. En la Agencia de Digitalización Andaluza mantuve un sistema de gestión en producción con Laravel, JavaScript y SQL: nuevas funciones y corrección de incidencias en código heredado.",
  "Me atrae que sean proyectos estables, sin body-shopping, y con participación real en las decisiones técnicas. Para ser claro: mi experiencia profesional son cuatro meses, por debajo del año que piden; lo compenso con aplicaciones propias en producción que puedo enseñar y explicar línea a línea.",
  "Puedo incorporarme de inmediato y trasladarme a Barcelona para trabajar presencial. Quedo a su disposición para una entrevista.",
 ],
},
# 4 ------------------------------------------------------------------
{
 "slug": "Libeen-AIProductEngineer", "lang": "es", "wm": True,
 "empresa": "Libeen", "puesto_ref": "AI Product Engineer (Madrid)",
 "subtitulo": "AI Product Engineer · Producto full-stack construido con agentes de código",
 "perfil": "Desarrollador full-stack (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que construye producto con agentes de código como herramienta principal. Trabajo a diario con Claude Code y mantengo su harness: instrucciones, skills, subagentes, hooks, MCP y comprobaciones. Llevo a producción apps con TypeScript, React y PostgreSQL (Supabase), con tests y CI/CD. Disponible para incorporarme en Madrid. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Agentes & harness", ["Claude Code", "Skills", "Subagentes", "Hooks", "MCP", "Tool calling", "Memoria", "Claude API", "OpenAI API", "RAG", "n8n"]),
    ("Full-stack", ["TypeScript", "React", "Next.js", "Node.js", "Python", "APIs REST", "Webhooks", "PostgreSQL", "Supabase (RLS, pg_cron)"]),
    ("Calidad & despliegue", ["Vitest (tests automáticos)", "Git", "Pull requests en GitHub", "CI/CD (Netlify, Vercel)", "Linux"]),
 ],
 "proyectos": ["alfred", "streakode", "lifevault", "elite"],
 "proy_desc": {"alfred": "Agente personal sobre Claude Code y la Claude API, 24/7 en un servidor Linux y por Telegram: agentes con memoria persistente, tool calling, skills, subagentes y hooks, integrados con Gmail, Notion y Google Sheets. Genera candidaturas a medida, como esta."},
 "saludo": "Estimado equipo de Libeen:",
 "parrafos": [
  "Me presento al puesto de AI Product Engineer. Describen a alguien que define bien el problema, dirige a agentes de código y monta el harness que hace fiable el resultado: es exactamente como trabajo desde hace un año. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Alfred, mi agente personal, funciona sobre Claude Code y la Claude API: instrucciones de proyecto, skills, subagentes, hooks y servidores MCP, con un registro de errores que convierto en reglas para que no se repitan. Conversa conmigo por Telegram 24/7 y actúa sobre Gmail, Notion y Google Sheets. Con ese mismo flujo construí Streakode, una PWA en producción con Next.js, TypeScript y Supabase (RLS, pg_cron), tests automáticos y notificaciones por push y email.",
  "Me atrae construir desde cero el agente que acompaña a cada cliente por WhatsApp y automatizar procesos de ventas, finanzas y legal en un equipo pequeño que reporta al CPTO. Para ser transparente: mi experiencia profesional son cuatro meses en una agencia, no he trabajado en fintech ni proptech y mis evaluaciones de agentes aún son informales.",
  "Puedo incorporarme de inmediato y trasladarme a Madrid. Les enseño Alfred funcionando cuando quieran.",
 ],
},
# 5 ------------------------------------------------------------------
{
 "slug": "Bluetab-PythonAIEngineer", "lang": "es", "wm": True,
 "empresa": "Bluetab, an IBM Company", "puesto_ref": "Python + AI Engineer (Agentic AI)",
 "subtitulo": "Python + AI Engineer · Agentes de IA, prompt engineering y RAG",
 "perfil": "Desarrollador (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que desarrolla agentes de IA en Python: prompts integrados por código, tool calling, sistemas multiagente y RAG con embeddings, sobre APIs REST. Mantengo en producción un sistema multi-agente sobre la Claude API en un servidor Linux 24/7 y trabajo con Git, pull requests y tests automáticos. Disponible para Madrid o cualquiera de sus hubs. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": ES_IA, "proyectos": ["alfred", "lifevault", "elite", "streakode"],
 "saludo": "Estimado equipo de Bluetab:",
 "parrafos": [
  "Me presento a la oferta de Agentic AI Engineer (Python + AI Engineer). Piden prompt engineering integrado por código, arquitecturas de agentes, Python backend, Git con pull requests y testing automatizado; es el trabajo que hago a diario. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Alfred es mi sistema multi-agente en Python sobre la Claude API: agentes especializados con memoria persistente, tool calling e integraciones por API con Gmail, Notion, Google Sheets y Telegram, desplegado 24/7 en un servidor Linux. En LifeVault y Estudiante Élite implementé RAG con embeddings y memoria de sesión. Trabajo con agentes de código y los dirijo con instrucciones, skills y comprobaciones, lo que encaja con su idea de automatizar el ciclo de desarrollo.",
  "Me atrae que la IA generativa se aplique a cómo se desarrolla el software, y el teletrabajo flexible con hubs. Para ser transparente: mis agentes están construidos directamente sobre la API y no con OpenAI Agents SDK, no he usado Bedrock ni SageMaker, y mi experiencia profesional son cuatro meses en una agencia.",
  "Puedo incorporarme de inmediato. Quedo a su disposición para una entrevista.",
 ],
},
# 6 ------------------------------------------------------------------
{
 "slug": "Devoteam-AIEngineer", "lang": "es", "wm": True,
 "empresa": "Devoteam", "puesto_ref": "AI Engineer Mid-Level (100 % remoto)",
 "subtitulo": "AI Engineer · Agentes, RAG y evaluación de soluciones de IA generativa",
 "perfil": "Desarrollador (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que construye soluciones de IA generativa en Python: agentes con tool calling, RAG con embeddings y búsqueda semántica, integración de APIs y fuentes de datos, y pruebas automatizadas. Mantengo en producción un sistema multi-agente sobre la Claude API 24/7 y apps con React, TypeScript y CI/CD. Trabajo en remoto desde Montilla (Córdoba). Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": ES_IA, "proyectos": ["alfred", "lifevault", "elite", "streakode"],
 "saludo": "Estimado equipo de Devoteam:",
 "parrafos": [
  "Me presento al puesto de AI Engineer en su equipo de IA generativa. Piden agentes, RAG con chunking y embeddings, integración de APIs y fuentes de datos, pruebas automatizadas y frontend con React para demos; son las piezas con las que trabajo. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Alfred es mi sistema multi-agente en Python sobre la Claude API, con memoria persistente, tool calling e integraciones con Gmail, Notion, Google Sheets y Telegram, 24/7 en un servidor Linux. En LifeVault construí búsqueda semántica con embeddings y un chatbot con contexto persistente, y en Estudiante Élite un RAG sobre el temario con transcripción de audio. Streakode, mi PWA con Next.js y Supabase, tiene tests automáticos y despliegue continuo.",
  "Me atrae la parte de evaluación con baterías de preguntas y pruebas de regresión, que es lo que más quiero profesionalizar. Para ser transparente: no llego a los dos años de experiencia que piden (son cuatro meses en una agencia más proyectos propios), no he trabajado con Azure AI Search ni Microsoft Foundry y mis evaluaciones aún son informales.",
  "Puedo incorporarme de inmediato en remoto. Quedo a su disposición para una entrevista.",
 ],
},
# 7 ------------------------------------------------------------------
{
 "slug": "Okify-FullStackSoftwareDeveloper", "lang": "en", "wm": False,
 "empresa": "Okify", "puesto_ref": "Full-stack Software Developer (Barcelona, hybrid)",
 "subtitulo": "Full-stack Software Developer · Python, JavaScript, REST integrations",
 "perfil": "Full-stack developer (Higher Technical Diploma in Web Application Development, 2025; Master's in Generative AI & Innovation, 2026) working with Python and JavaScript/TypeScript: REST API integrations, webhooks, automation flows and client-facing apps in React. I run in production a Python multi-agent system that integrates Gmail, Notion, Google Sheets and Telegram, and ship apps with automated tests and CI/CD. Willing to relocate to Barcelona. Native Spanish, B2 English (Cambridge, 2025).",
 "skills": [
    ("Code", ["Python", "JavaScript", "TypeScript", "HTML5", "CSS3", "React", "Next.js", "Node.js", "PHP", "Laravel"]),
    ("Integrations", ["REST APIs", "Webhooks", "JSON", "n8n", "Data validation", "Gmail / Notion / Google Sheets / Telegram APIs"]),
    ("Data & shipping", ["PostgreSQL", "MySQL", "SQL", "Supabase", "Git", "GitHub pull requests", "Vitest (automated tests)", "CI/CD (Netlify, Vercel)", "Linux"]),
    ("AI", ["Claude API", "OpenAI API", "Gemini API", "RAG"]),
 ],
 "proyectos": ["alfred", "streakode", "lifevault", "elite"],
 "saludo": "Hi Okify team,",
 "parrafos": [
  "I am applying for the Full-stack Software Developer role. You need someone who builds reliable integrations and automation tools in Python and JavaScript, works with REST APIs and webhooks and is comfortable with Git and the command line. That is my daily work. I hold a Higher Technical Diploma in Web Application Development (2025) and a Master's in Generative AI & Innovation (2026).",
  "Alfred, my Python system on the Claude API, integrates Gmail, Notion, Google Sheets and Telegram through their APIs and runs 24/7 on my Linux server, so I deal with failing third-party calls and data validation every week. At the Agencia de Digitalización Andaluza I built automated synchronisation flows between internal systems and maintained a production management system in Laravel, JavaScript and SQL. Streakode, my live PWA on Next.js and Supabase, has automated tests and CI/CD.",
  "What attracts me is the end-to-end ownership in a small team: integrations with utility providers are exactly the kind of messy real-world plumbing I enjoy. To be upfront: I do not hold a university degree in Computer Science (my training is the technical diploma plus the master's), my professional experience is a four-month contract, and I have not used Django or Celery.",
  "I can start immediately and relocate to Barcelona for the hybrid setup. Happy to walk you through my code.",
 ],
},
# 8 ------------------------------------------------------------------
{
 "slug": "InnoIT-AIEngineerPythonAgenticAI", "lang": "en", "wm": True,
 "empresa": "InnoIT Consulting", "puesto_ref": "AI Engineer — Python & Agentic AI (Madrid, hybrid)",
 "subtitulo": "AI Engineer · Python agents, tool calling and enterprise integrations",
 "perfil": "Developer (Higher Technical Diploma in Web Application Development, 2025; Master's in Generative AI & Innovation, 2026) who builds applied AI in Python: agents with tool calling and structured outputs, LLMs combined with deterministic rules, REST integrations with authentication, SQL and automated tests. I run in production a multi-agent system on the Claude API that works on Gmail, Notion and Google Sheets, 24/7 on a Linux server. Willing to relocate to Madrid. Native Spanish, B2 English (Cambridge, 2025).",
 "skills": EN_IA, "proyectos": ["alfred", "lifevault", "elite", "streakode"],
 "saludo": "Hi InnoIT team,",
 "parrafos": [
  "I am applying for the AI Engineer — Python & Agentic AI role. You describe a software engineering and integration job with a strong applied AI component: agents in Python, enterprise integrations, LLMs combined with deterministic logic and human-in-the-loop for sensitive decisions. That is how I build. I hold a Master's in Generative AI & Innovation (2026) after a Higher Technical Diploma in Web Application Development.",
  "Alfred, my multi-agent system on the Claude API, uses tool calling and persistent memory to act on Gmail, Notion and Google Sheets, and it asks me for approval before anything irreversible, such as sending an email. Hard rules sit next to the model: identifiers are only written when copied from a real tool response, and checks run before results are trusted. In LifeVault and Estudiante Élite I built RAG with embeddings over user documents.",
  "What attracts me is working on real business processes such as supplier invoices and legal document review, close to the people who use the tools. To be upfront: I have not used Gemini ADK, Microsoft Graph or BigQuery yet, my evaluations are still informal, and my professional experience is a four-month agency contract.",
  "I can start immediately and relocate to Madrid. Happy to show you Alfred running.",
 ],
},
# 9 ------------------------------------------------------------------
{
 "slug": "Collective-AIEngineer", "lang": "es", "wm": True,
 "empresa": "Collective.work", "puesto_ref": "AI Engineer (Madrid)",
 "subtitulo": "AI Engineer · Agentes con LLMs, React, Node.js y TypeScript",
 "perfil": "Desarrollador (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que construye agentes de IA con LLMs y producto end-to-end con React, Node.js y TypeScript: integración de las APIs de Anthropic, OpenAI y Gemini, RAG, búsqueda semántica y workflows de automatización. Mantengo en producción un sistema multi-agente que automatiza mi propia búsqueda de empleo: lee ofertas, puntúa el encaje y prepara candidaturas. Disponible para incorporarme en Madrid. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("IA generativa", ["Agentes con LLMs", "Tool calling", "RAG", "Embeddings y búsqueda semántica", "Claude API (Anthropic)", "OpenAI API", "Gemini API", "MCP", "n8n"]),
    ("Producto", ["TypeScript", "React", "Next.js", "Node.js", "Python", "APIs REST", "Webhooks"]),
    ("Datos & despliegue", ["PostgreSQL", "Supabase", "SQL", "Git", "Pull requests en GitHub", "Vitest (tests automáticos)", "CI/CD (Netlify, Vercel)", "Linux"]),
 ],
 "proyectos": ["alfred", "lifevault", "streakode", "elite"],
 "saludo": "Estimado equipo de Collective:",
 "parrafos": [
  "Me presento al puesto de AI Engineer. Buscan a alguien que diseñe agentes con LLMs, construya funcionalidades end-to-end con React, Node.js y TypeScript e integre las APIs de OpenAI y Anthropic; es mi stack. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Tengo un caso muy cercano a su producto: Alfred, mi sistema multi-agente sobre la Claude API, automatiza mi búsqueda de empleo. Consulta portales, filtra duplicados, puntúa el encaje de cada oferta con mi perfil, genera CV y carta a medida y registra cada candidatura en Notion; esta misma carta sale de ahí. En LifeVault construí búsqueda semántica con embeddings y un chatbot con contexto persistente, y Streakode es una PWA en producción con Next.js, TypeScript y Supabase.",
  "Me atrae trabajar en sourcing y reclutamiento con IA desde el otro lado de la mesa, y llevar ideas a producción rápido con el equipo de producto. Para ser transparente: mi experiencia profesional son cuatro meses en una agencia y mis evaluaciones de agentes todavía son informales.",
  "Puedo incorporarme de inmediato y trasladarme a Madrid. Les enseño el flujo funcionando cuando quieran.",
 ],
},
# 10 -----------------------------------------------------------------
{
 "slug": "HappyRobot-ForwardDeployedEngineer", "lang": "en", "wm": False,
 "empresa": "HappyRobot", "puesto_ref": "Forward Deployed Engineer (A Coruña)",
 "subtitulo": "Forward Deployed Engineer · React, TypeScript, Node.js, Python and LLM apps",
 "perfil": "Full-stack developer (Higher Technical Diploma in Web Application Development, 2025; Master's in Generative AI & Innovation, 2026) who builds LLM applications end to end: React, TypeScript, Node.js and Python, prompting, tool calling, speech transcription with Whisper and third-party API integrations. I run in production a multi-agent system on the Claude API, 24/7 on a Linux server, and ship apps with automated tests and CI/CD. Willing to relocate to A Coruña. Native Spanish, B2 English (Cambridge, 2025).",
 "skills": [
    ("Full-stack", ["React", "TypeScript", "Node.js", "Python", "Next.js", "REST APIs", "Webhooks", "PostgreSQL", "Supabase"]),
    ("AI", ["LLM prompting", "Tool calling", "Agent memory", "Multi-agent flows", "Whisper (transcription)", "RAG", "Claude API", "OpenAI API", "Gemini API", "MCP"]),
    ("Shipping", ["Git", "GitHub pull requests", "Vitest (automated tests)", "CI/CD (Netlify, Vercel)", "Linux", "n8n"]),
 ],
 "proyectos": ["alfred", "elite", "streakode", "lifevault"],
 "saludo": "Hi HappyRobot team,",
 "parrafos": [
  "I am applying for the Forward Deployed Engineer role in A Coruña. You need someone who combines full-stack work in React, TypeScript, Node.js and Python with LLM applications and direct contact with customers. I hold a Higher Technical Diploma in Web Application Development (2025) and a Master's in Generative AI & Innovation (2026).",
  "Alfred, my multi-agent system on the Claude API, runs 24/7 on a Linux server and acts on Gmail, Notion, Google Sheets and Telegram, so I have tuned prompts and tool calls against real failures, not demos. In Estudiante Élite I built a tutoring assistant with RAG and audio transcription with Whisper for law students, and Streakode is a live PWA on Next.js and TypeScript with automated tests. At the Agencia de Digitalización Andaluza I built API synchronisation flows for internal teams.",
  "What attracts me is turning a platform into working solutions for each customer, in a team of builders without seniority labels. To be upfront: I have not built voice agents or tuned voices, my professional experience is a four-month contract, and my customer-facing work so far has been with internal users.",
  "I can start immediately and relocate to A Coruña. Happy to show you Alfred running.",
 ],
},
# 11 -----------------------------------------------------------------
{
 "slug": "LABHOUSE-AIEngineerToolsAutomations", "lang": "en", "wm": True,
 "empresa": "LABHOUSE", "puesto_ref": "AI Engineer Tools & Automations (Barcelona)",
 "subtitulo": "AI Engineer · Internal AI tools, agents and automations in Python",
 "perfil": "Developer (Higher Technical Diploma in Web Application Development, 2025; Master's in Generative AI & Innovation, 2026) who spots manual work and replaces it with AI tools: agents with tool calling, RAG, Python integrations with APIs and webhooks, and n8n workflows. I built and run in production a multi-agent system on the Claude API that automates my own email, job search, nutrition log and project tracking, 24/7 on a Linux server. Willing to relocate to Barcelona. Native Spanish, B2 English (Cambridge, 2025).",
 "skills": [
    ("AI & agents", ["Claude API", "OpenAI API", "Gemini API", "Prompting", "Tool calling", "Agent memory", "Multi-agent flows", "MCP", "RAG", "Embeddings"]),
    ("Automation", ["n8n", "Make", "Webhooks", "REST APIs", "Gmail / Notion / Google Sheets / Telegram APIs", "Dashboards and reporting"]),
    ("Code & shipping", ["Python", "TypeScript", "JavaScript", "React", "Next.js", "PostgreSQL", "Supabase", "Git", "Vitest", "CI/CD", "Linux"]),
 ],
 "bullets": ["sync", "paneles", "laravel", "proxmox"],
 "proyectos": ["alfred", "elite", "lifevault", "streakode"],
 "saludo": "Hi LABHOUSE team,",
 "parrafos": [
  "I am applying for the AI Engineer Tools & Automations role. You want someone who walks in, finds where AI can remove manual work and builds the tool end to end. That is what I did for myself: I hold a Master's in Generative AI & Innovation (2026) after a Higher Technical Diploma in Web Application Development, and I built my own AI workforce.",
  "Alfred is a multi-agent system on the Claude API, running 24/7 on a Linux server: specialised agents with persistent memory and tool calling that sort my inbox, track my projects, log meals from a photo into Google Sheets and run my job search, from finding offers to generating this application. In Estudiante Élite I built n8n workflows with RAG and Whisper. At the Agencia de Digitalización Andaluza I automated data ingestion for daily dashboards and API sync flows between internal systems.",
  "What attracts me is building tools that a fast company uses every day, with clear impact on productivity. To be upfront: my LLM work in production is my own system rather than a company's, I have not built tools on paid acquisition data, and my professional experience is a four-month contract.",
  "I can start immediately and relocate to Barcelona. Happy to show you Alfred running.",
 ],
},
# 12 -----------------------------------------------------------------
{
 "slug": "Expleo-JuniorDataPythonEngineer", "lang": "es", "wm": False,
 "empresa": "Expleo Group", "puesto_ref": "Junior Data & Python Engineer | Sector Espacio / EGNOS (Madrid)",
 "subtitulo": "Junior Data & Python Engineer · Scripts, extracción y tratamiento de datos",
 "perfil": "Desarrollador junior (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que escribe scripts en Python para extraer, limpiar y cargar datos de webs y APIs, con SQL (PostgreSQL, MySQL) y documentación técnica. En la Agencia de Digitalización Andaluza automaticé la ingesta y el reporte de datos para paneles diarios. Disponible para incorporarme en Madrid. Español nativo, inglés B2 (Cambridge, 2025), con el que documento y leo documentación técnica a diario.",
 "skills": [
    ("Python & datos", ["Python", "Scripts de extracción y web scraping", "SQL", "PostgreSQL", "MySQL", "Supabase", "JSON", "APIs REST"]),
    ("Automatización", ["Ingesta y reporte automatizados", "n8n", "Linux", "Tareas programadas"]),
    ("Ingeniería", ["Git", "Pull requests en GitHub", "Vitest (tests automáticos)", "CI/CD (Netlify)", "Documentación técnica en inglés"]),
    ("Otros", ["TypeScript", "JavaScript", "React", "PHP", "Laravel", "Claude API", "OpenAI API"]),
 ],
 "bullets": ["paneles", "sync", "laravel", "proxmox"],
 "proyectos": ["alfred", "lifevault", "streakode", "elite"],
 "proy_desc": {"alfred": "Sistema multi-agente en Python, 24/7 en un servidor Linux: scripts de extracción de ofertas de empleo desde webs y APIs, deduplicado y registro en Notion y Google Sheets, con integraciones por API (Gmail, Notion, Google Sheets, Telegram) sobre la Claude API."},
 "saludo": "Estimado equipo de Expleo:",
 "parrafos": [
  "Me presento al puesto de Junior Data & Python Engineer para el proyecto de EGNOS. Piden scripts en Python, web scraping, tratamiento de datos y documentación técnica en inglés, con un nivel de experiencia inicial; es justo mi punto de partida. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "En la Agencia de Digitalización Andaluza automaticé la ingesta y el reporte de datos para paneles que se actualizaban a diario, y construí flujos de sincronización entre sistemas por API. En Alfred, mi sistema en Python sobre un servidor Linux, escribo scripts que extraen ofertas de empleo de varias webs y APIs, eliminan duplicados y registran los resultados en Notion y Google Sheets. Trabajo con SQL en PostgreSQL y MySQL.",
  "Me atrae aplicar Python a datos reales de un programa europeo de navegación por satélite y aprender el dominio. Para ser transparente: no he trabajado con datos de Copernicus, ArcGIS, Power BI ni GNSS, y mi experiencia profesional son cuatro meses; tengo inglés B2 (Cambridge, 2025).",
  "Puedo incorporarme de inmediato y trasladarme a Madrid. Quedo a su disposición para una entrevista.",
 ],
},
]
