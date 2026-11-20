FECHA_ES = "Montilla, 6 de noviembre de 2026"
FECHA_EN = "Montilla, Córdoba (Spain) · 6 November 2026"

ES_IA = [
    ("IA generativa", ["Prompt engineering", "Agentes y tool calling", "RAG", "Embeddings", "MCP", "Claude API", "OpenAI API", "Gemini API", "Sistemas multiagente", "Whisper"]),
    ("Lenguajes & datos", ["Python", "JavaScript", "TypeScript", "SQL", "PostgreSQL", "MySQL", "PHP"]),
    ("Ingeniería", ["APIs REST", "JSON", "Webhooks", "Git", "Pull requests en GitHub", "Linux", "Vitest (tests automáticos)", "CI/CD (Netlify, Vercel)"]),
    ("Frameworks", ["n8n", "Make", "Supabase", "Next.js", "React", "Node.js", "Laravel"]),
]
ES_FULL = [
    ("Frontend", ["React", "TypeScript", "JavaScript", "Next.js", "React Native", "HTML5", "CSS3"]),
    ("Backend & APIs", ["Node.js", "Python", "PHP", "Laravel", "APIs REST", "JSON", "Supabase", "Webhooks"]),
    ("Datos", ["PostgreSQL", "MySQL", "SQL", "Diseño de esquemas", "RLS"]),
    ("Ingeniería", ["Git", "Pull requests en GitHub", "Vitest (tests automáticos)", "CI/CD (Netlify, Vercel)", "Linux"]),
    ("IA", ["Claude API", "OpenAI API", "RAG", "Agentes y tool calling", "n8n"]),
]

