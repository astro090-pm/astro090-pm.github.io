"""Английские версии страниц, которые в build.py почти целиком состоят из текста."""


def install(B):
    esc, GITHUB, TG = B.esc, B.GITHUB, B.TG

    def cv_page():
        body = """
<section class="hero"><div class="wrap">
<a class="back" href="index.html">Home</a>
<h1>Résumé</h1>
<p class="lead">Product manager. For six years I've been launching products from scratch and taking businesses from offline to online.</p>
<p class="lead">I've worked in foodtech, telecom, fintech and charity — in B2C, B2B, B2E and B2G. Today I build AI products and research AI in company management.</p>
<p class="cv-link"><a href="assets/Ponurov_Roman_CV.pdf">Download the CV, PDF (in Russian)</a></p>
<div class="ledger" aria-label="Results">
<div class="ledger-row"><span class="num">+103%</span><span class="ledger-what">revenue after relaunching online grocery delivery</span><span class="ledger-where"><a href="cases/asia-online.html">Asia Online, 2023–2024</a></span></div>
<div class="ledger-row"><span class="num">10M</span><span class="ledger-what">users sign in to 9 MTS products with a single account</span><span class="ledger-where"><a href="cases/mts-id.html">MTS ID, 2021–2023</a></span></div>
<div class="ledger-row"><span class="num">+89%</span><span class="ledger-what">orders from business clients after the store went online</span><span class="ledger-where"><a href="cases/po-sosedstvu.html">Po Sosedstvu, 2022–2024</a></span></div>
<div class="ledger-row"><span class="num">4</span><span class="ledger-what">products launched from scratch, two of them as a co-founder</span><span class="ledger-where"><a href="cases/index.html">all cases</a></span></div>
</div>
</div></section>

<section class="block" id="path"><div class="wrap">
<h2>Career path</h2>
<p class="intro">From engineering to systems analysis, and from there to product management.</p>
<ol class="path">
<li><span class="yrs">2014–2015</span>Electrical machine test engineer, then electrical equipment repair engineer — Agregat-Privod, Mosenergo</li>
<li><span class="yrs">2017–2019</span>Lead sales engineer, then business development manager — Lighthouse Technologies. First product experience: built the company website from scratch — concept, structure, features, content — and ran its analytics in Yandex Metrica</li>
<li><span class="yrs">2019–2020</span>Lead systems analyst — Concern GRANIT</li>
<li><span class="yrs">2020–2021</span>Product manager — Concern GRANIT</li>
<li><span class="yrs">2021–2023</span>Product manager, MTS ID — MTS</li>
<li><span class="yrs">2023–2024</span>Head of E-commerce — Asia Retail</li>
<li class="now"><span class="yrs">since 2024</span>Senior product manager — Gazprombank</li>
</ol>
<p class="intro" style="margin-top:24px">Education is on a <a href="study.html">separate page</a>, academic work is under <a href="research.html">research</a>.</p>
</div></section>

<section class="block" id="contacts"><div class="wrap">
<h2>Contacts</h2>
<p class="intro">Open to conversations about product and AI roles.</p>
<div class="contacts">
<a href="https://t.me/astro090">Telegram: @astro090</a>
<a href="mailto:ponurov.roman@yandex.ru">ponurov.roman@yandex.ru</a>
<a href="https://www.linkedin.com/in/roman-ponurov-bb3b81a6/">LinkedIn</a>
<a href="https://github.com/astro090-pm">GitHub</a>
</div>
</div></section>
"""
        return B.layout("Résumé — Roman Ponurov", "Roman Ponurov's résumé: results, career path, contacts.", body, "cv.html")

    def projects_page():
        body = f"""
<article class="page"><div class="wrap">
<a class="back" href="index.html">Home</a>
<h1>Projects</h1>
<p class="intro">Things I launched myself — as a co-founder or author — and prototypes I use to test hypotheses about AI products.</p>

<h2>My own projects</h2>
<ul class="cards own">
{B.own_cards()}
</ul>

<h2 class="own-ai">AI prototypes</h2>
<p class="intro">The code is open.</p>
<article class="project">
<div>
<h3>Weekend Planner</h3>
<p>A Telegram bot that builds an hour-by-hour weekend plan in a minute: it checks the weather, events and places, stays within budget and takes the children's ages into account.</p>
<ul>
<li>Three agents — planner, scout and critic — talk over the A2A protocol</li>
<li>Tools live in my own MCP server; there is also a browser agent</li>
<li>The model only chooses options — names, prices and times are filled in by code</li>
<li>32 eval cases and product metrics: activation, retention, ratings</li>
</ul>
<p><a href="{GITHUB}/weekend-planner">Code and description on GitHub</a></p>
</div>
<figure>
<img src="assets/weekend-planner-arch.png" width="1344" height="960" alt="Diagram: the user writes to the Telegram bot, which passes the request to the planner; the planner calls the scout and the critic over A2A; the scout gets weather, events and places through the MCP server and reads pages with a browser.">
<figcaption>Who works with whom inside the bot</figcaption>
</figure>
</article>
</div></article>
"""
        return B.layout("Projects — Roman Ponurov", "Roman Ponurov's own startups and open-source AI projects.", body, "projects.html")

    def research_page(posts):
        notes = [p for p in posts if {TG["research"], TG["article"], TG["conference"]} & set(p["tags"])]
        body = f"""
<article class="page"><div class="wrap">
<a class="back" href="index.html">Home</a>
<h1>Research</h1>
<p class="intro">I study how artificial intelligence changes the way a company is managed: not individual tasks, but the system itself — planning, decision-making, control and communication. It's a continuation of my product work: by day I build a service with an AI agent at a bank, and in my research I try to understand why such projects work in some companies and fail in others.</p>

<div class="res-card">
<img class="uni-logo" src="assets/uni/ranepa.png" width="35" height="64" alt="">
<div>
<p class="res-kicker">PhD programme at RANEPA · 2024–2027 · Institute of Industry Management, Department of Theory and Systems of Industry Management</p>
<p class="res-topic">“Using artificial intelligence to improve a company's management system”</p>
</div>
</div>

<div class="res-stats">
<div><b>3</b>articles in peer-reviewed journals (VAK list)</div>
<div><b>3</b>talks at international conferences</div>
</div>

<h2>How I do research</h2>
<p class="intro">Besides reviewing the literature and company practice, the empirical part of the dissertation is a case study at a large Russian bank. I ran a series of semi-structured interviews with four groups of respondents: AI product and project managers, specialists from the AI technology centre, top management, and employees who work with AI tools every day. The interviews are anonymised, and the answers are compiled into a thematic matrix: where AI is built into management, how goals and KPIs for adoption are set, what gets in the way and what helps. The summary is in the post <a href="blog/intervyu-ii-v-banke.html">“What holds AI back in management”</a>.</p>

<h2>Questions I'm interested in</h2>
<ul class="res-q">
<li>In which management processes AI really makes a difference, and where it's just hype.</li>
<li>What risks and limitations it brings — from data quality to accountability for a decision.</li>
<li>What a company needs to prepare in advance: data, infrastructure, people and rules.</li>
</ul>

<h3 class="pubs-head">Articles in peer-reviewed journals (VAK list) <span>3</span></h3>
<ul class="pubs">
<li><span class="when">December 2025</span><span class="what"><a href="https://s-lib.com/issues/eiu_2025_10_v13_a28/">Risks and limitations of using artificial intelligence in company management</a><i>Economics and Management: Problems, Solutions</i></span></li>
<li><span class="when">September 2025</span><span class="what"><a href="https://www.finance-man.ru/index.php/journal/article/view/2105">Current trends in the use of artificial intelligence in corporate governance during digital transformation</a><i>Financial Management</i></span></li>
<li><span class="when">May 2025</span><span class="what"><a href="https://s-lib.com/issues/eiu_2025_06_v7_a26/">Characteristic features of the use of artificial intelligence in the management of Russian companies</a><i>Economics and Management: Problems, Solutions</i></span></li>
</ul>
<h3 class="pubs-head">Talks at international conferences <span>3</span></h3>
<ul class="pubs">
{"".join(f'<li><span class="when">{esc(d.split(" ", 1)[1])}</span><span class="what"><a href="{u}">{esc(t)}</a><i>{esc(c)}, {esc(city)}</i></span></li>' for d, city, c, t, u, _s, _i in B.CONFS)}
</ul>

{('<h2 class="res-notes">Research notes</h2><ul class="feed">' + B.feed(notes, "blog/") + '</ul>') if notes else ''}
</div></article>
"""
        return B.layout("Research — Roman Ponurov",
                        "Roman Ponurov's research on AI in company management: peer-reviewed articles and international conference talks.",
                        body, "research.html")

    def study_page():
        blocks = []
        for title, rows in B.STUDY:
            lis = "\n".join(
                f'<li><span class="when">{esc(org)}<br>{esc(kind)}</span><span class="what">{esc(name)}<i>{esc(about)}</i></span></li>'
                for org, name, about, kind in rows)
            blocks.append(f'<section class="uni"><div class="uni-head"><h2>{esc(title)}</h2></div><ul class="pubs">\n{lis}\n</ul></section>')
        body = f"""
<article class="page"><div class="wrap">
<a class="back" href="index.html">Home</a>
<h1>Education</h1>
<p class="intro">Three universities — engineering, finance, management — and everything else I've studied: certificates, courses, an accelerator and an independent assessment.</p>
<h2 class="edu-head">Higher education</h2>
<section class="uni">
<div class="uni-head"><h2><img class="uni-logo" src="assets/uni/ranepa.png" width="35" height="64" alt="">RANEPA</h2><p class="uni-meta">PhD programme, management<br>Moscow, 2024–2027</p></div>
<p class="uni-topic">Institute of Industry Management, Department of Theory and Systems of Industry Management. Dissertation: “Using artificial intelligence to improve a company's management system” — details on the <a href="research.html">research</a> page.</p>
</section>
<section class="uni">
<div class="uni-head"><h2><img class="uni-logo" src="assets/uni/hse.png" width="64" height="64" alt="">HSE University</h2><p class="uni-meta">Master's, Corporate Finance<br>Moscow, 2018–2021</p></div>
<p class="uni-topic">Faculty of Economic Sciences, “Corporate Finance” programme. Thesis: “Modelling and evaluating the efficiency of investment projects in a company's digital transformation” — how to tell in advance whether a digital transformation will pay off. <a href="blog/magisterskaya-vshe.html">More</a> · <a href="assets/decks/hse-master-thesis.pdf" target="_blank" rel="noopener">slides, PDF</a></p>
</section>

<section class="uni">
<div class="uni-head"><h2><img class="uni-logo" src="assets/uni/mei.png" width="136" height="64" alt="">MPEI</h2><p class="uni-meta">Master's, Electrical Engineering<br>Moscow, 2008–2015</p></div>
<p class="uni-topic">Moscow Power Engineering Institute. The engineering foundation where it all started: testing and maintaining electrical equipment, then selling technical solutions.</p>
</section>
<h2 class="edu-head">Further learning</h2>
{"".join(blocks)}
</div></article>
"""
        return B.layout("Education — Roman Ponurov", "Roman Ponurov's education: RANEPA, HSE University, MPEI, certificates, courses and accelerators.", body, "study.html")

    def about_page():
        body = """
<article class="page"><div class="wrap">
<a class="back" href="index.html">Home</a>
<h1>About me</h1>
<div class="prose about">
<p>Hi 👋 This page is a short manual for working with me. It's for colleagues, teammates and anyone I'm starting something with: <b>so we spend less time getting used to each other and more time on the product</b>.</p>

<h2>What I do</h2>
<p>By day I'm a product manager, and as a PhD student at RANEPA I'm writing a dissertation on <b>“Using artificial intelligence to improve a company's management system”</b>. It's the same topic from two sides: at work I build a service with an AI agent for credit analysis, and in my research I look at how AI changes not individual tasks but management itself — planning, decision-making, control and communication inside a company.</p>
<p>I'm interested in three questions:</p>
<ul>
<li>in which management processes AI really makes a difference, and where it's just hype;</li>
<li>what risks and limitations it brings — from data quality to accountability for a decision;</li>
<li>what a company needs to prepare in advance: data, infrastructure, people and rules.</li>
</ul>
<p>That's what my <a href="research.html">articles and talks</a> are about, and I cover the practical side in the <a href="agents.html">AI agents</a> section.</p>

<h2>What I believe in</h2>
<ul>
<li>Hypothesis → test → decision</li>
<li>One primary metric per experiment</li>
<li>Business results matter more than the number of features</li>
<li>AI strengthens management but doesn't take responsibility away from people</li>
<li>Process and data first, the model second</li>
<li>AI where it delivers measurable value, not AI for its own sake</li>
</ul>

<h2>How to work with me</h2>
<p><b>I start with “why”.</b> Before discussing a solution, I'll ask which user or business problem we're solving and how we'll know we've solved it. It's not distrust, it's a habit.</p>
<p><b>I like numbers and facts.</b> An opinion without data is a fine starting point, but I want to make decisions based on customer interviews, analytics or an experiment.</p>
<p><b>Sober about AI.</b> If you suggest “adding AI”, I'll ask which process it will improve, how we'll measure the effect and who is responsible when the model is wrong. If there are answers, I'm the first to support it.</p>
<p><b>Feedback — directly.</b> If something is wrong with the product, the process or my work, tell me right away and to the point. I give feedback the same way: specifically, with a suggestion for what to change.</p>
<p><b>Bad news — early.</b> A missed deadline I learn about a week ahead is plan B. The same deadline I learn about on release day is a fire.</p>
<p><b>Communication.</b> I reply fastest on Telegram. I read email, but not instantly. If it's urgent, say so.</p>
<p><b>Meetings.</b> A meeting needs a goal and an outcome: at the end we write down who does what and by when.</p>
<p class="about-rule">If you're unsure whether to message me — message me.</p>
</div>
<p class="related-row">More about me: <a href="assets/Ponurov_Roman_CV.pdf" target="_blank" rel="noopener">CV (PDF, Russian)</a> · <a href="cases/index.html">case portfolio</a> · <a href="research.html">research</a> · <a href="agents.html">AI agents</a></p>
</div></article>
"""
        return B.layout("About me — Roman Ponurov", "How to work with me: principles, feedback, communication and meetings.", body, "about.html")

    def now_page(posts):
        body = f"""
<article class="page"><div class="wrap">
<a class="back" href="./">Home</a>
<h1>Now</h1>
<p class="post-meta">Updated 16 October 2026</p>
<div class="prose now">
<p>What I'm busy with these weeks. I update this page once a month — the idea comes from Derek Sivers' <a href="https://nownownow.com/about" target="_blank" rel="noopener">now pages</a>.</p>

<h2>🧑‍💼 Work</h2>
<p>Senior product manager at Gazprombank: I'm developing an internal corporate credit analysis service with an AI agent.</p>

<h2>🎓 Teaching</h2>
<p>I teach an <a href="blog/lekcii-it-menedzhment.html">IT Management</a> course for first-year students: seven lectures on Tuesdays until 24 November. Students work in teams to launch their own service — from forming a team and an MVP to metrics.</p>

<h2>🔬 Research</h2>
<p>I'm writing my dissertation at RANEPA on AI in company management. I've just finished a series of interviews for the case study — <a href="blog/intervyu-ii-v-banke.html">findings here</a>. In September I spoke at two international conferences.</p>

<h2>🤖 Building</h2>
<p>I'm developing <a href="projects.html">Weekend Planner</a> — an agentic Telegram bot with an MCP server, A2A agents and evals — and documenting my <a href="agents.html">path into AI agents</a>.</p>

<h2>📚 Reading</h2>
<p>Rereading Marty Cagan's <a href="blog/vdohnovlennye-kagan.html">Inspired</a>.</p>
</div>
{B.year_block(posts)}
</div></article>
"""
        return B.layout("Now — Roman Ponurov", "What Roman Ponurov is doing now: work, teaching, research, projects, reading.", body, "now.html")

    def short_date(p):
        y, mo, d = (int(x) for x in p["date"].split("-"))
        return f"{d} {B.MONTHS_SHORT[mo - 1]} {y}"

    def plural(n, one, few, many):
        word = {"пост": "post", "кейс": "case"}.get(one, one)
        return f"{n} {word}{'' if n == 1 else 's'}"

    for f in (cv_page, projects_page, research_page, study_page, about_page, now_page, short_date, plural):
        setattr(B, f.__name__, f)
