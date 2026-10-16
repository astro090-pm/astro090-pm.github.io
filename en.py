"""Английская версия сайта: /en/ — главная, кейсы, проекты, исследования. Вызывается из build.py."""
import html as _html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
esc = lambda s: _html.escape(s, quote=True)

CASES_EN = [
    # slug, company, years, title-short, cover (big, small, color), work?
    ("gazprombank", "Gazprombank", "2024 — now", ("AI agent", "credit analysis", "#C9DDC5"), True),
    ("asia-online", "Asia Retail", "2023–2024", ("+103%", "revenue", "#F0C24B"), True),
    ("mts-id", "MTS", "2021–2023", ("10M", "users", "#BFD3F2"), True),
    ("granit", "Concern GRANIT", "2019–2021", ("B2G", "process automation", "#D9DED6"), True),
    ("bolz-dev", "bolz.dev", "2025", ("MCP", "actions for AI agents", "#C9E8D5"), False),
    ("bolz-tech", "bolz.tech", "2023–2025", ("B2B2C", "sharing in one window", "#BFD3F2"), False),
    ("po-sosedstvu", "Po Sosedstvu", "2022–2024", ("+89%", "B2B orders", "#F0C24B"), False),
    ("dobster", "Dobster", "2022–2023", ("0 → prod", "charity platform", "#E8D3E0"), False),
]


def title(slug):
    t = (ROOT / "content" / "en" / "cases" / f"{slug}.md").read_text(encoding="utf-8")
    return re.search(r"^#\s+(.+)$", t, re.M).group(1).strip()


