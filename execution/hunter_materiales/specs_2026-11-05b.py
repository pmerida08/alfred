FECHA_ES = "Montilla, 5 de noviembre de 2026"
FECHA_EN = "Montilla, Córdoba (Spain) · 5 November 2026"

ES_IA = [
    ("IA generativa", ["Agentes y tool calling", "RAG", "Embeddings", "Prompt engineering", "MCP", "Claude API", "OpenAI API", "Gemini API", "Sistemas multiagente", "Whisper"]),
    ("Lenguajes & datos", ["Python", "SQL", "PostgreSQL", "MySQL", "TypeScript", "JavaScript", "PHP"]),
    ("Ingeniería", ["APIs REST", "JSON", "Git", "Pull requests en GitHub", "Linux", "Vitest (tests automáticos)", "CI/CD (Netlify)"]),
    ("Frameworks", ["n8n", "Supabase", "Next.js", "React", "Node.js", "Laravel"]),
]
ES_FULL = [
    ("Frontend", ["React", "TypeScript", "JavaScript", "Next.js", "React Native", "HTML5", "CSS3"]),
    ("Backend & APIs", ["Python", "Node.js", "APIs REST", "JSON", "PHP", "Laravel", "Supabase", "Webhooks"]),
    ("Datos", ["PostgreSQL", "MySQL", "SQL", "Diseño de esquemas", "RLS"]),
    ("Ingeniería", ["Git", "Pull requests en GitHub", "Vitest (tests automáticos)", "CI/CD (Netlify, Vercel)", "Linux"]),
    ("IA", ["Claude API", "OpenAI API", "RAG", "Agentes y tool calling", "n8n"]),
]

