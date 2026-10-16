"""Данные английской версии: подменяют русские структуры build.py и переводят оставшиеся строки интерфейса."""
import html as _html
import json
import re
from pathlib import Path

esc = lambda s: _html.escape(s, quote=True)
HERE = Path(__file__).parent
GITHUB = "https://github.com/astro090-pm"
WP = GITHUB + "/weekend-planner"
PIO = "https://github.com/piofant/skills"
SP = "https://github.com/obra/superpowers"

TG = {"product": "product", "books": "books", "agents": "AI agents", "research": "research",
      "article": "journal article", "conference": "conference"}

CASES = [
    ("asia-online", "Asia Retail", "2023–2024", "B2C, ~600K users",
     "Relaunch of online grocery delivery: app, payments, order picking, partnerships with Glovo and a bank.",
     "Revenue +103%, orders +67%, churn −24%"),
    ("mts-id", "MTS", "2021–2023", "B2B2C, ~10M users",
     "Single seamless sign-in across the ecosystem's products and a move from a monolith to microservices.",
     "9 flagship products and MTS Bank connected, seamless logins +23%"),
    ("po-sosedstvu", "Po Sosedstvu", "2022–2024", "B2C and B2B, co-founder",
     "Taking an offline store online with an external team and a small budget.",
     "B2B: orders +89%, average check +71%, revenue +58%"),
    ("gazprombank", "Gazprombank", "since 2024", "B2E, 1,000 employees",
     "Internal corporate credit analysis service with an AI agent: from concept and budget approval to launch.",
     "Launched from scratch into production"),
    ("dobster", "Dobster", "2022–2023", "B2C, co-founder",
     "Free help for the elderly and people with disabilities: the platform connects the client, the helper and the donor.",
     "Launched from scratch to production"),
    ("granit", "Concern GRANIT", "2019–2021", "B2G, 50 users",
     "Process automation for a government department; my path from systems analyst to product manager.",
     "Service launched from scratch"),
    ("bolz-tech", "bolz.tech", "2023–2025", "B2B2C, co-founder",
     "An ecosystem of sharing services in one window: rentals without new apps, embedded in partners' apps.",
     "Power banks in production, MIC and Moscow Innovator 2025"),
    ("bolz-dev", "bolz.dev", "2025", "B2B and B2C, co-founder",
     "An MCP connector that lets AI agents find, book and pay for real-world services.",
     "MVP in August 2025"),
]

TAGS = {
    "asia-online": (["foodtech", "e-com"], ["B2C"], ("+103%", "revenue", "#F0C24B")),
    "mts-id": (["telecom", "platform"], ["B2B2C"], ("10M", "users", "#BFD3F2")),
    "po-sosedstvu": (["foodtech", "e-com"], ["B2C", "B2B"], ("+89%", "B2B orders", "#F0C24B")),
    "gazprombank": (["fintech", "AI"], ["B2E"], ("AI agent", "in credit analysis", "#C9DDC5")),
    "dobster": (["charity"], ["B2C"], ("0 → prod", "launched from scratch", "#E8D3E0")),
    "granit": (["public sector"], ["B2G"], ("B2G", "process automation", "#D9DCD4")),
    "bolz-tech": (["startup", "sharing"], ["B2C", "B2B2C"], ("B2B2C", "sharing in one window", "#BFD3F2")),
    "bolz-dev": (["startup", "AI", "AI agents"], ["B2B", "B2C"], ("MCP", "actions for AI agents", "#C9E8D5")),
}

OWN = [
    ("po-sosedstvu", "Po Sosedstvu", "Co-founder and product manager · 2022–2024",
     "Took an offline grocery store online: an online shop with delivery for private and corporate clients. Concept, processes, a team of external contractors, launch on 1C-Bitrix.",
     "B2B: orders +89%, average check +71%, revenue +58%", ("po-sosedstvu.ru", "https://po-sosedstvu.ru/")),
    ("dobster", "Dobster", "Co-founder and product manager · 2022–2023",
     "Free help for the elderly, people with disabilities, veterans and large families: cleaning, repairs, nannies, carers. The platform connects the client, the helper and a donor who pays for the work.",
     "Launched from scratch to production", None),
    ("bolz-dev", "bolz.dev", "Co-founder, CPO · 2025",
     "An MCP connector through which AI agents take real-world actions themselves: they find, book and pay for services without following links.",
     "MVP in August 2025; marketplace and taxi scenarios", ("bolz.dev", "https://bolz.dev/")),
    ("bolz-tech", "bolz.tech", "Co-founder, CPO · 2023–2025",
     "An ecosystem of sharing services in one window: scooters, bikes, cars and power banks inside partners' apps — no installation or sign-up.",
     "Power banks in production; MTS Urent and GetEnergy; MIC and Moscow Innovator 2025", None),
]