def layout(ctx, page_title, description, body, path, ru_path, depth=1):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(page_title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{ctx['SITE_URL']}/{path}">
<link rel="alternate" hreflang="ru" href="{ctx['SITE_URL']}/{ru_path}">
<link rel="alternate" hreflang="en" href="{ctx['SITE_URL']}/{path}">
<meta property="og:title" content="{esc(page_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{ctx['SITE_URL']}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{ctx['FONTS']}">
<link rel="stylesheet" href="{up}assets/style.css?v={ctx['CSS_V']}">
<script>try{{const t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t;}}catch(e){{}}</script>
<script src="{up}assets/site.js?v={ctx['JS_V']}" defer data-root="{up}"></script>
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{up}en/"><img class="avatar avatar-sm" src="{up}assets/avatar-sm.jpg" width="34" height="34" alt="">Roman Ponurov</a>
<nav class="nav" aria-label="Sections">
<a href="{up}en/">about</a>
<a href="{up}en/cases/">case studies</a>
<a href="{up}en/projects.html">projects</a>
<a href="{up}en/research.html">research</a>
<a href="{up}assets/Ponurov_Roman_CV.pdf" target="_blank" rel="noopener">CV (RU)</a>
</nav>
<span class="tools">
<a class="icon-btn lang" href="{up}{ru_path}" title="Русская версия" hreflang="ru">RU</a>
<button type="button" class="icon-btn" id="theme-toggle" aria-label="Toggle dark theme"><svg class="i-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg><svg class="i-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>
</span>
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


def cards(prefix, which):
    out = []
    for slug, company, years, (big, small, color), work in CASES_EN:
        if work != which:
            continue
        out.append(f"""<li class="card case-card">
<a class="cover" href="{prefix}{slug}.html" style="background:{color}" aria-hidden="true" tabindex="-1"><span class="cover-big">{esc(big)}</span><span class="cover-small">{esc(small)}</span></a>
<p class="card-meta">{esc(company)} · {esc(years)}</p>
<h3 class="card-title"><a href="{prefix}{slug}.html">{esc(title(slug))}</a></h3>
</li>""")
    return "\n".join(out)


def index_page(ctx):
    body = f"""
<div class="wrap home">
<section class="hero-home">
<img class="avatar avatar-lg" src="../assets/avatar.jpg" width="160" height="160" alt="Roman Ponurov">
<div>
<h1>Roman Ponurov</h1>
<p class="roles">Senior Product Manager building AI products · university lecturer in IT management · PhD researcher on AI in corporate management</p>
</div>
</section>

<section class="results" aria-label="Key results">
<a class="res" href="cases/asia-online.html"><b data-count="103" data-prefix="+" data-suffix="%">+103%</b><span>revenue after an e-commerce relaunch</span></a>
<a class="res" href="cases/mts-id.html"><b data-count="10" data-suffix="M">10M</b><span>users of MTS ID across 9 products</span></a>
<a class="res" href="cases/po-sosedstvu.html"><b data-count="89" data-prefix="+" data-suffix="%">+89%</b><span>B2B orders after going online</span></a>
<a class="res" href="cases/"><b data-count="4">4</b><span>products launched from scratch</span></a>
</section>

<div class="prose">
<h2>About</h2>
<p>I'm a product manager with 6+ years in B2C, B2B, B2E and B2G — foodtech, telecom, fintech and charity. I launch products from scratch and take offline businesses online. Today I build an internal corporate credit analysis service with an AI agent at Gazprombank and prototype agentic products on my own: MCP servers, multi-agent systems over A2A, evals and product metrics for agents.</p>
<p>Alongside product work I'm a PhD candidate at RANEPA researching how artificial intelligence improves corporate management, and I teach an IT management course to first-year university students.</p>

<h2>Experience</h2>
<ul>
<li><b>Gazprombank</b> — Senior Product Manager, 2024 — now. Internal credit analysis service with an AI agent, from concept and budget to production.</li>
<li><b>Asia Retail</b> — Head of E-commerce, 2023–2024. Relaunched online grocery delivery: revenue +103%, orders +67%, churn −24%.</li>
<li><b>MTS</b> — Product Manager, MTS ID, 2021–2023. Seamless sign-in in 9 flagship products for ~10M users, seamless logins +23%.</li>
<li><b>Concern GRANIT</b> — Systems Analyst → Product Manager, 2019–2021. B2G process automation from scratch.</li>
<li><b>Earlier (2014–2019)</b> — electrical engineer, sales engineer, business development manager; built the first company website.</li>
</ul>

<h2>Startups and side projects</h2>
<ul>
<li><a href="cases/bolz-dev.html"><b>bolz.dev</b></a> — co-founder & CPO: MCP connector that lets AI agents take real-world actions (MVP, 2025).</li>
<li><a href="cases/bolz-tech.html"><b>bolz.tech</b></a> — co-founder & CPO: all sharing services in one window (B2B2C); Moscow Innovation Cluster accelerator.</li>
<li><a href="cases/po-sosedstvu.html"><b>Po Sosedstvu</b></a> — co-founder: offline grocery store taken online; B2B orders +89%.</li>
<li><a href="cases/dobster.html"><b>Dobster</b></a> — co-founder: charity platform for free help at home.</li>
<li><a href="projects.html"><b>Weekend Planner</b></a> — open-source agentic Telegram bot: A2A agents, own MCP server, 32 eval cases.</li>
</ul>

<h2>Research and teaching</h2>
<p>3 peer-reviewed articles (VAK list) and 3 international conference talks on AI in management, 2025–2026 — see <a href="research.html">research</a>. Since October 2026 I teach a 7-lecture IT management course.</p>

<h2>Education</h2>
<ul>
<li><b>RANEPA</b> — PhD programme in management, 2024–2027.</li>
<li><b>HSE University</b> — MSc in Corporate Finance, 2021.</li>
<li><b>Moscow Power Engineering Institute</b> — MSc in Electrical Engineering, 2015.</li>
<li>Professional Scrum Product Owner I (PSPO I); courses by ProductDo, GoPractice, Pendo.io.</li>
</ul>

<h2>Skills</h2>
<p>Product strategy, hypotheses, CustDev, JTBD, A/B tests, unit economics, roadmap and backlog, product budgets · team leadership up to 50 people, Agile, KPIs · BPMN, user stories · Figma, Miro, SQL, Git · Claude Code, Cursor, LLM APIs, n8n; LLM agents, MCP, A2A, evals · English B1 (BEC).</p>

<h2>Contacts</h2>
<p>Telegram <a href="https://t.me/astro090">@astro090</a> · <a href="mailto:ponurov.roman@yandex.ru">ponurov.roman@yandex.ru</a> · <a href="https://www.linkedin.com/in/roman-ponurov-bb3b81a6/">LinkedIn</a> · <a href="https://github.com/astro090-pm">GitHub</a></p>
</div>
</div>
"""
    return layout(ctx, "Roman Ponurov — Product Manager", "Roman Ponurov: senior product manager building AI products, lecturer and PhD researcher on AI in management.", body, "en/", "", depth=1)


def cases_page(ctx):
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="../">Home</a>
<h1>Case studies</h1>
<p class="intro">Products I launched and grew at work — and my own startups. Each case: context, what I did, results.</p>
<h2>At work</h2>
<ul class="cards">{cards("", True)}</ul>
<h2 class="own-ai">Startups and side projects</h2>
<ul class="cards">{cards("", False)}</ul>
</div></article>
"""
    return layout(ctx, "Case studies — Roman Ponurov", "Product case studies: e-commerce, telecom, fintech, B2G and startups.", body, "en/cases/", "cases/", depth=2)


def case_page(ctx, slug, company, nxt):
    text = (ROOT / "content" / "en" / "cases" / f"{slug}.md").read_text(encoding="utf-8")
    t = re.search(r"^#\s+(.+)$", text, re.M).group(1).strip()
    text = re.sub(r"^#\s+.+\n", "", text, count=1)
    text = re.sub(r"(?m)^(?!- |\d+\. )(.+)\n(?=- |\d+\. )", r"\1\n\n", text)
    body_html = markdown.markdown(text, extensions=["tables", "sane_lists"])
    body = f"""
<article class="page"><div class="wrap">
<a class="back" href="./">All case studies</a>
<h1>{esc(t)}</h1>
<div class="prose">
{body_html}
<p class="next-case">Next case: <a href="{nxt}.html">{esc(title(nxt))}</a></p>
</div>
</div></article>
"""
    return layout(ctx, f"{t} — Roman Ponurov", t, body, f"en/cases/{slug}.html", f"cases/{slug}.html", depth=2)


def projects_page(ctx):
    body = """
<article class="page"><div class="wrap">
<a class="back" href="./">Home</a>
<h1>Projects</h1>
<p class="intro">An open-source prototype where I test ideas about agentic products. Startups are in <a href="cases/">case studies</a>.</p>
<article class="project">
<div>
<h3>Weekend Planner</h3>
<p>A Telegram bot that builds an hour-by-hour weekend plan in a minute: it checks the weather, events and places, fits the budget and takes kids' ages into account.</p>
<ul>
<li>Three agents — planner, scout and critic — talk over the A2A protocol</li>
<li>Tools live in a custom MCP server; there is a browser agent</li>
<li>The model only chooses options — names, prices and times are filled in by code</li>
<li>32 eval cases and product metrics: activation, retention, ratings</li>
</ul>
<p><a href="https://github.com/astro090-pm/weekend-planner">Code and docs on GitHub</a></p>
</div>
<figure>
<img src="../assets/weekend-planner-arch.png" width="1344" height="960" alt="Architecture: Telegram bot → planner; planner talks to scout and critic over A2A; scout uses an MCP server for weather, events, places and a browser.">
<figcaption>Who talks to whom inside the bot</figcaption>
</figure>
</article>
</div></article>
"""
    return layout(ctx, "Projects — Roman Ponurov", "Open-source agentic prototype: Weekend Planner.", body, "en/projects.html", "projects.html")


def research_page(ctx):
    body = """
<article class="page"><div class="wrap">
<a class="back" href="./">Home</a>
<h1>Research</h1>
<p class="intro">I study how artificial intelligence changes corporate management — not individual tasks but the system itself: planning, decision-making, control and communication. It complements my product work: by day I build a service with an AI agent at a bank, and in research I look at why such projects succeed in some companies and fail in others.</p>
<div class="res-card"><img class="uni-logo" src="../assets/uni/ranepa.png" width="35" height="64" alt=""><div>
<p class="res-kicker">PhD programme, RANEPA · 2024–2027 · Institute of Industry Management</p>
<p class="res-topic">“Using artificial intelligence to improve a company's management system”</p></div></div>
<div class="res-stats"><div><b>3</b>peer-reviewed articles (VAK list)</div><div><b>3</b>international conference talks</div></div>
<h2>Method</h2>
<p class="intro">Besides literature and industry-practice analysis, the empirical part is a case study in a large Russian bank: semi-structured interviews with AI product and project managers, AI centre specialists, top management and employees who use AI tools daily. The interviews are anonymised and coded into a thematic matrix.</p>
<h3 class="pubs-head">Articles</h3>
<ul class="pubs">
<li><span class="when">December 2025</span><span class="what"><a href="https://s-lib.com/issues/eiu_2025_10_v13_a28/">Risks and limitations of using AI in company management</a><i>Economics and Management: Problems, Solutions (in Russian)</i></span></li>
<li><span class="when">September 2025</span><span class="what"><a href="https://www.finance-man.ru/index.php/journal/article/view/2105">Current trends in the use of AI in corporate governance during digital transformation</a><i>Financial Management (in Russian)</i></span></li>
<li><span class="when">May 2025</span><span class="what"><a href="https://s-lib.com/issues/eiu_2025_06_v7_a26/">Specific features of AI use in the management of Russian companies</a><i>Economics and Management: Problems, Solutions (in Russian)</i></span></li>
</ul>
<h3 class="pubs-head">Conference talks</h3>
<ul class="pubs">
<li><span class="when">September 2026</span><span class="what"><a href="https://naukaip.ru/wp-content/uploads/2026/09/MK-2774.pdf">Organisational readiness of Russian companies to adopt AI in management: barriers and directions</a><i>XVI International Scientific and Practical Conference, Penza</i></span></li>
<li><span class="when">September 2026</span><span class="what"><a href="https://sibac.info/conf/economy/cx/430396">Organisational and managerial mechanisms for reducing AI risks in bank management</a><i>CX International Scientific and Practical Conference, Novosibirsk</i></span></li>
<li><span class="when">March 2026</span><span class="what"><a href="https://sibac.info/conf/economy/civ/403674">Technology requirements for company infrastructure when implementing AI</a><i>CIV International Scientific and Practical Conference, Novosibirsk</i></span></li>
</ul>
</div></article>
"""
    return layout(ctx, "Research — Roman Ponurov", "Research on AI in corporate management: articles and international conference talks.", body, "en/research.html", "research.html")


def build(ctx):
    out = ROOT / "en"
    (out / "cases").mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(index_page(ctx), encoding="utf-8")
    (out / "projects.html").write_text(projects_page(ctx), encoding="utf-8")
    (out / "research.html").write_text(research_page(ctx), encoding="utf-8")
    (out / "cases" / "index.html").write_text(cases_page(ctx), encoding="utf-8")
    slugs = [c[0] for c in CASES_EN]
    for i, (slug, company, *_r) in enumerate(CASES_EN):
        (out / "cases" / f"{slug}.html").write_text(case_page(ctx, slug, company, slugs[(i + 1) % len(slugs)]), encoding="utf-8")