OFERTAS = [
# 1 ------------------------------------------------------------------
{
 "slug": "Capgemini-JuniorAIGenerativeAIEngineer", "lang": "es", "wm": True,
 "empresa": "Capgemini", "puesto_ref": "Junior AI & Generative AI Engineer (Madrid)",
 "subtitulo": "Junior AI & Generative AI Engineer · LLMs, RAG y agentes en Python",
 "perfil": "Desarrollador de IA junior (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que construye soluciones GenAI en Python: integración de LLMs (Claude, OpenAI, Gemini), RAG con embeddings, agentes con tool calling y asistentes conversacionales con memoria. Mantengo en producción un sistema multi-agente 24/7 en Linux y he trabajado sobre código existente en producción. Disponible para incorporarme en Madrid. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": ES_IA, "proyectos": ["alfred", "lifevault", "elite", "streakode"],
 "saludo": "Estimado equipo de Capgemini:",
 "parrafos": [
  "Me presento al puesto de Junior AI & Generative AI Engineer en Madrid. Buscan a alguien con experiencia práctica en soluciones de IA generativa, asistentes virtuales y RAG, y eso es lo que he construido en el último año. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Alfred, mi sistema multi-agente en Python sobre la Claude API, funciona 24/7 en un servidor Linux: agentes con memoria persistente, tool calling e integraciones con Gmail, Notion, Google Sheets y Telegram. En LifeVault y Estudiante Élite implementé RAG con embeddings, chatbots con contexto persistente y transcripción con Whisper. En la Agencia de Digitalización Andaluza trabajé sobre un sistema de gestión en producción con Laravel, JavaScript y SQL.",
  "Para ser transparente: mi experiencia profesional son cuatro meses, por debajo del año que piden, y no he desplegado en Azure ni usado frameworks de evaluación de LLMs en un entorno corporativo. Lo compenso con proyectos en producción que puedo enseñar y con ganas de aprovechar la formación y certificaciones que ofrecen.",
  "Puedo incorporarme de inmediato y trasladarme a Madrid. Quedo a su disposición para una entrevista.",
 ],
},
# 2 ------------------------------------------------------------------
{
 "slug": "Confidencial-TecnicoJuniorIADesarrolloSoporteIT", "lang": "es", "wm": True,
 "empresa": "Grupo empresarial (oferta confidencial)", "puesto_ref": "Técnico/a Junior de Inteligencia Artificial, Desarrollo y Soporte IT (Madrid)",
 "subtitulo": "Técnico Junior de IA y Desarrollo · Automatización, aplicaciones internas y soporte IT",
 "perfil": "Técnico junior de IA y desarrollo (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que construye aplicaciones internas y automatizaciones con IA: JavaScript, TypeScript, Python, APIs, bases de datos y flujos con n8n y Make. En la Agencia de Digitalización Andaluza mantuve un sistema de gestión en producción y lideré la migración a máquinas virtuales Linux en Proxmox. Disponible en Madrid. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("IA y automatización", ["Claude API", "OpenAI API", "Gemini API", "Agentes y tool calling", "RAG", "n8n", "Make", "Asistentes de programación con IA"]),
    ("Desarrollo", ["JavaScript", "TypeScript", "Python", "React", "Next.js", "PHP", "Laravel", "APIs REST"]),
    ("Datos", ["SQL", "PostgreSQL", "MySQL", "Supabase"]),
    ("Sistemas", ["Linux", "Proxmox (máquinas virtuales)", "Git", "Google Workspace", "Microsoft 365 (usuario)"]),
 ],
 "bullets": ["laravel", "proxmox", "sync", "paneles"],
 "proyectos": ["alfred", "lifevault", "streakode", "elite"],
 "saludo": "Estimado equipo de selección:",
 "parrafos": [
  "Me presento al puesto de Técnico/a Junior de Inteligencia Artificial, Desarrollo y Soporte IT. Combinar el desarrollo de herramientas internas con IA y el soporte a usuarios es justo el perfil mixto que tengo: CFGS en Desarrollo de Aplicaciones Web (2025), Máster en IA Generativa e Innovación (2026) y un primer empleo en el que hice de las dos cosas.",
  "En la Agencia de Digitalización Andaluza mantuve un sistema de gestión en producción con Laravel, JavaScript y SQL, monté flujos de sincronización entre sistemas internos y lideré la migración a máquinas virtuales Linux en Proxmox. Por mi cuenta mantengo Alfred, un sistema de agentes de IA que automatiza correo, calendario y documentos con integraciones por API, y aplicaciones web con TypeScript, Supabase y n8n.",
  "Para ser claro: no he usado Lovable en un proyecto, aunque desarrollo a diario con asistentes de IA y construyo las mismas aplicaciones con código propio, y mi experiencia con Microsoft Entra ID y Business Central es nula. Aprendo rápido este tipo de herramientas.",
  "Puedo incorporarme de inmediato y trasladarme a Madrid. Quedo a su disposición para una entrevista.",
 ],
},
# 3 ------------------------------------------------------------------
{
 "slug": "Prodware-AIEngineer", "lang": "es", "wm": True,
 "empresa": "Prodware España", "puesto_ref": "AI Engineer",
 "subtitulo": "AI Engineer · Agentes, tools y RAG sobre LLMs en Python",
 "perfil": "Desarrollador de IA (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que construye agentes en Python sobre LLMs (Claude, GPT, Gemini): tools y skills propias, integración con APIs y sistemas externos, RAG con embeddings y búsqueda semántica. Mantengo en producción un sistema multi-agente 24/7 conectado a Gmail, Notion, Google Sheets y Telegram, con servidores MCP. Disponible en remoto o presencial. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": ES_IA, "proyectos": ["alfred", "lifevault", "elite", "streakode"],
 "saludo": "Estimado equipo de Prodware:",
 "parrafos": [
  "Me presento al puesto de AI Engineer. Construir agentes, crear skills, tools y plugins propios e integrarlos con sistemas corporativos y fuentes de datos es lo que hago a diario. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Alfred, mi sistema multi-agente en Python sobre la Claude API, funciona 24/7 en un servidor Linux con agentes especializados, memoria persistente, skills propias y servidores MCP que lo conectan con Gmail, Notion, Google Sheets y Telegram. En LifeVault y Estudiante Élite diseñé RAG con embeddings y búsqueda semántica sobre documentos del usuario. En la Agencia de Digitalización Andaluza integré sistemas internos por API.",
  "Para ser transparente: no he trabajado con Azure AI Foundry ni con Amazon Bedrock, mis agentes van directamente sobre las APIs de los modelos, y mi experiencia profesional es de cuatro meses. Me atrae precisamente entrar en el ecosistema Microsoft con la formación continua que ofrecen.",
  "Puedo incorporarme de inmediato. Quedo a su disposición para una entrevista y para enseñarles Alfred funcionando.",
 ],
},
# 4 ------------------------------------------------------------------
{
 "slug": "Marlex-ProgramadorIA", "lang": "es", "wm": True,
 "empresa": "Paul Marlex (para empresa industrial cliente)", "puesto_ref": "Programador/a IA y Aplicaciones Transversales (Sant Jaume de Llierca)",
 "subtitulo": "Programador de IA y aplicaciones internas · Python, TypeScript, SQL y APIs",
 "perfil": "Programador (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que desarrolla aplicaciones internas y automatizaciones con IA: Python, JavaScript/TypeScript, React, SQL, APIs REST y Git. He mantenido un sistema de gestión en producción, desplegado servidores Linux y máquinas virtuales en Proxmox, y llevo un sistema de agentes de IA 24/7. Disponible para trasladarme y trabajar presencial. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Desarrollo", ["Python", "TypeScript", "JavaScript", "React", "Next.js", "PHP", "Laravel", "APIs REST", "Git"]),
    ("Datos y servidores", ["SQL", "PostgreSQL", "MySQL", "Supabase", "Linux", "Proxmox"]),
    ("IA", ["Claude API", "OpenAI API", "Gemini API", "Agentes y tool calling", "RAG", "Asistentes de programación con IA", "n8n"]),
 ],
 "bullets": ["laravel", "sync", "proxmox", "paneles"],
 "proyectos": ["alfred", "lifevault", "streakode", "elite"],
 "saludo": "Estimado equipo de Marlex:",
 "parrafos": [
  "Me presento al puesto de Programador/a de Inteligencia Artificial y Aplicaciones Transversales. Unificar y mejorar las aplicaciones internas, automatizar procesos como la generación de ofertas y llevar la IA a los departamentos es el tipo de trabajo que hago. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "En la Agencia de Digitalización Andaluza mantuve un sistema de gestión en producción con Laravel, JavaScript y SQL, monté flujos de sincronización entre sistemas internos y lideré la migración de servidores a máquinas virtuales Linux en Proxmox. Mi proyecto Alfred es un sistema de agentes de IA que genera documentos a medida (este CV, por ejemplo) e integra correo, Notion y hojas de cálculo por API.",
  "Para ser claro: no he integrado SAP, CRM ni Autodesk Inventor, y mi experiencia profesional son cuatro meses; liderar la estrategia de IA sería un reto que asumiría con ganas y con autonomía, empezando por los procesos con más trabajo manual.",
  "Puedo incorporarme de inmediato y trasladarme a la Garrotxa para trabajar presencial. Quedo a su disposición para una entrevista.",
 ],
},
# 5 ------------------------------------------------------------------
{
 "slug": "OneSpan-AIAutomationEngineer", "lang": "en", "wm": True,
 "empresa": "OneSpan", "puesto_ref": "AI Automation Engineer (Barcelona)",
 "subtitulo": "AI Automation Engineer · Agents on the Claude API, scripting and CI/CD",
 "perfil": "Developer (Higher Technical Diploma in Web Application Development, 2025; Master's in Generative AI & Innovation, 2026) who automates real work with agents and plain scripts: I run in production a multi-agent system on the Claude API, 24/7 on a Linux server, with tool calling, persistent memory, MCP servers and API integrations. Comfortable across Python, TypeScript, Node.js, Git, automated tests and CI/CD. Willing to relocate to Barcelona. Native Spanish, B2 English (Cambridge, 2025).",
 "skills": [
    ("AI & agents", ["Claude API", "Claude Code", "Tool calling", "MCP", "Agent memory", "Multi-agent flows", "RAG", "Embeddings", "OpenAI API"]),
    ("Code & scripting", ["Python", "TypeScript", "JavaScript", "Node.js", "Bash", "SQL", "REST APIs", "Webhooks"]),
    ("Shipping", ["Git", "GitHub pull requests", "Vitest (automated tests)", "CI/CD (Netlify, Vercel)", "Linux", "n8n"]),
 ],
 "proyectos": ["alfred", "streakode", "lifevault", "elite"],
 "saludo": "Hi OneSpan team,",
 "parrafos": [
  "I am applying for the AI Automation Engineer role in Barcelona. Finding the repetitive work inside a team and removing it, with an agent where judgement is needed and a script where that is simply more reliable, is how I already work. I hold a Higher Technical Diploma in Web Application Development (2025) and a Master's in Generative AI & Innovation (2026).",
  "Alfred, my multi-agent system on the Claude API, runs 24/7 on a Linux server and takes over my own email triage, calendar, job applications and document generation through Gmail, Notion, Google Sheets and Telegram. Building it taught me where agents fail and where a deterministic script is the better answer: half of it is plain Python. Streakode, a live PWA, ships with automated tests and CI/CD, and at the Agencia de Digitalización Andaluza I replaced manual data handling with API synchronisation flows.",
  "To be upfront: my professional experience is a four-month contract, I have not worked inside a large R&D organisation and my English is B2, not native. I can show you everything I mention running.",
  "I can start immediately and relocate to Barcelona. I would welcome the chance to talk.",
 ],
},
# 6 ------------------------------------------------------------------
{
 "slug": "ALTEN-DesarrolladorFullStackGetafe", "lang": "es", "wm": False,
 "empresa": "ALTEN Spain", "puesto_ref": "Desarrollador/a Full Stack (Getafe)",
 "subtitulo": "Desarrollador Full-Stack · React, Python y automatización de procesos",
 "perfil": "Desarrollador full-stack (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) con React y TypeScript en frontend y Python, Node.js y PHP/Laravel en backend. He trabajado sobre un sistema de gestión en producción, automatizado flujos entre sistemas internos y construido aplicaciones con IA integrada. Disponible para trabajar en Getafe. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": ES_FULL,
 "bullets": ["laravel", "sync", "paneles", "proxmox"],
 "proyectos": ["streakode", "alfred", "lifevault", "elite"],
 "saludo": "Estimado equipo de ALTEN:",
 "parrafos": [
  "Me presento al puesto de Desarrollador/a Full Stack para el proyecto de digitalización de fabricación en el sector aeronáutico. Automatizar procesos con una aplicación web completa, React delante y Python detrás, con IA donde aporte, encaja con lo que hago. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "En la Agencia de Digitalización Andaluza mantuve un sistema de gestión en producción con Laravel, JavaScript y SQL y monté flujos de sincronización y paneles con datos diarios para equipos internos. Streakode es una PWA en producción con Next.js, TypeScript y Supabase con tests automáticos, y Alfred es un sistema de agentes de IA en Python que automatiza procesos por API.",
  "Para ser transparente: mi experiencia profesional son cuatro meses, por debajo del año que piden, y no he trabajado con Django; mi Python backend es con scripts, APIs y agentes. Aprendo rápido un framework nuevo y lo compenso con proyectos que puedo enseñar.",
  "Puedo incorporarme de inmediato y trasladarme a Madrid. Quedo a su disposición para una entrevista.",
 ],
},
# 7 ------------------------------------------------------------------
{
 "slug": "Qtech-PythonEngineer", "lang": "es", "wm": False,
 "empresa": "Q-tech", "puesto_ref": "Python Engineer (Barcelona, híbrido)",
 "subtitulo": "Python Engineer · APIs REST, React y tests automáticos",
 "perfil": "Desarrollador (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) con Python en producción, APIs REST, frontend en React y TypeScript y tests automáticos como parte normal del desarrollo. Mantengo un sistema en Python 24/7 en un servidor Linux y he trabajado sobre código existente en producción. Disponible para trabajar híbrido en Barcelona. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Backend", ["Python", "APIs REST", "JSON", "Node.js", "PHP", "Laravel", "Webhooks"]),
    ("Frontend", ["React", "TypeScript", "JavaScript", "Next.js"]),
    ("Datos", ["PostgreSQL", "MySQL", "SQL", "Supabase"]),
    ("Calidad e infra", ["Vitest (tests automáticos)", "Git", "Pull requests en GitHub", "CI/CD (Netlify, Vercel)", "Linux"]),
 ],
 "bullets": ["laravel", "sync", "paneles", "proxmox"],
 "proyectos": ["alfred", "streakode", "lifevault", "elite"],
 "saludo": "Estimado equipo de Q-tech:",
 "parrafos": [
  "Me presento al puesto de Python Engineer para el equipo de Vulnerability. Desarrollar funcionalidades end-to-end con Python en backend y React en frontend, escribir tests y aprender del criterio de perfiles senior es exactamente el siguiente paso que busco. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Alfred es un sistema en Python que funciona 24/7 en un servidor Linux e integra por API Gmail, Notion, Google Sheets y Telegram. Streakode es una PWA en producción con Next.js y TypeScript, PostgreSQL y tests automáticos. En la Agencia de Digitalización Andaluza mantuve un sistema de gestión en producción con Laravel, JavaScript y SQL y monté flujos de sincronización por API.",
  "Para ser transparente: no he usado FastAPI ni Django en producción, mi experiencia con Docker y Kubernetes es básica y mi experiencia profesional son cuatro meses. La oferta pide ganas de moverse en un stack amplio sin dominarlo todo desde el inicio, y eso sí lo tengo.",
  "Puedo incorporarme de inmediato y trasladarme a Barcelona. Quedo a su disposición para una entrevista.",
 ],
},
# 8 ------------------------------------------------------------------
{
 "slug": "Smadex-SoftwareEngineerInternalTools", "lang": "en", "wm": False,
 "empresa": "Smadex", "puesto_ref": "Software Engineer (Internal tools), Barcelona",
 "subtitulo": "Software Engineer · Internal tools, integrations and workflow automation",
 "perfil": "Full-stack developer (Higher Technical Diploma in Web Application Development, 2025; Master's in Generative AI & Innovation, 2026) who builds internal tools and automations: integrations between systems via API, Google Workspace and Notion workflows, n8n and Make, and end-to-end apps in TypeScript, Node.js, Python and SQL. I maintained a production management system for internal teams and run my own automation platform 24/7. Willing to relocate to Barcelona. Native Spanish, B2 English (Cambridge, 2025).",
 "skills": [
    ("Full-stack", ["TypeScript", "JavaScript", "Node.js", "Python", "React", "Next.js", "PHP", "Laravel", "SQL", "PostgreSQL"]),
    ("Integrations", ["REST APIs", "Webhooks", "Google Workspace APIs", "Notion API", "Telegram API", "n8n", "Make", "Supabase"]),
    ("Shipping", ["Git", "GitHub pull requests", "Vitest (automated tests)", "CI/CD (Netlify, Vercel)", "Linux"]),
    ("AI", ["Claude API", "OpenAI API", "Tool calling", "RAG"]),
 ],
 "bullets": ["sync", "laravel", "paneles", "proxmox"],
 "proyectos": ["alfred", "streakode", "lifevault", "elite"],
 "saludo": "Hi Smadex team,",
 "parrafos": [
  "I am applying for the Software Engineer (Internal tools) role in the Platform Experience team. Turning manual processes around spreadsheets, documents and email into simple, maintainable tools, and choosing between building, integrating or just automating, is the work I enjoy most. I hold a Higher Technical Diploma in Web Application Development (2025) and a Master's in Generative AI & Innovation (2026).",
  "At the Agencia de Digitalización Andaluza I built API synchronisation flows between internal systems, real-time dashboards fed by daily automated ingestion, and maintained a production management system in Laravel, JavaScript and SQL for internal users. On my own I run Alfred, which automates my email, calendar, documents and spreadsheets through the Gmail, Google Sheets, Notion and Telegram APIs, and Streakode, a live Next.js PWA with automated tests.",
  "To be upfront: my professional experience is a four-month contract, below the year you ask for, and I have not used Angular, Salesforce or HubSpot. I am pragmatic about not overengineering, and I can show you the tools I mention running.",
  "I can start immediately and relocate to Barcelona. I would welcome the chance to talk.",
 ],
},
# 9 ------------------------------------------------------------------
{
 "slug": "Recodme-AIEngineer", "lang": "es", "wm": True,
 "empresa": "ReCodme", "puesto_ref": "AI Engineer (Madrid, híbrido)",
 "subtitulo": "AI Engineer · Agentes, RAG, tool calling y MCP en Python",
 "perfil": "Desarrollador de IA (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que construye agentes en Python: tool calling, servidores MCP, RAG con embeddings y orquestación de agentes especializados con memoria persistente. Mantengo en producción un sistema multi-agente 24/7 en Linux integrado por API con Gmail, Notion, Google Sheets y Telegram. Disponible para trabajar híbrido en Madrid. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": ES_IA, "proyectos": ["alfred", "lifevault", "elite", "streakode"],
 "saludo": "Estimado equipo de ReCodme:",
 "parrafos": [
  "Me presento al puesto de AI Engineer. RAG, tool calling, agentes y MCP, los cuatro pilares que piden, son con lo que trabajo a diario. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Alfred, mi sistema multi-agente en Python sobre la Claude API, funciona 24/7 en un servidor Linux: agentes especializados con memoria persistente, tools propias y servidores MCP para Gmail, Notion, Google Sheets y Telegram. En LifeVault y Estudiante Élite implementé RAG con embeddings y asistentes con contexto persistente. Me gusta traducir necesidades de usuarios no técnicos en soluciones; Estudiante Élite nació así, con estudiantes de derecho.",
  "Para ser transparente: no he usado LangGraph, LangChain, FastAPI ni Langfuse en producción, mis agentes están construidos directamente sobre la API, y mi experiencia profesional es de cuatro meses. Los conceptos los domino; el framework concreto lo aprendería rápido.",
  "Puedo incorporarme de inmediato y trasladarme a Madrid. Quedo a su disposición para una entrevista.",
 ],
},
# 10 -----------------------------------------------------------------
{
 "slug": "Experis-JuniorMidAutomatizacionPython", "lang": "es", "wm": False,
 "empresa": "Experis España", "puesto_ref": "Perfil Junior-Mid Automatización Python / Jenkins (Cloud & Automation)",
 "subtitulo": "Desarrollador Python · Automatización, APIs y CI/CD",
 "perfil": "Desarrollador (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que automatiza procesos con Python: APIs, scripts, tareas programadas y servicios que corren 24/7 en un servidor Linux. Trabajo con Git, pull requests y CI/CD, y lideré la migración de servidores a máquinas virtuales Linux en Proxmox. Disponible para trabajar híbrido en Madrid o Barcelona. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Automatización", ["Python", "APIs REST", "Scripts y tareas programadas", "Webhooks", "n8n", "systemd"]),
    ("Infraestructura", ["Linux", "Proxmox (máquinas virtuales)", "CI/CD (Netlify, Vercel)", "Git", "Pull requests en GitHub", "AWS Academy (nube)"]),
    ("Desarrollo", ["TypeScript", "JavaScript", "Node.js", "PHP", "Laravel", "SQL", "PostgreSQL"]),
 ],
 "bullets": ["proxmox", "sync", "laravel", "paneles"],
 "proyectos": ["alfred", "streakode", "lifevault", "elite"],
 "saludo": "Estimado equipo de Experis:",
 "parrafos": [
  "Me presento al puesto de perfil Junior-Mid de Automatización Python para el proyecto de IBM Cloud. Desarrollar una API en Python que automatice tareas sobre servidores y reduzca procesos manuales es el tipo de trabajo que más disfruto. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "En la Agencia de Digitalización Andaluza lideré la migración a máquinas virtuales Linux en Proxmox, que redujo el tiempo de despliegue en 4 días, y monté flujos de sincronización automática entre sistemas por API. Por mi cuenta mantengo Alfred, un sistema en Python que corre 24/7 en un servidor Linux con servicios systemd y tareas programadas, y aplicaciones con CI/CD en Netlify y Vercel.",
  "Para ser transparente: no he usado Terraform, Jenkins, Flask ni IBM Cloud, y mi experiencia profesional son cuatro meses. Es la oportunidad que busco para aprender infraestructura como código con un equipo que ya la usa.",
  "Puedo incorporarme de inmediato y trabajar híbrido en Madrid o Barcelona. Quedo a su disposición para una entrevista.",
 ],
},
# 11 (sustituye a Prodware, bloqueada por captcha) -------------------
{
 "slug": "Roams-DesarrolladorFullStackAIAugmented", "lang": "es", "wm": True,
 "empresa": "Roams", "puesto_ref": "Desarrollador/a Full-Stack AI-Augmented (Palencia)",
 "subtitulo": "Desarrollador Full-Stack AI-Augmented · Claude Code, especificaciones y Python",
 "perfil": "Desarrollador full-stack (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que desarrolla con Claude Code y agentes a diario: primero especificaciones en Markdown y contratos de API, después código revisado con tests y criterio propio. Python, TypeScript, React y PostgreSQL. Disponible para trasladarme a Palencia. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Desarrollo con IA", ["Claude Code", "Agentes y tool calling", "MCP", "Specs en Markdown", "Claude API"]),
    ("Full-stack", ["Python", "Node.js", "APIs REST", "PostgreSQL", "Supabase", "TypeScript", "React", "Next.js"]),
    ("Calidad e infra", ["Vitest", "Git", "Pull requests", "CI/CD (Netlify, Vercel)", "Linux", "AWS Academy"]),
 ],
 "proyectos": ["alfred", "streakode", "lifevault", "elite"],
 "saludo": "Estimado equipo de Roams:",
 "parrafos": [
  "Me presento al puesto de Desarrollador/a Full-Stack AI-Augmented. Trabajar con Claude Code y agentes como aliados principales, pero definiendo antes qué construir y revisando después lo que generan, es exactamente cómo desarrollo hoy. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Alfred, mi sistema multi-agente en Python, está organizado alrededor de especificaciones: cada tarea tiene una directiva en Markdown con objetivo, pasos y casos límite, y scripts deterministas que la ejecutan; los agentes orquestan, no improvisan. Streakode, una PWA en producción con Next.js, TypeScript y Supabase con RLS, la construyo con Claude Code y la protejo con tests automáticos y revisión de cada cambio. En la Agencia de Digitalización Andaluza trabajé sobre código ajeno en producción (Laravel, JavaScript, SQL).",
  "Para ser transparente: mi frontend es React, no Angular; no he usado Terraform y mi experiencia con AWS es formativa (AWS Academy). Mi experiencia profesional son cuatro meses. Lo que sí traigo es criterio para dar contexto a un modelo, reducir alucinaciones y detectar cuándo el código generado no es sostenible.",
  "Puedo incorporarme de inmediato y trasladarme a Palencia. Quedo a su disposición para una entrevista y para enseñarles cómo trabajo con Claude Code en un caso real.",
 ],
},
]