TAG_EMOJI = {"product": "💼 ", "AI agents": "🤖 ", "books": "📚 ", "teaching": "🎓 ", "research": "🔬 ", "startup": "🚀 ",
             "journal article": "📄 ", "conference": "🎤 ", "fintech": "🏦 ", "foodtech": "🛒 ", "telecom": "📡 "}
TAG_GROUPS = [
    ("product", ["product", "startup", "AI", "AI agents", "platform", "e-com", "management", "books"]),
    ("industries", ["foodtech", "telecom", "fintech", "charity", "public sector", "sharing"]),
    ("business models", ["B2C", "B2B", "B2B2C", "B2E", "B2G"]),
    ("teaching and research", ["teaching", "journal article", "conference", "research", "AI in management"]),
]

MONTHS_GEN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
MONTHS_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

RESULTS_STRIP = """<section class="results" aria-label="Key results">
<a class="res" href="cases/asia-online.html"><b data-count="103" data-prefix="+" data-suffix="%">+103%</b><span>revenue after an e-commerce relaunch</span></a>
<a class="res" href="cases/mts-id.html"><b data-count="10" data-suffix="M">10M</b><span>MTS ID users across 9 MTS products</span></a>
<a class="res" href="cases/po-sosedstvu.html"><b data-count="89" data-prefix="+" data-suffix="%">+89%</b><span>B2B orders after going online</span></a>
<a class="res" href="timeline.html"><b data-count="4">4</b><span>products launched from scratch</span></a>
</section>"""

STUDY = [
    ("Certificates", [
        ("Scrum.org", "Professional Scrum Product Owner I (PSPO I)", "Scrum product owner certificate: product value, backlog, stakeholder management.", "certificate"),
        ("Cambridge English", "Business English Certificate (BEC)", "Business English, level B1.", "certificate"),
    ]),
    ("Independent assessment", [
        ("Assessty for MTS · April 2022", "Product manager competency assessment",
         "Middle grade. Strongest area: building new products under uncertainty. 17 topics scored 8–10 out of 10: value management, business model and monetisation, key metrics, hypotheses, UX testing, timelines, risks, grooming.", "assessment"),
    ]),
    ("Courses", [
        ("ProductDo · 2025", "Technical knowledge for product managers", "Architecture, APIs, databases and integrations — to speak the same language as engineers.", "course"),
        ("GoPractice · 2025", "SQL simulator for product analytics", "SQL queries for product metrics: funnels, cohorts, retention.", "course"),
        ("Pendo.io · 2024", "AI for Product Management", "How to apply AI in product management work and in the products themselves.", "course"),
        ("Google · 2023", "Fundamentals of digital marketing", "Acquisition channels, search and contextual ads, web analytics.", "course"),
        ("GoPractice · 2022", "Data-driven product management simulator", "Product analytics and metrics on an end-to-end case: from hypothesis to a data-based decision.", "course"),
        ("HSE University · 2014", "Translator in professional communication", "Professional English: translation and business communication.", "programme"),
    ]),
    ("Accelerators and competitions", [
        ("Moscow Innovation Cluster · June–September 2025", "Academy of Innovators accelerator",
         "Completed the programme with my own product bolz.tech, an ecosystem of sharing services: packaging the idea, testing hypotheses, pitching to experts.", "accelerator"),
        ("Moscow · July–August 2025", "Moscow Innovator 2025 competition",
         "Took part with the same product, bolz.tech.", "competition"),
    ]),
]

