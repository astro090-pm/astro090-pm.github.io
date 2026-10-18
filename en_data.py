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
    ("bolz-dev", "bolz.dev", "Co-founder, CPO · Dubai · 2025",
     "An MCP connector through which AI agents take real-world actions themselves: they find, book and pay for services without following links.",
     "MVP in August 2025; marketplace and taxi scenarios", ("bolz.dev", "https://bolz.dev/")),
    ("bolz-tech", "bolz.tech", "Co-founder, CPO · Dubai · 2023–2025",
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
        ("Cambridge English · October 2021", "Business English Certificate Preliminary (BEC)", "Business English, level B1: exam passed (Pass), overall score 146 on the Cambridge English Scale. Reading 152, writing 142, listening 139, speaking 151.", "certificate",
         {"img": "assets/certs/cambridge-bec-2021.jpg", "verify": "https://www.cambridgeenglish.org/verifiers", "label": "Statement of results"}),
    ]),
    ("Independent assessment", [
        ("Assessty for MTS · April 2022", "Product manager competency assessment",
         "Middle grade. Strongest area: building new products under uncertainty. 17 topics scored 8–10 out of 10: value management, business model and monetisation, key metrics, hypotheses, UX testing, timelines, risks, grooming.", "assessment"),
    ]),
    ("Courses", [
        ("ProductDo · 2025", "Technical knowledge for product managers", "Architecture, APIs, databases and integrations — to speak the same language as engineers.", "course"),
        ("GoPractice · 2025", "SQL simulator for product analytics", "SQL queries for product metrics: funnels, cohorts, retention. 402 practical assignments; certificate dated 29 April 2025.", "course",
         {"img": "assets/certs/gopractice-sql-2025.jpg", "verify": "https://gopractice.ru/course/sql/certificate/gq9lmuju"}),
        ("Pendo.io · 2024", "AI for Product Management", "How to apply AI in product management work and in the products themselves. A course by Pendo with Google Cloud and Mind the Product — completed.", "course",
         {"img": "assets/certs/pendo-ai-pm-2024.png", "label": "Course badge"}),
        ("Google · 2023", "Fundamentals of digital marketing", "Acquisition channels, search and contextual ads, web analytics. Exam passed on 23 July 2023; the programme is endorsed by IAB Europe.", "course",
         {"img": "assets/certs/google-marketing-2023.jpg", "verify": "https://learndigital.withgoogle.com/link/1ol24okmw3k"}),
        ("GoPractice · 2022", "Data-driven product management simulator", "Product analytics and metrics on an end-to-end case: from hypothesis to a data-based decision. 413 practical assignments, 83% correct answers; certificate dated 12 August 2022.", "course",
         {"img": "assets/certs/gopractice-pm-2022.jpg", "verify": "https://gopractice.ru/course/pm/certificate/rr3mnnve"}),
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
    ("10 September 2026", "online", "16th International Scientific and Practical Conference “Development of Modern Science and Education: Current Issues, Achievements and Innovations”",
     "Organisational readiness of Russian companies to bring artificial intelligence into the management system: barriers and directions of development",
     "https://naukaip.ru/wp-content/uploads/2026/09/MK-2774.pdf", "doklad-gotovnost-kompanij", "assets/posts/en/talk-3.png"),
    ("7 September 2026", "online", "110th International Scientific and Practical Conference “Current Issues of Economic Sciences and Modern Management”",
     "Organisational and managerial mechanisms for reducing the risks of using artificial intelligence in bank management",
     "https://sibac.info/conf/economy/cx/430396", "doklad-riski-ii-banki", "assets/posts/en/talk-2.png"),
    ("4 March 2026", "online", "104th International Scientific and Practical Conference “Current Issues of Economic Sciences and Modern Management”",
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
        ("Jobs To Be Done", "I define which “job” the user hires the product for.", "Dobster, bolz.tech, bolz.dev, Weekend Planner"),
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
    ("October 2023", "project", "Co-founder and CPO of bolz.tech, Dubai", "An ecosystem of sharing services in one window; power bank sharing in production by December 2024.", "cases/bolz-tech.html"),
    ("April 2024", "work", "Senior product manager — Gazprombank", "Corporate credit analysis service with an AI agent: from scratch to production.", "cases/gazprombank.html"),
    ("2024", "education", "Pendo.io: AI for Product Management", "How to apply AI in product work and in products.", "study.html"),
    ("2024", "research", "Started a PhD at RANEPA", "Topic: using AI to improve a company's management system.", "research.html"),
    ("May 2025", "research", "First peer-reviewed article", "“Characteristic features of AI use in the management of Russian companies”.", "blog/statya-ii-v-menedzhmente.html"),
    ("June–September 2025", "achievement", "MIC Academy of Innovators accelerator and the Moscow Innovator 2025 competition", "With the bolz.tech project.", "blog/bolz-akselerator.html"),
    ("2025", "education", "ProductDo and GoPractice: technical foundations and SQL for PMs", "Architecture, APIs, SQL analytics.", "study.html"),
    ("August 2025", "project", "Co-founder and CPO of bolz.dev, Dubai — MVP", "An MCP connector through which AI agents take real-world actions.", "cases/bolz-dev.html"),
    ("September 2025", "research", "Second peer-reviewed article", "“Current trends in the use of AI in corporate governance”.", "blog/statya-tendencii-ii.html"),
    ("December 2025", "research", "Third peer-reviewed article", "“Risks and limitations of using AI in company management”.", "blog/statya-riski-ii.html"),
    ("March 2026", "research", "First talk at an international conference", "Infrastructure requirements for implementing AI, online.", "blog/doklad-infrastruktura-ii.html"),
    ("September 2026", "research", "Two more online talks at international conferences", "Reducing AI risks in banks; companies' organisational readiness for AI.", "conferences.html"),
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
    ("Moscow", 37.6, 55.75, "Work at MTS, GRANIT, Gazprombank; MPEI, HSE, RANEPA; Po Sosedstvu and Dobster", "timeline.html"),
    ("Dubai", 55.27, 25.2, "My own startups bolz.tech and bolz.dev, 2023–2025", "cases/bolz-tech.html"),
    ("Bishkek", 74.6, 42.87, "Asia Retail: e-commerce relaunch, +103% revenue", "cases/asia-online.html"),
]

CERT_LBL = {"cert": "Certificate", "verify": "verify", "alt": "Certificate"}

MEDIA_KINDS = [("podcasts", "🎧 Podcasts"), ("videos", "🎬 Lectures and videos"), ("reading", "📡 Who I read")]

PROJECTS = [
    ("🗓", "#E6EDF9", "2026.10", "TG BOT / AI AGENTS", "Weekend Planner",
     "A Telegram bot that builds an hour-by-hour weekend plan: weather, events, places, budget and children's ages.",
     ["3 agents over A2A", "32 eval cases", "55 tests", "prototype"],
     [("Code on GitHub", GITHUB + "/weekend-planner"), ("Roadmap", "#roadmap"), ("Architecture", "#architecture"), ("My path into AI agents", "agents.html")],
     "Planning a weekend means half an hour of switching between event listings, maps and the forecast. I built a bot that does it in a minute. The model only chooses options; names, prices and times are filled in by code, so the plan doesn't invent places that don't exist."),
    ("🔌", "#C9E8D5", "2025.08", "MCP / AI AGENTS · DUBAI", "bolz.dev",
     "An MCP connector through which AI agents find, book and pay for real-world services themselves.",
     ["MVP in August 2025", "co-founder, CPO"],
     [("Website", "https://bolz.dev/"), ("Case", "cases/bolz-dev.html"), ("Pitch, PDF", "assets/decks/bolz-dev-pitch.pdf")],
     "AI agents can search and advise, but to pay the user still has to follow a link. We gave agents “find, book, pay” actions. We count success as a completed action — a paid order — not a nice-looking model answer."),
    ("🛴", "#BFD3F2", "2023.10", "B2B2C / SHARING · DUBAI", "bolz.tech",
     "All sharing services in one window — inside partners' apps, with no installation or sign-up.",
     ["power banks in production", "survey of 200 users", "MIC and Moscow Innovator 2025"],
     [("Case", "cases/bolz-tech.html"), ("Pitch, PDF (Russian)", "assets/decks/bolz-tech-pitch.pdf"), ("About the accelerator", "blog/bolz-akselerator.html")],
     "The scooter whose app you have is often not nearby. We embedded sharing into other apps via WebView: the card is linked once for all services. Then we noticed users increasingly come through AI assistants — that's how bolz.dev appeared."),
    ("🤝", "#E8D3E0", "2022.11", "WEB / CHARITY", "Dobster",
     "Free help at home for the elderly, people with disabilities, veterans and large families.",
     ["from scratch to production", "3-sided deal", "no fees"],
     [("Case", "cases/dobster.html"), ("Partnership programme, PDF (Russian)", "assets/decks/dobster-partnership.pdf")],
     "Those who need help most find it hardest to get. The platform connects the client, the helper and a donor who pays for the work. I designed the client's journey so an elderly person could complete it: verification via Gosuslugi, a request, a review."),
    ("🛒", "#F6DFA4", "2022.08", "E-COM / FOODTECH", "Po Sosedstvu",
     "An online shop for Belarusian groceries with delivery for private and corporate clients.",
     ["B2B: orders +89%", "average check +71%", "revenue +58%"],
     [("Website", "https://po-sosedstvu.ru/"), ("Case", "cases/po-sosedstvu.html")],
     "An offline store needed an online channel on a small budget. We launched the shop on 1C-Bitrix with a team of external contractors and a separate account area for companies — the site is still running."),
]
PROJECTS_TEXT = {"title": "Projects", "intro": "Things I launched myself — as a co-founder or author: startups, a social project and AI prototypes. My work at companies is in the <a href=\"cases/index.html\">case portfolio</a>.",
                 "desc": "Roman Ponurov's own projects: bolz.dev, bolz.tech, Dobster, Po Sosedstvu and open-source AI prototypes.",
                 "more": "see more",
                 "links": [("cases/index.html", "Cases", "product problems at my main jobs and how I solved them", "linear-gradient(135deg,#5BC0F8,#3D8BEA)"),
                           ("agents.html", "AI agents", "my path from theory to practice: LLMs, MCP, A2A, evals", "linear-gradient(135deg,#F4A259,#E0603A)")]}

AGENT = {"q": "who is Roman?", "label": "Answers about Roman", "lines": [
    ("builds a service with an AI agent at a bank", "cases/gazprombank.html"),
    ("is writing a PhD on AI in company management", "research.html"),
    ("teaches IT management to first-year students", "blog/lekcii-it-menedzhment.html"),
    ("built an open-source agentic Telegram bot", "projects.html"),
    ("co-built an MCP connector for AI agents in Dubai", "cases/bolz-dev.html"),
    ("launched 4 products from scratch", "cases/index.html"),
]}
NOW_CARD = {"title": "Now", "updated": "updated 16 October 2026", "more": "more", "items": [
    ("🧑‍💼", "Work", "developing a credit analysis service with an AI agent at Gazprombank", "cases/gazprombank.html"),
    ("🎓", "Teaching", "an IT Management course, lectures on Tuesdays until 24 November", "blog/lekcii-it-menedzhment.html"),
    ("🔬", "Research", "finished a series of interviews for my dissertation case study", "blog/intervyu-ii-v-banke.html"),
    ("🤖", "Building", "Weekend Planner, an agentic Telegram bot", "projects.html"),
]}

ORBIT = [("product", "cases/index.html"), ("AI agents", "agents.html"), ("research", "research.html"),
         ("lectures", "blog/lekcii-it-menedzhment.html"), ("startups", "projects.html")]
CAREER_LBL = {"now": "now", "aria": "Path by year", "present": "now", "sections": "Site sections", "then": "2014: test bench engineer"}

ROUTER = {"title": "Who are you?", "aria": "Route through the site", "routes": [
    ("hr", "I'm hiring", "In 2 minutes: results, cases and how to work with me.", [
        ("CV, PDF", "assets/Ponurov_Roman_CV_EN.pdf"), ("Case portfolio", "cases/index.html"), ("How to work with me", "about.html")]),
    ("student", "I'm a student", "The IT management course, lecture slides and book reviews.", [
        ("About the IT management course", "blog/lekcii-it-menedzhment.html"), ("Lecture 1, PDF", "assets/decks/it-management-lecture-1.pdf"), ("Books and reviews", "books.html")]),
    ("peer", "I'm a colleague", "AI agents in practice, research and open-source code.", [
        ("My path in AI agents", "agents.html"), ("Research", "research.html"), ("Projects and code", "projects.html")]),
]}

METRIC_TREES = {
    "asia-online": ("Revenue", "+103%", "", [
        ("Number of orders", "+67%", "", [
            ("New users", "+44%", "Glovo integration, storefront in the M-Bank app, app redesign", []),
            ("Active customers", "+31%", "", []),
            ("Customer churn", "−24%", "", []),
            ("Purchase conversion", "+17%", "online payment, redesign, ordering via the call center", []),
            ("Order cancellations", "−15%", "the Picker app, up-to-date prices and stock", []),
        ]),
        ("Average order value", "revenue grew faster than orders", "assortment +2,000 SKUs", []),
    ]),
    "mts-id": ("Seamless logins", "+23%", "the platform's key metric — measured across the whole ecosystem", [
        ("Connected products", "9 + MTS Bank", "integrations with consumer teams; 2 more external products together with MTS Pay", []),
        ("Seamless authorizations", "+7%", "", []),
        ("Readiness to scale", "", "moving from a monolith to microservices", []),
    ]),
}
TREE_LBL = {"h": "Metric tree", "note": "How the main result breaks down into metrics and which actions moved them. Numbers come from the Results section.",
            "lever": "levers"}

CASE_FILTER = {
    "intro": "Products I launched and grew: in my day jobs — in banking, telecom, retail and the public sector — and as a co-founder of my own projects. Pick a task similar to yours.",
    "aria": "Task type", "all": "all",
    "tasks": [("zero", "launch from scratch"), ("growth", "growth and relaunch"), ("platform", "platform and integrations"), ("ai", "AI in the product")],
    "own": "own project",
}

ROADMAP = {
    "title": "Roadmap: Weekend Planner",
    "note": "What is done, what I'm working on, what's next and what I dropped — and why.",
    "cols": [
        ("done", "Done · MVP in 3 days", [
            "3 agents over A2A: orchestrator, scout, critic",
            "My own MCP server and a browser agent",
            "32 eval cases and model comparison",
            "Prices, addresses and times in the plan come from code, not the model",
            "Events and metrics: activation, 👍, return 7d"]),
        ("now", "Now", [
            "First users: the goal is 20–50 people who received a plan",
            "A separate link per channel to see where people come from",
            "Plans with 👎 → new eval case → fix → re-run"]),
        ("next", "Next", [
            "Streaming and caching: answers in seconds, not tens of seconds",
            "Personalization based on rating history",
            "Online evals on real conversations",
            "Tracing by stage and alerts on rising fallbacks",
            "A/B tests of prompts and models with guardrail metrics",
            "Ticket purchase as a tool — with user confirmation"]),
    ],
    "cut_h": "Dropped",
    "cut": [
        ("One agent for everything", "where the path is known, predictable code is better: each stage can be measured and fixed separately"),
        ("The model writes prices and addresses", "it picks ids and code fills in the facts, so the plan can't invent places"),
        ("The official A2A SDK", "~150 readable lines were enough for a prototype; the contract matches the spec"),
        ("An LLM critic that triggers fixes", "LLM review can be wrong, so it only advises; code checks do the blocking"),
        ("Lock-in to one provider", "the model is switched with one setting, and evals compare models from different companies")],
    "jtbd": ("User job", "When on Friday I'm thinking about what to do with my kid at the weekend, I want an hour-by-hour plan that accounts for weather and budget in a minute, so that I don't spend half an hour switching between listings, maps and the forecast."),
    "us_h": "User stories",
    "us_lbl": {"ac": "Acceptance criteria", "m": "Metric", "done": "done", "next": "next"},
    "stories": [
        ("done", "As a user whose plan didn't fit, I want one button for another option or a cheaper one, so that I don't have to write the request again.",
         ["every plan has “🔁 Another option” and “💸 Cheaper” buttons", "a change can also be written as plain text", "the revised plan passes the same checks as the first one"],
         "refine rate — revisions per delivered plan"),
        ("done", "As a parent, I want the bot to account for my child's age and the weather, so that we don't end up somewhere a child isn't allowed, or in the rain.",
         ["only age-appropriate items get into the plan", "in rain — only indoor places", "code checks this, not the model; there are eval cases for kids and rain"],
         "👍 / (👍 + 👎)"),
        ("done", "As a user, I want a reminder on Friday, so that I plan the weekend in time.",
         ["only subscribers get the reminder", "it is sent on Friday at lunchtime — when people think about the weekend"],
         "reminder CTR and return 7d"),
        ("next", "As a user, I want to see the progress and get a plan in seconds, so that I don't wait in silence.",
         ["progress is shown by stage", "time to plan — seconds instead of tens of seconds"],
         "time to value — median from /start to the first plan"),
        ("next", "As a regular user, I want the bot to take my past ratings into account, so that plans fit better.",
         ["categories the person liked are taken into account"],
         "👍 / (👍 + 👎)"),
    ],
    "src": "More in the repository docs",
    "src_url": GITHUB + "/weekend-planner/blob/main/docs/ARCHITECTURE.md",
}

RES_LBL = {"down": "lower is better", "table": "Show as a table", "aria": "Results in numbers"}

EXPERIMENTS = {
    "asia-online": {"intro": "There were many hypotheses, and not all of them held up.", "cards": [
        {"status": "no", "hyp": "If delivery gets faster, the number of orders will grow.", "metric": "number of orders",
         "result": "no significant growth", "decision": ""},
    ]},
}
EXP_LBL = {"h": "What didn't work", "hyp": "Hypothesis", "metric": "Metric", "result": "Result", "decision": "Decision",
           "yes": "confirmed", "no": "not confirmed", "tag": "experiment"}

JTBD = {
    "dobster": [
        ("👵", "Recipient", "I need help around the house but can't pay for it", "to leave one simple request", "I get help for free without searching for someone myself"),
        ("🙋", "Helper", "I want to help people nearby", "to see specific tasks from verified recipients", "I help those who really need it"),
        ("💳", "Donor", "I donate money", "to pay for a specific task and get a report", "I see where the money went"),
    ],
    "bolz-tech": [
        ("🛴", "User", "there is no scooter or power bank nearby from the service whose app I have", "to rent from another one without a new install or sign-up", "I don't waste time on yet another app"),
        ("🔋", "Sharing service", "the promotion budget is small", "to get customers from other apps with large audiences", "I grow without my own marketing"),
        ("📱", "Partner app", "I need to raise MAU and usage frequency", "to add 24/7 sharing to the app", "users come back more often and the audience is monetized"),
    ],
    "bolz-dev": [
        ("🙂", "User", "I ask an AI assistant to buy or book something", "to go from request to payment in one conversation", "I don't follow links or fill in forms"),
        ("🤖", "AI agent", "a user asks me to take an action", "to call a tool with live prices and payment", "I finish the job instead of handing over a link"),
        ("🏪", "Service", "customers increasingly come through AI assistants", "to connect once and appear in agents' answers", "I don't lose those customers"),
    ],
}
JTBD_LBL = {"h": "User jobs (JTBD)", "when": "When", "want": "I want", "so": "so that"}

TOOLKIT_TITLE = "Toolkit"
SQL_TEXT = {
    "title": "SQL sandbox",
    "desc": "A SQL console right in the browser: queries over Roman Ponurov's site data — cases, metrics and posts.",
    "intro": "Real SQLite right in your browser. Inside is this site's data: cases, their metrics, posts and tags. Pick an example or write your own query.",
    "run": "Run", "hint": "Ctrl+Enter", "examples": "Examples", "schema": "Tables", "rows": ["row", "rows", "rows"], "ms": "ms",
    "loading": "Loading SQLite…", "ready": "Ready: SQLite is running in your browser.", "fail": "Could not load SQLite.", "empty": "Query ran, no rows.",
    "note": "Public data only — the same as on the site's pages. Nothing is sent to a server.",
    "suffix": " — Roman Ponurov",
    "ex": [
        ("Top 5 metrics by growth", "SELECT c.company, r.metric, r.change_pct\nFROM results r\nJOIN cases c ON c.slug = r.case_slug\nWHERE r.change_pct > 0\nORDER BY r.change_pct DESC\nLIMIT 5;"),
        ("Posts by year", "SELECT substr(date, 1, 4) AS year, COUNT(*) AS posts\nFROM posts\nGROUP BY year\nORDER BY year;"),
        ("Frequent tags", "SELECT tag, COUNT(*) AS posts\nFROM post_tags\nGROUP BY tag\nORDER BY posts DESC\nLIMIT 8;"),
        ("Cases by task type", "SELECT t.task, COUNT(*) AS cases,\n       GROUP_CONCAT(c.company, ', ') AS companies\nFROM case_tasks t\nJOIN cases c ON c.slug = t.slug\nGROUP BY t.task\nORDER BY cases DESC;"),
        ("Window function: metric rank in a case", "SELECT case_slug, metric, change_pct,\n       RANK() OVER (PARTITION BY case_slug\n                    ORDER BY ABS(change_pct) DESC) AS rnk\nFROM results\nORDER BY case_slug, rnk;"),
    ],
}

CALC_TEXT = {
    "title": "Product calculators",
    "desc": "Interactive calculators for unit economics (LTV, CAC, payback) and A/B tests (sample size, significance).",
    "intro": "Two calculations a product manager does most often. The default numbers are an example, not data from a specific product: plug in your own.",
    "cur": "$", "suffix": " — Roman Ponurov",
    "u_h": "Unit economics", "u_sub": "How much a customer brings in and whether acquiring them pays off.",
    "u_in": [("check", "Average order value", 40, "$"), ("margin", "Margin or commission per order", 25, "%"), ("orders", "Orders over customer lifetime", 6, "pcs"), ("cac", "CAC — acquisition cost", 32, "$")],
    "u_out": {"per": "Revenue per order", "ltv": "LTV — revenue per customer", "ratio": "LTV / CAC", "pay": "CAC payback", "pay_u": "orders",
              "good": "Acquisition pays off with room to spare", "ok": "Pays off, but with a thin margin", "bad": "Acquisition does not pay off"},
    "a_h": "A/B test", "a_sub": "How many users you need and whether the result is significant.",
    "s_h": "Sample size", "s_in": [("p", "Baseline conversion", 10, "%"), ("mde", "Minimum detectable effect (relative)", 10, "%")],
    "alpha": "Significance level α", "power": "Power",
    "s_out": "users in each group", "s_total": "total",
    "t_h": "Result significance", "t_a": "Group A", "t_b": "Group B", "t_users": "Users", "t_conv": "Conversions",
    "t_out": {"cr": "Conversion", "lift": "Difference", "p": "p-value", "sig": "The difference is statistically significant", "nosig": "No significant difference — you need more data, or the effect is smaller than expected"},
    "note": "Calculated for conversions with a two-sided two-proportion z-test.",
}

TOOL_PROOF = {
    "0:0": [("survey of 200 bolz.tech users", "cases/bolz-tech.html")],
    "0:1": [("Dobster", "cases/dobster.html#jtbd"), ("bolz.tech", "cases/bolz-tech.html#jtbd"), ("bolz.dev", "cases/bolz-dev.html#jtbd"), ("Weekend Planner", "projects.html#roadmap")],
    "1:1": [("Weekend Planner roadmap", "projects.html#roadmap")],
    "2:0": [("Asia Online metric tree", "cases/asia-online.html#metric-tree"), ("MTS ID", "cases/mts-id.html#metric-tree")],
    "2:1": [("bolz.tech", "cases/bolz-tech.html"), ("calculator", "calc.html#unit")],
    "2:2": [("experiment at Asia Online", "cases/asia-online.html#experiments"), ("calculator", "calc.html#ab")],
    "2:3": [("SQL sandbox", "sql.html"), ("GoPractice certificate", "study.html")],
    "3:1": [("Weekend Planner user stories", "projects.html#stories")],
    "4:0": [("my path into AI agents", "agents.html"), ("Weekend Planner code", GITHUB + "/weekend-planner")],
    "4:1": [("bolz.dev", "cases/bolz-dev.html")],
    "4:2": [("Weekend Planner evals", GITHUB + "/weekend-planner/tree/main/evals")],
}
TOOL_LBL = {"where": "Where I used it", "proof": "See", "try_h": "Try it yourself",
            "try": [("sql.html", "🗄", "SQL sandbox", "queries over the site's data right in your browser"),
                    ("calc.html", "🧮", "Calculators", "unit economics and A/B tests")]}

ARCH_LBL = {
    "h": "How it works", "tech": "Technologies", "dec": "Technical decisions",
    "opts": "Options", "why": "Why", "trade": "Trade-off", "role": "Product role",
    "legend": [("core", "ours"), ("ext", "external"), ("user", "people"), ("data", "data"), ("plan", "planned")],
    "scroll": "The diagram scrolls sideways",
    "planner_h": "How Weekend Planner works",
    "planner_intro": "One request goes through five stages: parsing → scouting → plan → checks → fixes. The model picks options, and code fills in the facts (names, addresses, prices).",
    "src": "More in the repository docs",
}

ARCH = {
    "planner": {
        "nodes": [
            ("user", "User", "in Telegram", "user", 0, 1.5),
            ("bot", "Telegram bot", "onboarding, buttons, reminders", "core", 1, 1.5),
            ("db", "SQLite", "users, events, plans", "data", 1, 3.2),
            ("planner", "Planner", "orchestrator: a 5-stage workflow", "core", 2, 1.5),
            ("llm", "LLM layer", "OpenAI-compatible API or GigaChat", "ext", 2, 3.2),
            ("scout", "Scout agent", "chooses tools itself", "core", 3, 0.6),
            ("critic", "Critic agent", "18 code checks + LLM review", "core", 3, 2.4),
            ("mcp", "weekend-tools", "MCP server, 4 tools", "core", 4, 0.6),
            ("meteo", "Open-Meteo", "weather, geocoding", "ext", 5, -0.3),
            ("kudago", "KudaGo", "events and places", "ext", 5, 0.6),
            ("osm", "OpenStreetMap", "places fallback", "ext", 5, 1.5),
            ("pw", "Playwright", "browser agent", "ext", 5, 2.4),
        ],
        "edges": [
            ("user", "bot", "", False), ("bot", "planner", "", False), ("bot", "db", "events", False),
            ("planner", "scout", "A2A", False), ("planner", "critic", "A2A", False), ("scout", "mcp", "MCP", False),
            ("mcp", "meteo", "", False), ("mcp", "kudago", "", False), ("mcp", "osm", "", False), ("mcp", "pw", "", False),
            ("planner", "llm", "", False), ("scout", "llm", "", False), ("critic", "llm", "", False),
        ],
        "tech": ["Python 3.13", "Telegram Bot API", "MCP", "A2A", "Playwright", "OpenAI-compatible API", "GigaChat", "SQLite", "Docker"],
        "decisions": [
            {"q": "How to orchestrate", "opts": ["one agent for everything", "a rigid workflow", "a workflow + an agent where the path isn't known in advance"], "pick": 2,
             "why": "Where the path is known (parse → plan → check), predictable code is better; where decisions are made on the fly (which tools, in what order), an agent.",
             "trade": "Less flexibility on known stages, but each stage can be measured and fixed separately.",
             "role": "Project author: my decision."},
            {"q": "How to prevent invented places and prices", "opts": ["the model writes the whole plan", "the model picks ids, code fills in the facts"], "pick": 1,
             "why": "The model cannot “say” a price or an address: after the plan is drafted, code overwrites the name, address, link and price with the candidate's data.",
             "trade": "Free text (explanations, tips) is still written by the model, so evals check it.",
             "role": "Project author: my decision."},
            {"q": "Who blocks a faulty plan", "opts": ["an LLM critic", "code checks; the LLM critic only advises"], "pick": 1,
             "why": "Deterministic checks are stable and cheap, while LLM review can be wrong.",
             "trade": "Code can't check subjective things (“is this what was asked”) — the LLM rates them, but can't block.",
             "role": "Project author: my decision."},
            {"q": "Protocol between agents", "opts": ["the official A2A SDK", "my own minimal A2A"], "pick": 1,
             "why": "About 150 fully understandable lines were enough for a prototype.",
             "trade": "I maintain it myself; but the contract matches the spec, so switching to the SDK only touches the a2a/ package.",
             "role": "Project author: my decision."},
            {"q": "Model lock-in", "opts": ["one provider's SDK", "my own layer over REST: OpenAI-compatible API and GigaChat"], "pick": 1,
             "why": "The model is switched with one setting, and evals compare models from different companies on the same cases; full control over retries and fallbacks.",
             "trade": "More own code: a client per protocol and tests via a mock transport.",
             "role": "Project author: my decision."},
        ],
    },
    "bolz-tech": {
        "nodes": [
            ("user", "User", "", "user", 0, 1.3),
            ("partner", "Partner app", "multi-million audience", "ext", 1, 1.3),
            ("appbolz", "APP BOLZ", "own app, AI smart push", "plan", 1, 2.9),
            ("gw", "MCP gateway connector", "for AI agents in apps", "plan", 2, 0),
            ("webapp", "WebApp Bolz", "web app inside a WebView", "core", 2, 1.3),
            ("backend", "Backend Bolz", "orders, payment, settlements", "core", 3, 1.3),
            ("kassa", "YooKassa", "instant payouts to partners", "ext", 3, 0),
            ("maps", "Maps", "sharing points nearby", "ext", 3, 2.6),
            ("lk", "Business dashboard", "", "plan", 3, 3.7),
            ("sharing", "Sharing services", "power banks, scooters — via API", "ext", 4, 0.7),
            ("vendor", "Vendors", "white-label sharing — via API", "ext", 4, 1.9),
        ],
        "edges": [
            ("user", "partner", "", False), ("partner", "webapp", "WebView", False), ("webapp", "backend", "", False),
            ("backend", "sharing", "API", False), ("backend", "vendor", "API", False), ("backend", "kassa", "", False),
            ("backend", "maps", "", False), ("backend", "lk", "", True), ("appbolz", "backend", "", True),
            ("partner", "gw", "", True), ("gw", "backend", "", True),
        ],
        "tech": ["WebView app", "sharing and vendor REST APIs", "YooKassa", "maps", "MCP (planned)"],
        "decisions": [
            {"q": "How to reach users", "opts": ["our own app", "a web app inside other apps (WebView)"], "pick": 1,
             "why": "Users rent any sharing service without a new install or sign-up, and we grow without our own marketing using partners' audiences.",
             "trade": "A long cycle with each partner: six months passed from agreeing to partner to production.",
             "role": "As CPO I defined the strategy and the B2B2C embedding model."},
            {"q": "What to launch first", "opts": ["all sharing types at once", "one type — power banks"], "pick": 1,
             "why": "One sharing type is faster to take to production: the power bank service launched in December 2024.",
             "trade": "At launch the “everything in one window” value isn't fully visible.",
             "role": "I ran the roadmap: from power banks to bikes, scooters, cars, coworkings and EV charging."},
            {"q": "How to handle payment", "opts": ["payment in each sharing service separately", "one card link for all sharing services"], "pick": 1,
             "why": "The user's main pain is signing up and linking a card again; partners get paid instantly via YooKassa.",
             "trade": "Bolz takes on settlements with partners.",
             "role": "I designed the user journey and the architecture."},
        ],
    },
    "bolz-dev": {
        "nodes": [
            ("user", "User", "“find a movie and buy a ticket”", "user", 0, 1.5),
            ("agent", "AI agent", "ChatGPT, Claude and others", "ext", 1, 1.5),
            ("sandbox", "Sandbox", "tutorials for developers", "plan", 1, 3),
            ("conn", "Bolz Connector", "MCP server: search, book, pay", "core", 2, 1.5),
            ("eval", "Execution evals", "success = a paid order", "core", 2, 3),
            ("cinema", "Cinemas", "", "ext", 3, 0),
            ("taxi", "Taxi", "", "ext", 3, 1),
            ("car", "Car sharing", "", "ext", 3, 2),
            ("market", "Marketplaces", "", "ext", 3, 3),
        ],
        "edges": [
            ("user", "agent", "request", False), ("agent", "conn", "MCP", False),
            ("conn", "cinema", "API", False), ("conn", "taxi", "API", False), ("conn", "car", "API", False), ("conn", "market", "API", False),
            ("conn", "eval", "action result", False), ("sandbox", "conn", "", True),
        ],
        "tech": ["Model Context Protocol", "service REST APIs", "normalized JSON, live prices", "plugins and a web interface for onboarding", "execution-based evals"],
        "decisions": [
            {"q": "How an agent takes action", "opts": ["the agent repeats human actions on websites (scraping, clicks)", "connectors to service APIs via MCP"], "pick": 1,
             "why": "Through websites an agent is slow and unreliable: the best models complete real tasks less than half the time. APIs give live prices and order and payment functions.",
             "trade": "Each service has to be connected, so coverage grows with integrations.",
             "role": "As CPO I described the architecture and analysed competitors: Notte and Firecrawl work through websites."},
            {"q": "How to measure agent quality", "opts": ["by the text of the answer", "by the completed action"], "pick": 1,
             "why": "The user needs a purchased ticket, not a nice answer.",
             "role": "I set the success metric: a paid order."},
        ],
    },
    "asia-online": {
        "nodes": [
            ("buyer", "Customer", "", "user", 0, 2),
            ("app", "Mobile app", "redesign and refactoring", "core", 1, 0),
            ("site", "Website", "redesign", "core", 1, 1),
            ("call", "Call center", "orders by script", "core", 1, 2),
            ("mbank", "Storefront in M-Bank", "banking app", "ext", 1, 3),
            ("glovo", "Glovo", "external integration", "ext", 1, 4),
            ("back", "E-commerce platform", "orders, catalog", "core", 2, 2),
            ("pay", "Online payment", "", "ext", 3, 0.4),
            ("erp", "Accounting", "prices, discounts, stock", "data", 3, 1.5),
            ("picker", "Picker app", "order picking", "core", 3, 2.6),
            ("an", "Analytics", "metrics and incidents", "data", 3, 3.7),
            ("stores", "Stores", "pickers", "user", 4, 2.6),
        ],
        "edges": [
            ("buyer", "app", "", False), ("buyer", "site", "", False), ("buyer", "call", "", False), ("buyer", "mbank", "", False), ("buyer", "glovo", "", False),
            ("app", "back", "", False), ("site", "back", "", False), ("call", "back", "", False), ("mbank", "back", "", False), ("glovo", "back", "", False),
            ("back", "pay", "", False), ("back", "erp", "", False), ("back", "picker", "", False), ("back", "an", "", False), ("stores", "picker", "", False),
        ],
        "tech": ["Python", "React Native", "Flutter", "online payment", "Glovo integration", "storefront in M-Bank"],
        "decisions": [],
    },
    "mts-id": {
        "nodes": [
            ("user", "User", "~10M", "user", 0, 1),
            ("p9", "9 MTS products", "flagship services", "ext", 1, 0),
            ("bank", "MTS Bank", "", "ext", 1, 1),
            ("ext2", "2 external products", "together with MTS Pay", "ext", 1, 2),
            ("id", "MTS ID", "single seamless sign-in", "core", 2, 1),
            ("mono", "Monolith", "before", "old", 3, 0.2),
            ("ms", "Microservices", "after", "core", 3, 1.8),
        ],
        "edges": [
            ("user", "p9", "", False), ("user", "bank", "", False), ("user", "ext2", "", False),
            ("p9", "id", "sign-in", False), ("bank", "id", "sign-in", False), ("ext2", "id", "sign-in", False),
            ("id", "mono", "", True), ("id", "ms", "", False),
        ],
        "tech": ["Java", "Swift", "Kotlin", "microservice architecture", "web + mobile"],
        "decisions": [
            {"q": "Platform architecture", "opts": ["keep the monolith", "move to microservices"], "pick": 1,
             "why": "The platform's value grows with every connected service, so the key work is integrations and reliability.",
             "role": "I led the migration as part of product work, not just as an engineering task."},
        ],
    },
    "po-sosedstvu": {
        "nodes": [
            ("b2c", "B2C customer", "", "user", 0, 0.4),
            ("b2b", "B2B client", "companies and sole traders", "user", 0, 2),
            ("site", "Online store", "1C-Bitrix: catalog, cart, points", "core", 1, 0.4),
            ("lk", "B2B account", "prices and stock", "core", 1, 2),
            ("one", "1C", "accounting: prices, stock", "data", 2, -0.5),
            ("mgr", "Manager", "document checks, access", "user", 2, 2.8),
            ("del", "Delivery and pickup", "Moscow region, other regions by carrier", "ext", 3, 1.2),
        ],
        "edges": [
            ("b2c", "site", "", False), ("b2b", "lk", "application", False), ("site", "one", "", False), ("lk", "one", "", False),
            ("mgr", "lk", "access", True), ("site", "del", "", False), ("lk", "del", "", False),
        ],
        "tech": ["1C-Bitrix", "1C", "web + adaptive", "external team: design, development, 1C, analytics, SEO"],
        "decisions": [
            {"q": "What to build the store on", "opts": ["custom development", "a ready-made platform and an external team"], "pick": 1,
             "why": "Resources were small: a ready-made platform with an external team is faster to launch.",
             "trade": "Launch speed and budget matter more than the flexibility of custom development.",
             "role": "I assembled the external team and set up the development process with them."},
        ],
    },
    "dobster": {
        "nodes": [
            ("rec", "Recipient", "", "user", 0, 0.3),
            ("helper", "Helper", "volunteer or professional", "user", 0, 1.5),
            ("donor", "Donor", "", "user", 0, 2.7),
            ("gos", "Gosuslugi", "status verification", "ext", 1, 0.3),
            ("plat", "Dobster platform", "tasks, responses, roles · Python, React", "core", 2, 1.5),
            ("notif", "Notifications", "to helpers and donors", "core", 3, 0.4),
            ("rep", "Reports and reviews", "", "core", 3, 1.5),
            ("partner", "Partner block", "partner companies", "core", 3, 2.6),
        ],
        "edges": [
            ("rec", "gos", "", False), ("gos", "plat", "task", False), ("helper", "plat", "response", False),
            ("donor", "plat", "task payment", False), ("plat", "notif", "", False), ("plat", "rep", "", False), ("plat", "partner", "", False),
        ],
        "tech": ["Python", "React", "Gosuslugi", "web + adaptive"],
        "decisions": [],
    },
}

PATCH = {k: v for k, v in globals().items() if k.isupper() and k not in ("HERE", "GITHUB", "WP", "PIO", "SP")}
PATCH["BOOKS_LINK"] = '<a href="{up}books.html">📚 books</a>'
PATCH["MEDIA_LINK"] = '<a href="{up}media.html">🎧 podcasts</a>'
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
            (pl(len(ys), "post", "posts"), len(ys), "blog/"),
        ]
        if year == 2026:
            rows.insert(0, ("university course I teach", 1, "blog/lekcii-it-menedzhment.html"))
            rows.insert(1, ("open-source AI prototype", 1, "projects.html"))
        if year == 2025:
            rows.insert(0, ("startups: bolz.tech and bolz.dev", 2, "projects.html"))
        if year == 2024:
            rows[0:0] = [("new role: senior product manager at Gazprombank", 1, "cases/gazprombank.html"),
                         ("started a PhD at RANEPA", 1, "research.html"),
                         ("bolz.tech partners: MTS Urent and GetEnergy", 2, "cases/bolz-tech.html"),
                         ("power bank sharing service in production", 1, "cases/bolz-tech.html")]
        if year == 2023:
            rows[0:0] = [("Asia Online revenue after the relaunch (2023–2024)", "+103%", "cases/asia-online.html"),
                         ("IT team built from scratch at Asia Retail", 1, "cases/asia-online.html"),
                         ("startup founded: bolz.tech", 1, "cases/bolz-tech.html"),
                         ("Dobster: from idea to production (2022–2023)", 1, "cases/dobster.html")]
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
<details class="menu"><summary>product</summary><div class="menu-list"><a href="{up}about.html">👋 about me</a><a href="{up}now.html">⏱ now</a><a href="{up}timeline.html">🗓 timeline</a><a href="{up}assets/Ponurov_Roman_CV_EN.pdf" target="_blank" rel="noopener">📄 CV (PDF)</a><a href="{up}cases/index.html">📁 case portfolio</a><a href="{up}tools.html">🧰 toolkit</a><a href="{up}sql.html">🗄 SQL sandbox</a><a href="{up}calc.html">🧮 calculators</a></div></details>
<a href="{up}projects.html">projects</a>
<details class="menu"><summary>knowledge</summary><div class="menu-list"><a href="{up}research.html">🔬 research</a><a href="{up}conferences.html">🎤 conferences</a><a href="{up}study.html">🎓 education</a>{PATCH["BOOKS_LINK"].format(up=up)}{PATCH["MEDIA_LINK"].format(up=up)}</div></details>
<details class="menu"><summary>AI</summary><div class="menu-list"><a href="{up}agents.html">🤖 AI agents</a><a href="{up}skills.html">🧰 AI skills</a></div></details>
<details class="menu"><summary>posts</summary><div class="menu-list"><a href="{up}blog/index.html">📝 all posts</a><a href="{up}tags/index.html">🏷 tags</a></div></details>
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