OFERTAS = [
# 1 ------------------------------------------------------------------
{
 "slug": "MalthusDarwin-AIInternalApplicationsSpecialist", "lang": "es", "wm": True,
 "empresa": "Malthus Darwin (para empresa de logística cliente)", "puesto_ref": "AI & Internal Applications Specialist (Masquefa)",
 "subtitulo": "AI & Internal Applications Specialist · Aplicaciones internas y automatización con IA",
 "perfil": "Desarrollador (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que convierte necesidades concretas en aplicaciones internas y automatizaciones con JavaScript/TypeScript y Python, programando a diario con Claude y depurando lo generado. Integro APIs y bases de datos y automatizo correo y flujos administrativos. Disponible para trabajar presencial en Masquefa. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("IA y programación asistida", ["Claude", "Claude Code", "ChatGPT", "Prompting orientado a código", "Agentes y tool calling", "Claude API"]),
    ("Desarrollo", ["JavaScript", "TypeScript", "Python", "React", "Next.js", "Node.js", "PHP", "Laravel"]),
    ("Integraciones y datos", ["APIs REST", "Webhooks", "SQL", "PostgreSQL", "MySQL", "Supabase", "n8n", "Make"]),
    ("Ingeniería", ["Git", "Linux", "Vitest (tests automáticos)", "CI/CD (Netlify, Vercel)"]),
 ],
 "bullets": ["sync", "laravel", "paneles", "proxmox"],
 "proyectos": ["alfred", "streakode", "lifevault", "elite"],
 "saludo": "Estimado equipo de Malthus Darwin:",
 "parrafos": [
  "Me presento al puesto de AI & Internal Applications Specialist en Masquefa. Identificar una necesidad concreta y convertirla rápido en una herramienta que funcione, programando con IA y entendiendo el código que sale, es exactamente como trabajo. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Alfred, mi sistema de agentes en Python sobre la Claude API, clasifica mi correo a diario, registra datos en Google Sheets y Notion y genera documentos a medida, integrado por API con Gmail y Telegram. Streakode es una PWA en producción con Next.js, Supabase y tests automáticos, desarrollada con asistentes de código. En la Agencia de Digitalización Andaluza mantuve un sistema de gestión con Laravel, JavaScript y SQL y monté flujos de sincronización entre sistemas internos.",
  "Me atrae que el objetivo no sean grandes sistemas corporativos, sino resolver problemas reales de logística con soluciones pequeñas y mantenibles. Para ser transparente: mi experiencia en empresa son cuatro meses y no he trabajado en el sector logístico.",
  "Puedo incorporarme de inmediato y trasladarme a la zona para trabajar presencial. Quedo a su disposición para una entrevista y para enseñarles estas herramientas funcionando.",
 ],
},
# 2 ------------------------------------------------------------------
{
 "slug": "Practikalia-PromptEngineer", "lang": "es", "wm": True,
 "empresa": "Practikalia Experience", "puesto_ref": "Prompt Engineer (Madrid, híbrido)",
 "subtitulo": "Prompt Engineer · Prompts, agentes y LLMs integrados en producto",
 "perfil": "Desarrollador de IA (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que diseña prompts complejos para tareas reales: system prompts, agentes con tool calling y asistentes con memoria sobre Claude, GPT y Gemini, e integra los modelos en aplicaciones (Python, TypeScript, APIs). Mantengo en producción un sistema multi-agente 24/7. Disponible en Madrid, híbrido. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": ES_IA[:2] + [("Ingeniería", ["APIs REST", "Git", "Linux", "n8n", "Make", "Supabase", "React", "Next.js", "CI/CD (Netlify, Vercel)"])], "proyectos": ["alfred", "elite", "lifevault", "streakode"],
 "saludo": "Estimado equipo de Practikalia Experience:",
 "parrafos": [
  "Me presento al puesto de Prompt Engineer. Diseñar, probar y refinar instrucciones para que un modelo conversacional se comporte de forma natural, fiable y coherente es parte de mi trabajo diario. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "En Alfred, mi sistema multi-agente sobre la Claude API, cada agente tiene su propio carácter, instrucciones y reglas que he ido ajustando con el uso real, con un registro de los errores cometidos para no repetirlos. Estudiante Élite es un asistente de tutoría con IA para estudiantes de derecho, con RAG sobre el temario y memoria de sesión: mi primer contacto con objetivos pedagógicos reales. En LifeVault integré un chatbot con contexto persistente sobre documentos del usuario.",
  "Me atrae que sus simuladores usen la conversación con IA para entrenar habilidades: es un caso en el que la calidad del prompt se nota directamente en quien aprende. Para ser claro: no he medido prompts con A/B testing formal ni tengo formación en diseño instruccional, y mi experiencia en empresa son cuatro meses.",
  "Puedo incorporarme de inmediato y trasladarme a Madrid. Quedo a su disposición para una entrevista.",
 ],
},
# 3 ------------------------------------------------------------------
{
 "slug": "Ventos-JuniorSoftwareDeveloper", "lang": "es", "wm": False,
 "empresa": "Ernesto Ventós", "puesto_ref": "Junior Software Developer (Sant Just Desvern)",
 "subtitulo": "Junior Software Developer · Aplicaciones internas, web y SQL",
 "perfil": "Desarrollador junior con CFGS en Desarrollo de Aplicaciones Web (2025) y Máster en IA Generativa e Innovación (2026). He desarrollado y mantenido aplicaciones internas en producción con JavaScript, HTML, CSS, PHP y MySQL, resuelto incidencias sobre código existente y documentado lo desarrollado, además de varios proyectos propios publicados. Uso Git a diario y leo documentación técnica en inglés. Disponible para trasladarme a Barcelona. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Web", ["HTML5", "CSS3", "JavaScript", "TypeScript", "React", "Next.js"]),
    ("Backend", ["PHP", "Laravel", "Python", "Node.js", "APIs REST"]),
    ("Bases de datos", ["MySQL", "SQL", "PostgreSQL", "Supabase"]),
    ("Herramientas", ["Git", "Pull requests en GitHub", "Linux", "Vitest (tests automáticos)", "CI/CD (Netlify, Vercel)"]),
    ("IA", ["Claude API", "OpenAI API", "RAG", "Automatización con n8n"]),
 ],
 "bullets": ["laravel", "sync", "paneles", "proxmox"],
 "proyectos": ["streakode", "lifevault", "alfred", "elite"],
 "saludo": "Estimado equipo de Ventós:",
 "parrafos": [
  "Me presento al puesto de Junior Software Developer. Colaborar en aplicaciones internas, hablar con los usuarios para entender qué necesitan y resolver incidencias es lo que hice en mi primer empleo, y encajo en la formación que piden: CFGS en Desarrollo de Aplicaciones Web (2025), al que he sumado el Máster en IA Generativa e Innovación (2026).",
  "En la Agencia de Digitalización Andaluza mantuve un sistema de gestión en producción con Laravel, JavaScript y SQL, corregí incidencias sobre código existente y monté flujos de sincronización entre sistemas internos. Por mi cuenta he publicado Streakode, una PWA con Next.js, TypeScript y Supabase con tests automáticos, y LifeVault, una plataforma de documentos con TypeScript y PostgreSQL. Trabajo siempre con Git y documento lo que hago.",
  "Me atrae entrar en un equipo de IT interno de una empresa internacional, donde el software se usa a diario y el feedback llega de los propios usuarios. Para ser transparente: mi experiencia en empresa son cuatro meses, por debajo del año que indican, aunque la completo con proyectos que siguen en producción; tampoco he trabajado con C#, SQL Server ni Business Central, y estoy dispuesto a aprenderlos.",
  "Puedo incorporarme de inmediato y trasladarme a la zona de Barcelona. Quedo a su disposición para una entrevista.",
 ],
},
# 4 ------------------------------------------------------------------
{
 "slug": "Alvores-TecnicoJuniorSolucionesIT", "lang": "es", "wm": False,
 "empresa": "Alvores", "puesto_ref": "Técnico/a Junior de Desarrollo de Soluciones IT (Almería o Málaga)",
 "subtitulo": "Técnico Junior de Desarrollo · Aplicaciones de negocio, automatización y web",
 "perfil": "Técnico junior de desarrollo con CFGS en Desarrollo de Aplicaciones Web (2025) y Máster en IA Generativa e Innovación (2026). He mantenido una plataforma de gestión empresarial en producción, resuelto incidencias y mejoras, automatizado procesos entre sistemas y creado webs y aplicaciones con HTML, CSS, JavaScript y React. Aprendo por mi cuenta herramientas nuevas y documento lo que desarrollo. Resido en Córdoba, con disponibilidad para Almería o Málaga. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Web", ["HTML5", "CSS3", "JavaScript", "TypeScript", "React", "Next.js"]),
    ("Automatización e integración", ["n8n", "Make", "APIs REST", "Webhooks", "Google Workspace APIs"]),
    ("Backend y datos", ["PHP", "Laravel", "Python", "SQL", "MySQL", "PostgreSQL", "Supabase"]),
    ("Herramientas", ["Git", "Linux", "Vitest (tests automáticos)", "CI/CD (Netlify, Vercel)"]),
    ("IA", ["Claude API", "OpenAI API", "Agentes y tool calling", "RAG"]),
 ],
 "bullets": ["laravel", "sync", "paneles", "proxmox"],
 "proyectos": ["lifevault", "streakode", "alfred", "elite"],
 "saludo": "Estimado equipo de Alvores:",
 "parrafos": [
  "Me presento al puesto de Técnico/a Junior de Desarrollo de Soluciones IT. Mantener una plataforma de gestión interna, resolver incidencias, atender peticiones de mejora y ocuparme también de la web es el tipo de trabajo que busco, y tengo la formación que piden: CFGS en Desarrollo de Aplicaciones Web (2025) y Máster en IA Generativa e Innovación (2026).",
  "En la Agencia de Digitalización Andaluza mantuve un sistema de gestión en producción con Laravel, JavaScript y SQL, monté flujos de sincronización entre sistemas y paneles con datos actualizados a diario. He creado aplicaciones web con React y TypeScript, como Streakode y LifeVault, y automatizaciones con n8n y Make, cuya lógica de flujos y conectores se parece a la de Power Automate.",
  "Para ser claro en lo más importante: no he trabajado con Power Apps ni Dataverse, y sé que lo piden como conocimiento mínimo. Vengo de la programación, no del low-code, y me comprometo a formarme en Power Platform desde ahora; su mentoría directa es precisamente lo que me atrae del puesto, junto con la posibilidad de trabajar en Andalucía.",
  "Puedo incorporarme de inmediato en Almería o Málaga. Quedo a su disposición para una entrevista.",
 ],
},
# 5 ------------------------------------------------------------------
{
 "slug": "Hays-ProgramadorPythonRemoto", "lang": "es", "wm": False,
 "empresa": "Hays", "puesto_ref": "Programador/a Python (100 % remoto)",
 "subtitulo": "Programador Python · APIs, integración de sistemas y bases de datos",
 "perfil": "Programador con CFGS en Desarrollo de Aplicaciones Web (2025) y Máster en IA Generativa e Innovación (2026). Desarrollo y mantengo en Python un sistema 24/7 en Linux con integraciones por API (Gmail, Notion, Google Sheets, Telegram), scripts deterministas y gestión de incidencias en producción. He trabajado con PostgreSQL y MySQL, integración de sistemas y Git. Disponible en remoto desde España. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Python", ["Python", "Scripts de automatización", "Integración de APIs", "Claude API", "OpenAI API"]),
    ("APIs e integración", ["APIs REST", "JSON", "Webhooks", "n8n", "Make"]),
    ("Bases de datos", ["PostgreSQL", "MySQL", "SQL", "Supabase", "Diseño de esquemas"]),
    ("Herramientas", ["Git", "Pull requests en GitHub", "Linux", "systemd", "CI/CD (Netlify, Vercel)"]),
    ("Otros lenguajes", ["TypeScript", "JavaScript", "PHP", "Laravel"]),
 ],
 "bullets": ["sync", "laravel", "paneles", "proxmox"],
 "proyectos": ["alfred", "lifevault", "elite", "streakode"],
 "saludo": "Estimado equipo de Hays:",
 "parrafos": [
  "Me presento al puesto de Programador/a Python en remoto. Desarrollar, mantener y evolucionar soluciones en Python, integrar sistemas por API y resolver incidencias es lo que hago desde hace meses en mi propio sistema en producción. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Alfred es un sistema en Python que corre 24/7 en un servidor Linux con servicios systemd, integrado por API con Gmail, Notion, Google Sheets y Telegram; su mantenimiento incluye diagnosticar errores en producción, como bloqueos del bot o conflictos entre instancias, y corregirlos. En la Agencia de Digitalización Andaluza trabajé con Laravel, JavaScript y SQL y monté sincronizaciones entre sistemas internos. Uso Git a diario y he diseñado esquemas en PostgreSQL y MySQL.",
  "Para ser transparente: mi experiencia en empresa son cuatro meses y en PHP; mi experiencia en Python viene de proyectos propios en producción, no de proyectos corporativos para organismos públicos. Me atrae el contrato indefinido y la posibilidad de entrar en un entorno con procesos más maduros.",
  "Puedo incorporarme de inmediato. Quedo a su disposición para una entrevista.",
 ],
},
# 6 ------------------------------------------------------------------
{
 "slug": "Juryo-SoftwareEngineer", "lang": "en", "wm": False,
 "empresa": "Juryo", "puesto_ref": "Software Engineer (Barcelona, on site)",
 "subtitulo": "Software Engineer · AI-native full-stack development with TypeScript and Python",
 "perfil": "AI-native developer (Higher Technical Diploma in Web Application Development, 2025; Master's in Generative AI & Innovation, 2026). I direct coding agents daily and review what they produce, building backends, APIs, webhooks and integrations in TypeScript and Python on PostgreSQL. I run a multi-agent system 24/7 on Linux and a live PWA with automated tests. Willing to relocate to Barcelona and work on site. Native Spanish, English B2 (Cambridge, 2025).",
 "skills": [
    ("Backend & data", ["TypeScript", "Node.js", "Python", "SQL", "PostgreSQL", "REST APIs", "Webhooks", "Supabase"]),
    ("AI-native", ["Claude Code", "Coding agents", "Claude API", "Tool calling", "MCP", "RAG"]),
    ("Product", ["React", "Next.js", "Dashboards", "Vercel", "Netlify"]),
    ("Shipping", ["Git", "GitHub pull requests", "Vitest (automated tests)", "CI/CD", "Linux"]),
 ],
 "bullets": ["sync", "laravel", "paneles", "proxmox"],
 "proyectos": ["streakode", "alfred", "lifevault", "elite"],
 "saludo": "Hi Juryo team,",
 "parrafos": [
  "I am applying for the Software Engineer role in Barcelona. I applied to your AI Engineer role on 3 November and I am writing again because this one fits how I already build: directing coding agents, reviewing their work and shipping end to end. I hold a Higher Technical Diploma in Web Application Development (2025) and a Master's in Generative AI & Innovation (2026).",
  "Streakode is a live PWA in Next.js, TypeScript and Supabase with row-level security, scheduled jobs, a server-timed daily challenge and automated tests. Alfred is my Python multi-agent system, running 24/7 on Linux, with integrations across Gmail, Notion, Google Sheets and Telegram that I keep reliable, including diagnosing production failures. At Andalusia's Digital Agency I worked on a production management system in Laravel, JavaScript and SQL and built synchronisation flows between internal systems.",
  "To be upfront: I do not have the depth of production experience under heavy load that you describe. My professional experience is a four-month contract, my projects serve far fewer users than a platform for law firms, and my English is B2. What I can offer is speed, ownership and work you can inspect.",
  "I can start immediately and relocate to Barcelona for 100% on-site work. I would welcome the chance to talk.",
 ],
},
# 7 ------------------------------------------------------------------
{
 "slug": "Adecco-VoiceAIAutomationSpecialist", "lang": "es", "wm": True,
 "empresa": "The Adecco Group (para empresa fintech cliente)", "puesto_ref": "Voice AI & Automation Specialist (Mairena del Aljarafe)",
 "subtitulo": "Voice AI & Automation · Agentes conversacionales, integraciones y automatización",
 "perfil": "Desarrollador de IA (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que construye agentes conversacionales con Claude y OpenAI: tool calling para ejecutar acciones en sistemas externos, bases de conocimiento con RAG, memoria de conversación y notas de voz transcritas con Whisper. Integro APIs y automatizo flujos con n8n y Make. Resido en Córdoba, con disponibilidad para Sevilla. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("IA conversacional", ["Agentes y tool calling", "Diseño de flujos conversacionales", "RAG", "Embeddings", "Whisper (voz a texto)", "Claude API", "OpenAI API", "MCP"]),
    ("Automatización e integración", ["n8n", "Make", "APIs REST", "Webhooks", "Gmail API", "Notion API", "Telegram API"]),
    ("Desarrollo", ["Python", "TypeScript", "JavaScript", "SQL", "PostgreSQL", "Supabase"]),
    ("Ingeniería", ["Git", "Linux", "CI/CD (Netlify, Vercel)"]),
 ],
 "proyectos": ["alfred", "elite", "lifevault", "streakode"],
 "saludo": "Estimado equipo de Adecco:",
 "parrafos": [
  "Me presento al puesto de Voice AI & Automation Specialist. Diseñar agentes que conversan, consultan una base de conocimiento y ejecutan acciones autorizadas en otros sistemas es lo que hago en mis proyectos. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Alfred es mi sistema multi-agente sobre la Claude API: lo uso por Telegram, también con notas de voz transcritas con Whisper, y registra y actualiza información en Gmail, Notion y Google Sheets mediante tool calling. Estudiante Élite es un asistente con RAG, memoria de sesión y transcripción de audio. LifeVault añade un chatbot con contexto persistente sobre documentos. Las integraciones las hago por API y con n8n y Make.",
  "Para ser transparente: no he trabajado con Vapi ni con telefonía real, solo con notas de voz, ni he integrado HubSpot, y mi experiencia en empresa son cuatro meses. La base de agentes, herramientas y conocimiento es la misma y puedo aprender esa capa rápido. Me atrae colaborar directamente con el CTO en un proyecto con esa autonomía.",
  "Puedo incorporarme de inmediato y trasladarme a la zona de Sevilla. Quedo a su disposición para una entrevista.",
 ],
},
# 8 ------------------------------------------------------------------
{
 "slug": "Profile-FullStackDeveloperJavaScript", "lang": "es", "wm": False,
 "empresa": "Profile Software Services", "puesto_ref": "Full Stack Developer (JavaScript), 100 % remoto",
 "subtitulo": "Full Stack Developer · TypeScript, Node.js y PostgreSQL",
 "perfil": "Desarrollador full stack con CFGS en Desarrollo de Aplicaciones Web (2025) y Máster en IA Generativa e Innovación (2026). Construyo aplicaciones con TypeScript, React, Node.js y PostgreSQL: componentes reutilizables, consumo de APIs, lógica de negocio, validación de datos y tests automáticos. He mantenido un sistema de gestión en producción y tengo una PWA publicada. Disponible en remoto desde España. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": ES_FULL,
 "bullets": ["laravel", "sync", "paneles", "proxmox"],
 "proyectos": ["streakode", "lifevault", "alfred", "elite"],
 "saludo": "Estimado equipo de Profile:",
 "parrafos": [
  "Me presento al puesto de Full Stack Developer en remoto. Desarrollar a la vez la interfaz, los servicios y las consultas a PostgreSQL con TypeScript es mi forma habitual de trabajar. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "Streakode es una PWA en producción con Next.js, TypeScript y Supabase: componentes reutilizables, lógica de negocio en servidor, un reto diario cronometrado, RLS en PostgreSQL y tests automáticos con Vitest. LifeVault combina TypeScript, React Native y PostgreSQL. En la Agencia de Digitalización Andaluza mantuve un sistema de gestión en producción con Laravel, JavaScript y SQL e integré sistemas internos por API.",
  "Para ser claro: no he trabajado con Vue, Jest ni Sonar (mi framework es React y mis tests van con Vitest, muy parecido a Jest), ni he aplicado el patrón BFF como tal, y mi experiencia en empresa son cuatro meses. Me atrae el onboarding que describen y que busquen personas implicadas antes que perfiles con años acumulados.",
  "Puedo incorporarme de inmediato. Quedo a su disposición para una entrevista.",
 ],
},
# 9 ------------------------------------------------------------------
{
 "slug": "Drasanvi-IASpecialist", "lang": "es", "wm": True,
 "empresa": "Drasanvi", "puesto_ref": "IA Specialist (León)",
 "subtitulo": "IA Specialist · Agentes, automatización y adopción de IA en la empresa",
 "perfil": "Especialista en IA aplicada (CFGS en Desarrollo de Aplicaciones Web, 2025; Máster en IA Generativa e Innovación, 2026) que detecta tareas repetitivas y las convierte en agentes, asistentes y automatizaciones con Claude, Python, SQL y APIs. Cuido que las soluciones se usen de verdad, estén documentadas y protejan los datos. Mantengo en producción un sistema multi-agente 24/7. Disponible para trasladarme a León. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("IA generativa", ["Prompts y agentes", "Claude", "ChatGPT", "Claude API", "OpenAI API", "Tool calling", "RAG", "Embeddings", "MCP"]),
    ("Datos", ["Python", "SQL", "PostgreSQL", "MySQL", "Google Sheets", "Paneles de datos"]),
    ("Automatización", ["n8n", "Make", "APIs REST", "Webhooks", "Scripts"]),
    ("Desarrollo", ["TypeScript", "JavaScript", "React", "Next.js", "Git", "Linux"]),
 ],
 "bullets": ["sync", "paneles", "laravel", "proxmox"],
 "proyectos": ["alfred", "lifevault", "elite", "streakode"],
 "saludo": "Estimado equipo de Drasanvi:",
 "parrafos": [
  "Me presento al puesto de IA Specialist. Priorizar soluciones que se usan y ahorran tiempo frente a pruebas de concepto sin continuidad, como pide su oferta, es el criterio con el que construyo. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026), que valoran.",
  "Alfred, mi sistema de agentes con Claude y Python, funciona 24/7 y me lleva correo, calendario, registros en Google Sheets y Notion y documentos, con un registro de errores y reglas de seguridad sobre lo que puede hacer sin confirmación. En la Agencia de Digitalización Andaluza automaticé sincronizaciones entre sistemas internos, eliminando errores manuales, y monté paneles con datos actualizados a diario. En LifeVault y Estudiante Élite trabajé con RAG sobre documentación.",
  "Debo ser claro con los límites: piden un grado y de dos a cuatro años de experiencia, y yo tengo CFGS, máster y cuatro meses en empresa. No he trabajado con SAP Business One, Power BI ni modelos de previsión de demanda, ni he gestionado el cumplimiento del RGPD o del Reglamento de IA. Me atrae poder acompañar a cada departamento desde dentro.",
  "Puedo incorporarme de inmediato y trasladarme a León. Quedo a su disposición para una entrevista.",
 ],
},
# 10 -----------------------------------------------------------------
{
 "slug": "HolaConsultores-ProgramadorFullStack", "lang": "es", "wm": False,
 "empresa": "Hola Consultores", "puesto_ref": "Programador full stack (Barcelona, híbrido)",
 "subtitulo": "Programador Full Stack · PHP, React y TypeScript",
 "perfil": "Programador full stack con CFGS en Desarrollo de Aplicaciones Web (2025) y Máster en IA Generativa e Innovación (2026). He desarrollado y mantenido aplicaciones web empresariales con PHP y Laravel, JavaScript y SQL, y construyo interfaces con React y TypeScript, APIs REST, tests automáticos y control de versiones con Git. Disponible para trasladarme a Barcelona, híbrido. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Backend", ["PHP", "Laravel", "APIs REST", "Node.js", "Python", "Webhooks"]),
    ("Frontend", ["React", "TypeScript", "JavaScript", "Next.js", "HTML5", "CSS3"]),
    ("Datos", ["MySQL", "SQL", "PostgreSQL", "Supabase"]),
    ("Calidad", ["Git", "Pull requests en GitHub", "Vitest (tests automáticos)", "CI/CD (Netlify, Vercel)", "Linux"]),
    ("IA", ["Claude API", "OpenAI API", "Agentes y tool calling", "RAG"]),
 ],
 "bullets": ["laravel", "sync", "paneles", "proxmox"],
 "proyectos": ["streakode", "lifevault", "alfred", "elite"],
 "saludo": "Estimado equipo de Hola Consultores:",
 "parrafos": [
  "Me presento al puesto de Programador/a Full Stack. Buscan buenas bases técnicas y ganas de crecer en aplicaciones web empresariales con PHP y React, y ese es mi punto de partida. Tengo el CFGS en Desarrollo de Aplicaciones Web (2025) y el Máster en IA Generativa e Innovación (2026).",
  "En la Agencia de Digitalización Andaluza desarrollé y mantuve un sistema de gestión en producción con Laravel, JavaScript y SQL, e integré sistemas internos por API. En frontend he construido Streakode, una PWA en producción con Next.js y TypeScript con tests automáticos en Vitest, y LifeVault, con React Native y TypeScript sobre PostgreSQL. Trabajo con pull requests en GitHub y CI/CD.",
  "Para ser transparente: mi experiencia en PHP es con Laravel, no con Symfony, Doctrine ni Symfony Messenger; tampoco he usado SQL Server ni PHPUnit, y mi experiencia en empresa son cuatro meses. Conozco conceptos equivalentes de Laravel (ORM y migraciones) y me atrae que paguen certificaciones y cursos para formarme.",
  "Puedo incorporarme de inmediato y trasladarme a Barcelona. Quedo a su disposición para una entrevista.",
 ],
},
# 11 -----------------------------------------------------------------
{
 "slug": "ALTECH-FrontendDeveloperReact", "lang": "es", "wm": False,
 "empresa": "ALTECH Solutions and Consulting", "puesto_ref": "Frontend Developer (React), Barcelona",
 "subtitulo": "Frontend Developer · React, TypeScript y APIs REST",
 "perfil": "Desarrollador frontend con CFGS en Desarrollo de Aplicaciones Web (2025) y Máster en IA Generativa e Innovación (2026). Construyo interfaces con React, Next.js, React Native y TypeScript, consumo APIs REST, escribo tests automáticos y documento lo que desarrollo. Tengo una PWA en producción y he trabajado sobre código existente en un sistema de gestión real. Disponible en remoto o para trasladarme a Barcelona. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Frontend", ["React", "TypeScript", "JavaScript", "Next.js", "React Native", "HTML5", "CSS3", "Tailwind"]),
    ("APIs y backend", ["APIs REST", "JSON", "Node.js", "Supabase", "PHP", "Laravel", "Python"]),
    ("Calidad", ["Vitest (tests automáticos)", "Git", "Pull requests en GitHub", "CI/CD (Netlify, Vercel)"]),
    ("Datos", ["PostgreSQL", "MySQL", "SQL"]),
    ("IA", ["Claude API", "OpenAI API", "RAG", "Agentes y tool calling"]),
 ],
 "bullets": ["laravel", "paneles", "sync", "proxmox"],
 "proyectos": ["streakode", "lifevault", "alfred", "elite"],
 "saludo": "Estimado equipo de ALTECH:",
 "parrafos": [
  "Me presento al puesto de Frontend Developer (React). Encajo en lo que piden: CFGS en Desarrollo de Aplicaciones Web (2025), al que he sumado el Máster en IA Generativa e Innovación (2026), y experiencia práctica con React en proyectos que están publicados.",
  "Streakode es una PWA en producción con Next.js, TypeScript y Tailwind: rachas, rankings y un reto diario cronometrado en servidor, con tests automáticos en Vitest. LifeVault es una aplicación con React Native y TypeScript, conectada a una API sobre PostgreSQL. En la Agencia de Digitalización Andaluza mantuve un sistema de gestión en producción con Laravel, JavaScript y SQL, con paneles que se actualizaban a diario, y aprendí a trabajar sobre código ajeno.",
  "Me atrae trabajar en proyectos de transporte y movilidad junto a un equipo senior del que aprender. Para ser transparente: mi experiencia en empresa son cuatro meses, no he usado .NET, Docker ni Kubernetes, y mi experiencia con Scrum es limitada.",
  "Puedo incorporarme de inmediato, en remoto o trasladándome a Barcelona. Quedo a su disposición para una entrevista.",
 ],
},
# 12 -----------------------------------------------------------------
{
 "slug": "Accenture-DixcoverProgramaPracticasFP", "lang": "es", "wm": False,
 "empresa": "Accenture", "puesto_ref": "Dixcover - Programa Prácticas FP (R00333176)",
 "subtitulo": "Desarrollo de aplicaciones, cloud, IA y automatización · CFGS DAW",
 "perfil": "Titulado en CFGS de Desarrollo de Aplicaciones Web (2025) con Máster en IA Generativa e Innovación (2026), que busca su primera experiencia larga en proyectos reales de tecnología. Construyo aplicaciones con TypeScript, React y Python, automatizaciones e integraciones por API y agentes de IA sobre LLMs, y he mantenido un sistema de gestión en producción. Disponible en cualquiera de sus oficinas. Español nativo, inglés B2 (Cambridge, 2025).",
 "skills": [
    ("Desarrollo", ["TypeScript", "JavaScript", "Python", "React", "Next.js", "React Native", "PHP", "Laravel", "APIs REST"]),
    ("IA y automatización", ["Claude API", "OpenAI API", "Agentes y tool calling", "RAG", "n8n", "Make"]),
    ("Cloud y datos", ["AWS Academy", "Linux", "Proxmox", "PostgreSQL", "MySQL", "SQL", "Supabase"]),
    ("Ingeniería", ["Git", "Pull requests en GitHub", "Vitest (tests automáticos)", "CI/CD (Netlify, Vercel)"]),
 ],
 "bullets": ["laravel", "sync", "proxmox", "paneles"],
 "proyectos": ["alfred", "streakode", "lifevault", "elite"],
 "saludo": "Estimado equipo de Accenture:",
 "parrafos": [
  "Me presento a Dixcover FP para el área de Technology. El programa valora el perfil DAW y busca motivación por encima de la experiencia. Debo aclarar algo desde el principio: terminé el CFGS en Desarrollo de Aplicaciones Web en 2025 y el Máster en IA Generativa e Innovación en 2026, así que ya no estoy matriculado. Si el programa exige estar cursando el ciclo o un convenio vigente, les agradezco que me lo indiquen y que valoren mi candidatura para otras vías de entrada.",
  "He trabajado en lo que describen. En la Agencia de Digitalización Andaluza mantuve un sistema de gestión en producción con Laravel, JavaScript y SQL y lideré la migración a máquinas virtuales Linux en Proxmox. Alfred, mi sistema multi-agente en Python, funciona 24/7 con integraciones por API, y Streakode es una PWA en producción con Next.js, Supabase y tests automáticos.",
  "Me atrae trabajar en proyectos reales desde el primer día, con mentoring, y aprender herramientas que aún no he usado en un cliente, como Azure, SAP o Salesforce. Mi inglés es B2 (Cambridge, 2025): me manejo con documentación y en conversación técnica, aunque quiero seguir mejorándolo.",
  "Puedo incorporarme de inmediato en cualquiera de sus oficinas. Quedo a su disposición para una entrevista.",
 ],
},
]