AGENT_STAGES = [
    (1, "How LLMs work", "Tokens, context, temperature, why a model “hallucinates” and how to write prompts that work reliably.", [], "theory"),
    (2, "Structured output and tools", "The model answers not with text but with JSON following a schema, and decides itself which tool to call: weather, events, search.",
     [("response schemas and the tool-calling loop in Weekend Planner", WP + "/tree/main/weekend_agent/agents")], "practised"),
    (3, "The agent loop", "The agent plans its steps, calls tools, checks the result and decides what to do next. Where you need an agent and where a plain script is enough.",
     [("scout, planner and critic", WP + "/tree/main/weekend_agent/agents")], "practised"),
    (4, "MCP — the tool protocol", "A standard way to connect external tools and data to a model, so you don't rewrite the integration for every agent.",
     [("my own MCP server with four tools", WP + "/blob/main/weekend_agent/mcp_server.py"), ("bolz.dev — an MCP connector for real agent actions", "cases/bolz-dev.html")], "practised"),
    (5, "Multi-agent systems and A2A", "Several agents with different roles negotiate with each other over the Agent-to-Agent protocol.",
     [("Weekend Planner agents talk over A2A", WP + "/tree/main/weekend_agent/a2a")], "practised"),
    (6, "Browser agents", "The agent opens pages, reads them and acts on a website where there is no API.",
     [("the scout's browser tool", WP + "/blob/main/weekend_agent/tools/providers.py")], "practised"),
    (7, "Orchestration and recovery", "What to do when a tool fails, the model returns garbage or loops: retries, fallback models, checks, step limits.",
     [("retries and fallback providers", WP + "/blob/main/weekend_agent/resilience.py")], "practised"),
    (8, "Evals", "How to measure agent quality: a set of cases, automated checks, comparing versions before and after a change.",
     [("32 eval cases", WP + "/tree/main/evals")], "practised"),
    (9, "Agent product metrics", "Agent-native metrics: share of tasks solved without a human, cost and response time, retention and user ratings.",
     [("funnel, retention and ratings in the bot", WP + "/blob/main/weekend_agent/analytics/metrics.py")], "practised"),
    (10, "Memory and RAG", "How an agent remembers the user and relies on its own documents, not just the model's knowledge.", [], "ahead"),
    (11, "Observability and safety", "Traces, logs and the cost of every step; protection against prompt injection and dangerous actions.", [], "ahead"),
    (12, "Agent in production", "Launching to real users: A/B tests, quality monitoring, agent economics.", [], "ahead"),
]

DECKS = [
    ("bolz-dev-pitch.pdf", "dev-cover.jpg", "bolz.dev — an MCP connector for AI agents", "pitch · 2025 · EN · 11 slides",
     "The problem from three sides — services, agents, users — an MCP-based solution, marketplace and taxi scenarios, competitors, go-to-market and roadmap.",
     "cases/bolz-dev.html"),
    ("bolz-tech-pitch.pdf", "tech-cover.jpg", "bolz.tech — an ecosystem of sharing services", "pitch · 2025 · RU · 12 slides",
     "B2B2C model via WebView, user journey, a survey of 200 respondents, architecture, market size, business model, competitors and unit economics.",
     "cases/bolz-tech.html"),
    ("dobster-partnership.pdf", "dobster-cover.jpg", "Dobster — partnership programme", "partnership · 2023 · RU · 8 slides",
     "How the help platform works: recipients, helpers and donors, a non-profit model without fees and what partner companies get.",
     "cases/dobster.html"),
    ("hse-master-thesis.pdf", "hse-cover.jpg", "Evaluating digital transformation projects", "HSE master's · 2020 · RU · 37 slides",
     "Master's thesis defence: how digital transformation projects differ from ordinary investment projects, cases of Rosseti, Russian Railways and Lukoil, four hypotheses and an evaluation model.",
     "blog/magisterskaya-vshe.html"),
    ("it-management-lecture-1.pdf", "lec-cover.jpg", "IT Management. Lecture 1", "teaching · October 2026 · RU · 61 slides",
     "Introduction to IT management: team roles, product life cycle, Waterfall and Agile, DORA metrics, product vs project manager, the path to an AI product manager and a team case.",
     "blog/lekcii-it-menedzhment.html"),
]

CONFS = [
    ("10 September 2026", "Penza", "16th International Scientific and Practical Conference “Development of Modern Science and Education: Current Issues, Achievements and Innovations”",
     "Organisational readiness of Russian companies to bring artificial intelligence into the management system: barriers and directions of development",
     "https://naukaip.ru/wp-content/uploads/2026/09/MK-2774.pdf", "doklad-gotovnost-kompanij", "assets/posts/en/talk-3.png"),
    ("7 September 2026", "Novosibirsk", "110th International Scientific and Practical Conference “Current Issues of Economic Sciences and Modern Management”",
     "Organisational and managerial mechanisms for reducing the risks of using artificial intelligence in bank management",
     "https://sibac.info/conf/economy/cx/430396", "doklad-riski-ii-banki", "assets/posts/en/talk-2.png"),
    ("4 March 2026", "Novosibirsk", "104th International Scientific and Practical Conference “Current Issues of Economic Sciences and Modern Management”",
     "Technological requirements for a company's infrastructure when implementing artificial intelligence",
     "https://sibac.info/conf/economy/civ/403674", "doklad-infrastruktura-ii", "assets/posts/en/talk-1.png"),
]

SKILL_GROUPS = [
    ("Presentations and documents", "📊", [
        ("Dark presentation", "Minimalist slides on a dark background where every headline is a conclusion, not a topic.", PIO),
        ("Investor pitch", "A deck for investors: problem, solution, market, traction, team.", PIO),
        ("Consulting report", "Consulting-style slides, reports and PDFs from plain Markdown.", PIO),
        ("Product case", "A case breakdown from problem statement to a finished presentation.", PIO),
        ("Academic paper", "Defences, research talks and reports following Russian academic standards (GOST).", PIO),
    ]),
    ("Research and analytics", "🔎", [
        ("Deep research", "Research from a blank page to a summary report with sources.", PIO),
        ("Market analysis", "A market through the SCPR and MECE frameworks, TAM/SAM/SOM sizing, RICE prioritisation.", PIO),
        ("NotebookLM notebook", "Working with sources in NotebookLM: notes, podcasts, summaries.", PIO),
        ("Material breakdown", "Breaks a talk or article into layers: facts, meaning, conclusions, what to do.", PIO),
    ]),
    ("Writing", "✍️", [
        ("Natural text editor", "Removes bureaucratic and “machine” phrasing from Russian text.", PIO),
        ("Writing in someone's voice", "Writes in a specific author's style from samples of their texts.", PIO),
        ("Academic writing", "Texts for committees: from a motivation letter to a dissertation defence.", PIO),
    ]),
    ("Personal context", "🗂", [
        ("Telegram context", "Pulls the relevant conversation from Telegram chats into the work.", PIO),
        ("Calendar", "Knows the week's schedule: meetings, times, places.", PIO),
        ("Google Drive search", "Finds the right file on Drive and brings it into the work.", PIO),
        ("Semantic blog search", "Remembers all posts and finds them by meaning, not by keywords.", PIO),
        ("Audio transcription", "Transcribes voice messages and meeting recordings locally.", PIO),
    ]),
    ("Agents and task management", "🤖", [
        ("Finding and installing skills", "Finds a suitable skill and connects it right away.", PIO),
        ("Loop until done", "Repeats a task in a loop until it is finished.", PIO),
        ("Agent team", "Assembles a team of agents with reviewers for a single feature.", PIO),
        ("Structured thinking", "Thinks a question through slowly and step by step when the answer isn't obvious.", PIO),
        ("Expert debate", "Pits several experts' positions against each other until they reach a shared conclusion.", PIO),
    ]),
    ("Development", "🛠", [
        ("Requirements discovery", "Won't let coding start until it's clear what we're building and why.", SP),
        ("Plan and execute", "A step-by-step plan, handing tasks to agents and execution.", SP),
        ("Test-driven development", "Test first, then code; on failure it looks for the cause, not the symptom.", SP),
        ("Code review", "Sends code for review, works through comments and gets the branch merged.", SP),
        ("Interface design", "Interfaces with a deliberate visual approach instead of a template.", "https://github.com/anthropics/skills"),
        ("Creating skills", "Helps write a new skill and understand existing ones.", SP),
    ]),
]

TOOLKIT = [
    ("User research", [
        ("CustDev and in-depth interviews", "Validating the problem before development.", "Gazprombank, MTS ID, Asia Online, a survey of 200 bolz.tech users, interviews for my dissertation"),
        ("Jobs To Be Done", "I define which “job” the user hires the product for.", ""),
        ("UX testing", "I watch where users stumble before release.", ""),
    ]),
    ("Prioritisation and strategy", [
        ("ICE and RICE", "I compare hypotheses by impact, confidence and effort.", ""),
        ("Roadmap and backlog", "I link business goals to the release plan.", "every product, from GRANIT to Gazprombank"),
        ("Product concept and budget", "I defend the product to stakeholders before development starts.", "Gazprombank, MTS ID"),
    ]),
    ("Metrics and experiments", [
        ("Product metrics and funnels", "Conversion, churn, retention, share of orders from the app.", "Asia Online: +103% revenue, −24% churn"),
        ("Unit economics", "CAC, LTV, average check, channel payback.", "“first 100 paying users” and PMF at bolz.tech"),
        ("A/B tests", "I test changes on part of the audience.", "GoPractice course, the “Experiments and economics” lecture"),
        ("SQL", "I pull data for metrics myself.", "GoPractice simulator"),
    ]),
    ("Processes and requirements", [
        ("BPMN", "I describe business processes as-is and to-be.", "Concern GRANIT, Po Sosedstvu"),
        ("User stories and specifications", "I set tasks for engineering so they can be verified.", "GRANIT, MTS ID"),
        ("Agile and team KPIs", "I set the team's rhythm and measurable goals.", "e-com restructuring at Asia Retail"),
    ]),
    ("AI and agents", [
        ("LLM agents", "The agent loop: plan, call tools, check, retry.", "Weekend Planner, the AI-agent service at the bank"),
        ("MCP and A2A", "Protocols for tools and agent communication.", "Weekend Planner's MCP server, bolz.dev"),
        ("Evals", "I evaluate an agent by the result of its action, not by its text.", "32 Weekend Planner eval cases, bolz.dev"),
        ("Claude Code, Cursor, LLM APIs", "I build prototypes myself: OpenAI-compatible models, GigaChat.", "Weekend Planner, this website"),
        ("n8n", "No-code automations.", ""),
    ]),
    ("Services", [
        ("Figma and Miro", "Mockups, CJM, process diagrams.", "every product"),
        ("Git and GitHub", "Prototype code and portfolio.", "github.com/astro090-pm"),
        ("1C-Bitrix, Bitrix24, Yandex Metrica", "Launching websites and their analytics.", "Po Sosedstvu, Lighthouse Technologies"),
    ]),
]

CONST_PROJECTS = [
    ("Gazprombank", ["Gazprombank", "bank"]), ("MTS ID", ["MTS ID"]), ("Asia Online", ["Asia"]), ("GRANIT", ["GRANIT"]),
    ("Po Sosedstvu", ["Po Sosedstvu"]), ("bolz.tech", ["bolz.tech"]), ("bolz.dev", ["bolz.dev"]),
    ("Weekend Planner", ["Weekend Planner"]), ("Dissertation and courses", ["dissertation", "GoPractice", "lecture"]), ("Lighthouse", ["Lighthouse"]),
]

TIMELINE = [
    ("2008–2015", "education", "MPEI, master's degree", "Electrical engineering, electromechanics and electrotechnology.", "study.html"),
    ("2014", "education", "HSE University: “Translator in professional communication”", "Professional English.", "study.html"),
    ("July 2014", "work", "Electrical machine test engineer — Agregat-Privod", "First job: an electrical machines laboratory.", ""),
    ("December 2014", "work", "Electrical equipment repair engineer — Mosenergo", "Maintaining power plant equipment up to 10 kV.", ""),
    ("April 2017", "work", "Lead sales engineer — Lighthouse Technologies", "Industrial equipment: tenders, technical and commercial proposals, clients.", ""),
    ("August 2018", "work", "Business development manager — Lighthouse Technologies", "First product experience: built the company website from scratch, rolled out Bitrix24.", "blog/pervyj-sajt-lighthouse.html"),
    ("2018–2021", "education", "HSE University, master's in Corporate Finance", "Thesis on evaluating digital transformation projects.", "blog/magisterskaya-vshe.html"),
    ("August 2019", "work", "Lead systems analyst — Concern GRANIT", "BPMN, requirements, interface prototypes, testing.", "cases/granit.html"),
    ("November 2020", "work", "Product manager — Concern GRANIT", "Automation service for a government department (B2G) from scratch to production.", "cases/granit.html"),
    ("October 2021", "work", "Product manager, MTS ID — MTS", "Seamless sign-in across 9 flagship products for ~10M users, seamless logins +23%.", "cases/mts-id.html"),
    ("2022", "education", "GoPractice: data-driven product management simulator", "Product analytics and metrics.", "study.html"),
    ("April 2022", "achievement", "Independent Assessty assessment at MTS — Middle grade", "Strongest area: building new products under uncertainty.", "blog/ocenka-mts.html"),
    ("August 2022", "project", "Co-founder of Po Sosedstvu", "Took an offline store online: B2B orders +89%, average check +71%.", "cases/po-sosedstvu.html"),
    ("November 2022", "project", "Co-founder of Dobster", "A charity platform: from idea to production.", "cases/dobster.html"),
    ("2023", "education", "Google: fundamentals of digital marketing", "Acquisition channels and web analytics.", "study.html"),
    ("April 2023", "work", "Head of E-commerce — Asia Retail", "Relaunch of Asia Online: revenue +103%, orders +67%, churn −24%.", "cases/asia-online.html"),
    ("October 2023", "project", "Co-founder and CPO of bolz.tech", "An ecosystem of sharing services in one window; power bank sharing in production by December 2024.", "cases/bolz-tech.html"),
    ("April 2024", "work", "Senior product manager — Gazprombank", "Corporate credit analysis service with an AI agent: from scratch to production.", "cases/gazprombank.html"),
    ("2024", "education", "Pendo.io: AI for Product Management", "How to apply AI in product work and in products.", "study.html"),
    ("2024", "research", "Started a PhD at RANEPA", "Topic: using AI to improve a company's management system.", "research.html"),
    ("May 2025", "research", "First peer-reviewed article", "“Characteristic features of AI use in the management of Russian companies”.", "blog/statya-ii-v-menedzhmente.html"),
    ("June–September 2025", "achievement", "MIC Academy of Innovators accelerator and the Moscow Innovator 2025 competition", "With the bolz.tech project.", "blog/bolz-akselerator.html"),
    ("2025", "education", "ProductDo and GoPractice: technical foundations and SQL for PMs", "Architecture, APIs, SQL analytics.", "study.html"),
    ("August 2025", "project", "Co-founder and CPO of bolz.dev — MVP", "An MCP connector through which AI agents take real-world actions.", "cases/bolz-dev.html"),
    ("September 2025", "research", "Second peer-reviewed article", "“Current trends in the use of AI in corporate governance”.", "blog/statya-tendencii-ii.html"),
    ("December 2025", "research", "Third peer-reviewed article", "“Risks and limitations of using AI in company management”.", "blog/statya-riski-ii.html"),
    ("March 2026", "research", "First talk at an international conference", "Infrastructure requirements for implementing AI, Novosibirsk.", "blog/doklad-infrastruktura-ii.html"),
    ("September 2026", "research", "Two more talks: Novosibirsk and Penza", "Reducing AI risks in banks; companies' organisational readiness for AI.", "conferences.html"),
    ("October 2026", "teaching", "Started teaching an IT Management course at a university", "Seven lectures for first-year students, team cases and a final project.", "blog/lekcii-it-menedzhment.html"),
    ("October 2026", "project", "AI prototype: Weekend Planner", "A2A agents, my own MCP server, a browser agent, 32 eval cases.", "projects.html"),
    ("October 2026", "research", "Interview series for the dissertation case study", "How AI is built into the management of a large bank.", "blog/intervyu-ii-v-banke.html"),
]
TL_TYPES = [("work", "💼"), ("project", "🚀"), ("research", "🔬"), ("education", "🎓"), ("teaching", "🧑‍🏫"), ("achievement", "🏅")]

GANTT = [
    ("Work", "#7C9BEA", [
        ("Agregat-Privod", 2014.5, 2014.9, ""), ("Mosenergo", 2014.95, 2015.9, ""),
        ("Lighthouse", 2017.25, 2019.2, "blog/pervyj-sajt-lighthouse.html"),
        ("Concern GRANIT", 2019.6, 2021.8, "cases/granit.html"), ("MTS", 2021.8, 2023.4, "cases/mts-id.html"),
        ("Asia Retail", 2023.3, 2024.25, "cases/asia-online.html"), ("Gazprombank", 2024.3, 2026.85, "cases/gazprombank.html"),
    ]),
    ("Own projects", "#E8956A", [
        ("Po Sosedstvu", 2022.6, 2024.9, "cases/po-sosedstvu.html"), ("Dobster", 2022.85, 2023.8, "cases/dobster.html"),
        ("bolz.tech", 2023.8, 2025.8, "cases/bolz-tech.html"), ("bolz.dev", 2025.6, 2026.85, "cases/bolz-dev.html"),
        ("Planner", 2026.75, 2026.85, "projects.html"),
    ]),
    ("Education", "#9BB8A4", [
        ("MPEI", 2008.7, 2015.5, "study.html"), ("HSE", 2018.7, 2021.5, "blog/magisterskaya-vshe.html"),
        ("RANEPA, PhD", 2024.7, 2027.5, "research.html"),
    ]),
    ("Research and teaching", "#A98BEA", [
        ("3 articles", 2025.4, 2025.95, "research.html"), ("3 talks", 2026.15, 2026.72, "conferences.html"),
        ("University course", 2026.76, 2026.9, "blog/lekcii-it-menedzhment.html"),
    ]),
]

GEO = [
    ("Moscow", 37.6, 55.75, "Work at MTS, GRANIT, Gazprombank; MPEI, HSE, RANEPA; my own startups", "timeline.html"),
    ("Bishkek", 74.6, 42.87, "Asia Retail: e-commerce relaunch, +103% revenue", "cases/asia-online.html"),
    ("Novosibirsk", 82.9, 55.0, "Two talks at international conferences, 2026", "conferences.html"),
    ("Penza", 45.0, 53.2, "A talk at an international conference, 2026", "conferences.html"),
]

MEDIA_KINDS = [("podcasts", "🎧 Podcasts"), ("videos", "🎬 Lectures and videos"), ("reading", "📡 Who I read")]

PATCH = {k: v for k, v in globals().items() if k.isupper() and k not in ("HERE", "GITHUB", "WP", "PIO", "SP")}
PATCH["BOOKS_LINK"] = '<a href="{up}books.html">📚 books</a>'
PATCH["MEDIA_LINK"] = ""
PATCH["MONTHS_NOM"] = {m.lower(): i + 1 for i, m in enumerate(MONTHS_GEN)}


def year_stats(B):
    def stats(posts, year):
        ys = [p for p in posts if p["date"].startswith(str(year))]
        tag = lambda t: sum(t in p["tags"] for p in ys)
        courses = sum(str(year) in org for title, rows in STUDY for org, *_ in rows
                      if title in ("Courses", "Accelerators and competitions"))
        pl = lambda n, one, many: one if n == 1 else many
        rows = [
            (pl(tag("conference"), "conference talk", "conference talks"), tag("conference"), "conferences.html"),
            (pl(tag("journal article"), "peer-reviewed article", "peer-reviewed articles"), tag("journal article"), "research.html"),
            (pl(courses, "course", "courses and programmes"), courses, "study.html"),
            (pl(tag("books"), "book", "books"), tag("books"), "books.html"),
            (pl(len(ys), "post", "posts"), len(ys), "blog/"),
        ]
        if year == 2026:
            rows.insert(0, ("university course I teach", 1, "blog/lekcii-it-menedzhment.html"))
            rows.insert(1, ("open-source AI prototype", 1, "projects.html"))
        if year == 2025:
            rows.insert(0, ("startups: bolz.tech and bolz.dev", 2, "projects.html"))
        return [r for r in rows if r[1]]
    return stats


MOON = '<svg class="i-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg><svg class="i-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
LOUPE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'


def layout(ctx):
    S = ctx["SITE_URL"]

    def lay(title, description, body, path, depth=0):
        up = "../" * depth
        root = "../" * (depth + 1)
        ru_path = path or ""
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{S}/en/{path}">
<link rel="alternate" hreflang="ru" href="{S}/{ru_path}">
<link rel="alternate" hreflang="en" href="{S}/en/{path}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{S}/en/{path}">
<meta property="og:site_name" content="Roman Ponurov">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="{S}/assets/og-en.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Roman Ponurov, product manager: +103% e-com revenue, 10M MTS ID users, 4 products launched from scratch">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{S}/assets/og-en.png">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{ctx['FONTS']}">
<link rel="stylesheet" href="{up}assets/style.css?v={ctx['CSS_V']}">
<script>try{{const t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;}}catch(e){{}}</script>
<script src="{up}assets/site.js?v={ctx['JS_V']}" defer data-root="{up}"></script>
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{up}index.html"><img class="avatar avatar-sm" src="{up}assets/avatar-sm.jpg" width="34" height="34" alt="">Roman Ponurov</a>
<nav class="nav" aria-label="Sections">
<details class="menu"><summary>product</summary><div class="menu-list"><a href="{up}about.html">👋 about me</a><a href="{up}now.html">⏱ now</a><a href="{up}timeline.html">🗓 timeline</a><a href="{up}assets/Ponurov_Roman_CV.pdf" target="_blank" rel="noopener">📄 CV (PDF, Russian)</a><a href="{up}cases/index.html">📁 case portfolio</a><a href="{up}decks.html">🎞 decks</a><a href="{up}tools.html">🧰 toolkit</a></div></details>
<a href="{up}projects.html">projects</a>
<details class="menu"><summary>knowledge</summary><div class="menu-list"><a href="{up}research.html">🔬 research</a><a href="{up}conferences.html">🎤 conferences</a><a href="{up}study.html">🎓 education</a>{PATCH["BOOKS_LINK"].format(up=up)}</div></details>
<details class="menu"><summary>AI</summary><div class="menu-list"><a href="{up}agents.html">🤖 AI agents</a><a href="{up}skills.html">🧰 AI skills</a></div></details>
<a href="{up}blog/index.html">posts</a>
<a href="{up}tags/index.html">tags</a>
</nav>
<span class="tools">
<a class="icon-btn lang" href="{root}{ru_path}" title="Russian version" hreflang="ru">RU</a>
<button type="button" class="icon-btn" id="search-open" aria-label="Search the site" title="Search (/)">{LOUPE}</button>
<button type="button" class="icon-btn" id="theme-toggle" aria-label="Toggle dark theme" title="Dark theme">{MOON}</button>
</span>
<script>
document.addEventListener('click', e => document.querySelectorAll('details.menu[open]').forEach(d => {{ if (!d.contains(e.target)) d.open = false; }}));
document.querySelectorAll('details.menu').forEach(d => d.addEventListener('toggle', () => {{ if (d.open) document.querySelectorAll('details.menu[open]').forEach(o => {{ if (o !== d) o.open = false; }}); }}));
</script>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap foot">
© 2026 Roman Ponurov · <a href="mailto:ponurov.roman@yandex.ru">email</a> · <a href="https://t.me/astro090">telegram</a> · <a href="https://www.linkedin.com/in/roman-ponurov-bb3b81a6/">linkedin</a> · all rights reserved
</div></footer>
</body>
</html>
"""
    return lay


# ---------- перевод оставшихся строк (тексты внутри функций build.py) ----------
_TR_FILE = HERE / "i18n_en" / "ui.json"
TR = json.loads(_TR_FILE.read_text(encoding="utf-8")) if _TR_FILE.exists() else {}
RAW = TR.pop("__raw__", [])  # [[русский HTML-фрагмент, английский], ...] — для предложений со ссылками внутри
CYR = re.compile(r"[А-Яа-яЁё]")
HEAT = dict(zip("ЯФМАИСОНД", "JFMAJSOND"))


def _tr(s):
    if not CYR.search(s):
        return s
    core = s.strip()
    if core in TR:
        return s[: len(s) - len(s.lstrip())] + TR[core] + s[len(s.rstrip()):]
    return s


RX = [
    (r" — кейс Романа Понурова", " — a case by Roman Ponurov"),
    (r" — Роман Понуров", " — Roman Ponurov"),
    (r">(\d+) мин<", r">\1 min<"),
    (r"Где применял: ", "Used at: "),
    (r"Первый слайд: ", "First slide: "),
    (r"Посты и кейсы с меткой «([^»]+)»\.", r"Posts and cases tagged “\1”."),
    (r"Посты — страница (\d+)", r"Posts — page \1"),
    (r"страница (\d+) / (\d+)", r"page \1 / \2"),
    (r"Пройдено этапов: (\d+) из (\d+)", r"Stages completed: \1 of \2"),
    (r"Города: ", "Cities: "),
    (r"Рабочий набор из (\d+) ИИ-скиллов продакта", r"A working set of \1 AI skills for a product manager"),
]


def translate(h):
    for ru, en in RAW:
        h = h.replace(ru, en)
    for a, b in RX:
        h = re.sub(a, b, h)
    h = re.sub(r"<em>([ЯФМАИСОНД])</em>", lambda m: f"<em>{HEAT[m.group(1)]}</em>", h)
    parts = re.split(r"(<(?:script|style)\b.*?</(?:script|style)>)", h, flags=re.S)
    for i in range(0, len(parts), 2):
        p = parts[i]
        p = re.sub(r">([^<]+)<", lambda m: ">" + _tr(m.group(1)) + "<", p)
        p = re.sub(r'\b(title|alt|aria-label|content|placeholder)="([^"]*)"', lambda m: f'{m.group(1)}="{_tr(m.group(2))}"', p)
        parts[i] = p
    return "".join(parts)

# соответствие тегов: русский → английский (для переключателя языка на страницах тегов)
TAG_RU_EN = {"продакт": "product", "стартап": "startup", "ИИ-агенты": "AI agents", "менеджмент": "management", "книги": "books",
             "платформа": "platform", "фудтех": "foodtech", "телеком": "telecom", "финтех": "fintech",
             "благотворительность": "charity", "госсектор": "public sector", "шеринг": "sharing", "преподавание": "teaching",
             "научная статья": "journal article", "конференция": "conference", "исследования": "research",
             "ИИ в управлении": "AI in management"}
