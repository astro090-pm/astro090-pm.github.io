"""Блоки личного бренда (ТЗ от 17.10.2026): первый экран, «Мой путь в ИИ», «Мой путь в коучинге»,
«Студентам» и подробный кейс Планировщика выходных. Каждый текст — на двух языках (ru/en).

Правило: только подтверждённые факты. Статусы: done — работает / есть опыт, proto — прототип,
part — частично, wip — в процессе, plan — планируется.
"""
from __future__ import annotations

import html

esc = lambda s: html.escape(s, quote=True)
GH = "https://github.com/astro090-pm"
WP = GH + "/weekend-planner"

ST = {
    "ru": {"done": "Есть опыт", "practice": "Есть практика", "proto": "Прототип", "part": "Частично", "wip": "В процессе",
           "plan": "Планируется", "live": "Работает", "closed": "Участие завершено", "ready": "Проверено на практике",
           "draft": "Черновик", "example": "Пример из практики"},
    "en": {"done": "Experienced", "practice": "Practised", "proto": "Prototype", "part": "Partly", "wip": "In progress",
           "plan": "Planned", "live": "Live", "closed": "Past involvement", "ready": "Tested in practice",
           "draft": "Draft", "example": "Real-world example"},
}
ST_CLS = {"done": "ok", "practice": "ok", "live": "ok", "ready": "ok", "proto": "mid", "part": "mid", "wip": "mid",
          "example": "mid", "plan": "plan", "draft": "plan", "closed": "off"}


def badge(key: str, L: str) -> str:
    return f'<span class="st st-{ST_CLS[key]}">{esc(ST[L][key])}</span>'


# ---------------------------------------------------------------- первый экран
def hero(L: str) -> str:
    t = {
        "ru": ("Роман Понуров", "От бизнес-задачи до работающего ИИ-продукта.",
               "Я занимаюсь продуктовыми задачами, исследую применение искусственного интеллекта и создаю прикладные решения — от проверки гипотез до работающих прототипов.",
               "Смотреть проекты", "Читать исследования"),
        "en": ("Roman Ponurov", "From a business problem to a working AI product.",
               "I work on product problems, research how artificial intelligence is applied and build practical solutions — from testing hypotheses to working prototypes.",
               "See projects", "Read research"),
    }[L]
    return f"""<section class="hero-brand" aria-labelledby="hero-h">
<p class="kicker">Product Management · Applied AI · Engineering</p>
<p class="hero-name"><img class="avatar" src="assets/avatar-sm.jpg" width="48" height="48" alt="">{esc(t[0])}</p>
<h1 id="hero-h">{esc(t[1])}</h1>
<p class="hero-lead">{esc(t[2])}</p>
<p class="hero-cta"><a class="btn btn-main" href="projects.html">{esc(t[3])}</a><a class="btn" href="research.html">{esc(t[4])}</a></p>
</section>"""


def directions(L: str) -> str:
    rows = {
        "ru": ("Направления", [
            ("agents.html", "Мой путь в ИИ", "От продакта к AI Product Engineer: дорожная карта, проекты, дневник практики."),
            ("coaching.html", "Мой путь в коучинге", "Маршрут к профессиональным стандартам ICF. Сейчас — этап планирования."),
            ("students.html", "Студентам", "Учебный маршрут по AI Product Engineering и формат практических материалов."),
        ]),
        "en": ("Directions", [
            ("agents.html", "My path into AI", "From product manager to AI Product Engineer: roadmap, projects, practice log."),
            ("coaching.html", "My path into coaching", "A route towards ICF professional standards. Currently at the planning stage."),
            ("students.html", "For students", "A learning route for AI Product Engineering and the format of practical materials."),
        ]),
    }[L]
    links = "".join(f'<a class="xlink" href="{u}"><b>{esc(t)}</b><span>{esc(d)}</span></a>' for u, t, d in rows[1])
    return f'<section class="dirs" aria-labelledby="dirs-h"><h2 id="dirs-h" class="sec-h">{esc(rows[0])}</h2><div class="xlinks xlinks-3">{links}</div></section>'


# ---------------------------------------------------------------- «Мой путь в ИИ»
AI = {
    "ru": {
        "title": "Мой путь в ИИ",
        "intro": "Шесть лет я запускаю продукты, а сейчас развиваю в банке сервис с ИИ-агентом. Чтобы ставить задачи ИИ-продуктам и честно оценивать их, мне мало продуктовой стороны — нужно понимать, как такие системы устроены изнутри. Поэтому я учусь собирать их сам: от гипотезы до прототипа с тестами и эвалами. Здесь не список курсов, а то, что сделано руками, как это проверялось и что я понял.",
        "start_h": "Точка старта",
        "start": [
            "6+ лет в продакт-менеджменте: B2C, B2B, B2E и B2G — <a href=\"cases/index.html\">кейсы</a>.",
            "Первый технический опыт — системный аналитик в Концерне ГРАНИТ (2019–2020): BPMN, требования, прототипы интерфейсов, тестирование.",
            "Курсы: Pendo.io «AI for Product Management» (2024), ProductDo «Технические знания для продакта» и GoPractice «Симулятор SQL» (2025) — <a href=\"study.html\">образование</a>.",
            "С 2024 года — продуктовая роль в сервисе кредитного анализа с ИИ-агентом в Газпромбанке; в 2025 году — CPO <a href=\"cases/bolz-dev.html\">bolz.dev</a>, MCP-коннектора для ИИ-агентов.",
        ],
        "map_h": "Дорожная карта компетенций",
        "map_note": "Это план развития, а не заявление об уровне. Статус ставлю только там, где есть проверяемое подтверждение — код, тесты или опубликованный кейс.",
        "cols": ("Этап", "Что входит", "Статус", "Подтверждение"),
        "map": [
            ("Продуктовый фундамент", "Пользовательские проблемы, гипотезы, метрики, экономика продукта", "done",
             '<a href="cases/index.html">8 кейсов</a>, <a href="tools.html">инструментарий</a>'),
            ("Технические основы", "Python, терминал, Git и GitHub, API, переменные окружения, тестирование", "practice",
             f'<a href="projects/weekend-planner.html">Планировщик выходных</a>: Python 3.13, ключи в .env, 55 юнит-тестов и CI в GitHub Actions'),
            ("Работа с языковыми моделями", "Вызовы моделей, контекст, ограничения, обработка ошибок", "practice",
             "Структурированные ответы, вызов инструментов, ретраи и цепочка запасных моделей; OpenAI-совместимый API и GigaChat"),
            ("Создание ИИ-приложений", "Серверная логика, интерфейс, интеграции, данные", "proto",
             "Telegram-бот, собственный MCP-сервер, агенты по A2A, данные KudaGo, Open-Meteo и OpenStreetMap"),
            ("RAG и поиск по документам", "Подготовка документов, поиск, передача контекста модели", "plan", "—"),
            ("Оценка качества", "Тестовые наборы, корректность ответов, задержка, стоимость, отказоустойчивость", "part",
             "32 эвал-кейса, таксономия провалов, LLM-as-judge; метрики задержки и токенов заложены, на реальных пользователях ещё не измерялись"),
            ("Развёртывание, наблюдаемость, безопасность", "Деплой, мониторинг, трассировка, защита, сопровождение", "part",
             "Есть Dockerfile, защита от prompt injection и SSRF; трассировка и работа на реальных пользователях — впереди"),
        ],
        "proj_h": "Текущие проекты",
        "proj": [
            ("projects/weekend-planner.html", "Планировщик выходных", "proto", "Агентный Telegram-бот: MCP, A2A, браузерный агент, эвалы. MVP — октябрь 2026, код открыт."),
            ("cases/bolz-dev.html", "bolz.dev", "proto", "MCP-коннектор для реальных действий ИИ-агентов; MVP в августе 2025. Роль — сооснователь и CPO."),
            ("https://github.com/astro090-pm/astro090-pm.github.io", "Этот сайт", "live", "Статический генератор на Python, двуязычная версия, поиск без сервера. Собран с ИИ-ассистентом для кода."),
        ],
        "log_h": "Дневник практики",
        "log_intro": "Записи о том, что сделано и что понял. Новые записи — по шаблону ниже.",
        "tpl_sum": "Шаблон записи дневника",
        "tpl": ["Дата", "Цель", "Что сделано", "Технические решения", "Что реально заработало", "Как проверял",
                "Проблемы и ограничения", "Выводы", "Следующий шаг", "Ссылки на код или демо (если есть)"],
        "tpl_how": "Чтобы добавить запись: создать файл content/posts/ГГГГ-ММ-ДД-slug.md с тегом «ИИ-агенты» и заполнить разделы. Пост сам появится здесь и в ленте.",
        "map2_h": "Карта пути: ИИ-агенты",
        "map2_note": "Подробная карта по агентам — двенадцать этапов от устройства LLM до агента в продакшене.",
        "next_h": "Выводы и следующие шаги",
        "lessons": [
            "<b>Факты — от кода, выбор — от модели.</b> В Планировщике модель выбирает только id найденных мест и событий, а названия, цены и время подставляет код. Это главная защита от галлюцинаций.",
            "<b>Код блокирует, LLM советует.</b> 18 детерминированных проверок плана стабильны и дёшевы; LLM-ревью может ошибаться, поэтому само по себе не запускает правки.",
            "<b>Workflow там, где путь известен, агент — где решать по ходу.</b> Так каждую стадию можно измерить и починить отдельно.",
        ],
        "next": "Дальше по карте: память и RAG, наблюдаемость и безопасность, запуск агента на реальных пользователях — с A/B-тестами и экономикой.",
    },
    "en": {
        "title": "My path into AI",
        "intro": "I've been launching products for six years, and now I'm developing a service with an AI agent at a bank. To set goals for AI products and evaluate them honestly, the product side isn't enough — I need to understand how these systems work inside. So I'm learning to build them myself: from a hypothesis to a prototype with tests and evals. This isn't a list of courses but what I've built hands-on, how it was tested and what I learned.",
        "start_h": "Starting point",
        "start": [
            "6+ years in product management: B2C, B2B, B2E and B2G — <a href=\"cases/index.html\">cases</a>.",
            "First technical experience: systems analyst at Concern GRANIT (2019–2020) — BPMN, requirements, interface prototypes, testing.",
            "Courses: Pendo.io “AI for Product Management” (2024), ProductDo “Technical knowledge for PMs” and the GoPractice SQL simulator (2025) — <a href=\"study.html\">education</a>.",
            "Since 2024, a product role on a credit analysis service with an AI agent at Gazprombank; in 2025, CPO of <a href=\"cases/bolz-dev.html\">bolz.dev</a>, an MCP connector for AI agents.",
        ],
        "map_h": "Competency roadmap",
        "map_note": "This is a development plan, not a claim about my level. I only set a status where there is verifiable evidence — code, tests or a published case.",
        "cols": ("Stage", "What it covers", "Status", "Evidence"),
        "map": [
            ("Product foundations", "User problems, hypotheses, metrics, product economics", "done",
             '<a href="cases/index.html">8 cases</a>, <a href="tools.html">toolkit</a>'),
            ("Technical basics", "Python, terminal, Git and GitHub, APIs, environment variables, testing", "practice",
             '<a href="projects/weekend-planner.html">Weekend Planner</a>: Python 3.13, keys in .env, 55 unit tests and CI on GitHub Actions'),
            ("Working with language models", "Model calls, context, limitations, error handling", "practice",
             "Structured output, tool calling, retries and a chain of fallback models; OpenAI-compatible API and GigaChat"),
            ("Building AI applications", "Backend logic, interface, integrations, data", "proto",
             "A Telegram bot, my own MCP server, A2A agents, data from KudaGo, Open-Meteo and OpenStreetMap"),
            ("RAG and document search", "Preparing documents, retrieval, passing context to the model", "plan", "—"),
            ("Quality evaluation", "Test sets, answer correctness, latency, cost, resilience", "part",
             "32 eval cases, failure taxonomy, LLM-as-judge; latency and token metrics are instrumented but not yet measured on real users"),
            ("Deployment, observability, security", "Deploy, monitoring, tracing, protection, maintenance", "part",
             "A Dockerfile, protection against prompt injection and SSRF; tracing and real-user operation are still ahead"),
        ],
        "proj_h": "Current projects",
        "proj": [
            ("projects/weekend-planner.html", "Weekend Planner", "proto", "An agentic Telegram bot: MCP, A2A, a browser agent, evals. MVP in October 2026, open source."),
            ("cases/bolz-dev.html", "bolz.dev", "proto", "An MCP connector for real-world AI agent actions; MVP in August 2025. Role: co-founder and CPO."),
            ("https://github.com/astro090-pm/astro090-pm.github.io", "This website", "live", "A static generator in Python, a bilingual version, search without a server. Built with an AI coding assistant."),
        ],
        "log_h": "Practice log",
        "log_intro": "Notes on what was done and what I learned. New entries follow the template below.",
        "tpl_sum": "Practice log entry template",
        "tpl": ["Date", "Goal", "What was done", "Technical decisions", "What actually worked", "How it was tested",
                "Problems and limitations", "Conclusions", "Next step", "Links to code or demo (if any)"],
        "tpl_how": "To add an entry: create content/posts/YYYY-MM-DD-slug.md with the “AI agents” tag and fill in the sections. The post appears here and in the feed automatically.",
        "map2_h": "Roadmap: AI agents",
        "map2_note": "A detailed agent roadmap — twelve stages from how LLMs work to an agent in production.",
        "next_h": "Conclusions and next steps",
        "lessons": [
            "<b>Facts come from code, choices from the model.</b> In Weekend Planner the model only picks the ids of places and events that were found; names, prices and times are filled in by code. This is the main protection against hallucinations.",
            "<b>Code blocks, the LLM advises.</b> 18 deterministic plan checks are stable and cheap; the LLM review can be wrong, so on its own it doesn't trigger fixes.",
            "<b>A workflow where the path is known, an agent where decisions are made on the fly.</b> That way each stage can be measured and fixed separately.",
        ],
        "next": "Next on the map: memory and RAG, observability and safety, running the agent with real users — with A/B tests and unit economics.",
    },
}


def ai_top(L: str) -> str:
    T = AI[L]
    start = "".join(f"<li>{s}</li>" for s in T["start"])
    rows = "".join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{badge(s, L)}</td><td>{ev}</td></tr>' for a, b, s, ev in T["map"])
    proj = "".join(f'<li class="card proj-card"><p class="card-meta">{badge(s, L)}</p><h3 class="card-title"><a href="{u}">{esc(n)}</a></h3><p class="card-about">{esc(d)}</p></li>'
                   for u, n, s, d in T["proj"])
    c = T["cols"]
    return f"""<p class="intro">{esc(T['intro'])}</p>
<h2>{esc(T['start_h'])}</h2>
<ul class="facts">{start}</ul>
<h2>{esc(T['map_h'])}</h2>
<p class="intro">{esc(T['map_note'])}</p>
<div class="tbl-wrap"><table class="roadmap"><thead><tr><th scope="col">{c[0]}</th><th scope="col">{c[1]}</th><th scope="col">{c[2]}</th><th scope="col">{c[3]}</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>{esc(T['proj_h'])}</h2>
<ul class="cards proj-cards">{proj}</ul>"""


def template_box(summary: str, fields: list[str], how: str) -> str:
    lis = "".join(f"<li>{esc(f)}</li>" for f in fields)
    return f'<details class="tpl"><summary>{esc(summary)}</summary><ol>{lis}</ol><p>{esc(how)}</p></details>'


def ai_log_head(L: str) -> str:
    T = AI[L]
    return f'<h2>{esc(T["log_h"])}</h2><p class="intro">{esc(T["log_intro"])}</p>'


def ai_bottom(L: str, stages_html: str) -> str:
    T = AI[L]
    lessons = "".join(f"<li>{s}</li>" for s in T["lessons"])
    return f"""{template_box(T['tpl_sum'], T['tpl'], T['tpl_how'])}
<h2 class="stages-head">{esc(T['map2_h'])}</h2>
<p class="intro">{esc(T['map2_note'])}</p>
{stages_html}
<h2>{esc(T['next_h'])}</h2>
<ul class="facts">{lessons}</ul>
<p class="intro">{esc(T['next'])}</p>"""


# ---------------------------------------------------------------- «Мой путь в коучинге»
ICF = {
    "core": "https://coachingfederation.org/credentialing/coaching-competencies/icf-core-competencies/",
    "ethics": "https://coachingfederation.org/credentialing/coaching-ethics/icf-code-of-ethics/",
    "acc": "https://coachingfederation.org/credentialing/icf-credentials-overview/acc/",
    "paths": "https://coachingfederation.org/icf-credential/acc-paths",
}
COACH = {
    "ru": {
        "title": "Мой путь в коучинге",
        "status": "Статус направления",
        "intro": "Эта страница дополняет основную линию сайта — продукты и ИИ. Здесь я буду открыто фиксировать путь в бизнес-коучинге: обучение, практику и рефлексию, ориентируясь на профессиональные стандарты Международной федерации коучинга (ICF).",
        "honest": "Важно: я не заявляю о наличии credential ICF и не предлагаю на этом сайте коучинговые услуги. Этапы ниже — план; каждый будет отмечен как пройденный только с датой и подтверждением.",
        "goal_h": "Зачем мне это",
        "goal": "Я управлял командами до 50 человек, а сейчас преподаю курс «ИТ-менеджмент» первокурсникам. Коучинговый подход — умение задавать вопросы, а не давать готовые ответы, — нужен и в управлении продуктом, и в преподавании. Хочу освоить его системно, по стандартам профессии.",
        "route_h": "Маршрут",
        "route_note": "Ориентир — первый уровень ICF, Associate Certified Coach (ACC). Требования приведены по официальному сайту ICF на октябрь 2026 года; перед каждым шагом сверяю их заново.",
        "route": [
            ("Выбрать программу обучения", "Аккредитованную ICF (Level 1 или Level 2) или с часами Continuing Coach Education — от этого зависит путь подачи заявки"),
            ("Обучение коучингу", "Не менее 60 часов"),
            ("Практика", "100 часов коучинга с клиентами, из них не менее 75 оплачиваемых"),
            ("Ментор-коучинг", "10 часов с опытным коучем в течение не менее трёх месяцев"),
            ("Оценка практики и экзамен", "Оценка записи сессии (performance evaluation) и экзамен ICF ACC"),
            ("Заявка на ACC", "Подача через ICF после выполнения всех требований"),
        ],
        "diff_h": "Три разные вещи, которые легко спутать",
        "diff": [
            ("Обучение", "Курс или программа, которую человек прошёл. Говорит о полученных знаниях, но не о квалификации."),
            ("Сертификат программы", "Документ школы об окончании обучения. Это не квалификация ICF, даже если программа аккредитована ICF."),
            ("Credential ICF", "Индивидуальная профессиональная квалификация (ACC, PCC, MCC), которую выдаёт сама ICF после обучения, практики, ментор-коучинга, оценки и экзамена."),
        ],
        "practice_h": "Практика и этика",
        "practice": "Учебные разборы появятся здесь только обезличенными и с согласия участников, без деталей сессий. Отзывы и кейсы клиентов на сайте не публикуются.",
        "std_h": "Стандарты ICF — официальные источники",
        "std": [("core", "Ключевые компетенции ICF"), ("ethics", "Этический кодекс ICF"), ("acc", "Требования к ACC"), ("paths", "Пути получения ACC")],
        "refl_h": "Журнал рефлексии",
        "refl_intro": "Записей пока нет — журнал начнётся вместе с обучением. Формат записи:",
        "tpl_sum": "Шаблон записи рефлексии",
        "tpl": ["Дата", "Что практиковал (упражнение, учебная сессия)", "Какая компетенция ICF", "Что получилось",
                "Что не получилось", "Вопрос к ментору", "Следующий шаг"],
        "tpl_how": "Чтобы добавить запись: создать файл content/posts/ГГГГ-ММ-ДД-slug.md с тегом «коучинг». Без имён и деталей, по которым можно узнать человека.",
        "posts_h": "Записи",
        "desc": "Путь Романа Понурова в бизнес-коучинге: маршрут к стандартам ICF, практика и рефлексия. Статус — планирование.",
    },
    "en": {
        "title": "My path into coaching",
        "status": "Status",
        "intro": "This page complements the site's main line — products and AI. Here I'll openly document my path into business coaching: learning, practice and reflection, guided by the professional standards of the International Coaching Federation (ICF).",
        "honest": "Important: I don't claim to hold an ICF credential and I don't offer coaching services on this site. The stages below are a plan; each will be marked as done only with a date and evidence.",
        "goal_h": "Why I'm doing this",
        "goal": "I've led teams of up to 50 people, and now I teach an IT Management course to first-year students. The coaching approach — asking questions instead of handing out ready answers — matters both in product management and in teaching. I want to learn it systematically, to professional standards.",
        "route_h": "Route",
        "route_note": "The target is ICF's first level, Associate Certified Coach (ACC). Requirements are taken from the official ICF website as of October 2026; I re-check them before each step.",
        "route": [
            ("Choose a training programme", "ICF-accredited (Level 1 or Level 2) or one with Continuing Coach Education hours — this determines the application path"),
            ("Coach training", "At least 60 hours"),
            ("Practice", "100 hours of coaching with clients, at least 75 of them paid"),
            ("Mentor coaching", "10 hours with an experienced coach over at least three months"),
            ("Performance evaluation and exam", "Evaluation of a recorded session and the ICF ACC exam"),
            ("ACC application", "Submitted to ICF once all requirements are met"),
        ],
        "diff_h": "Three different things that are easy to confuse",
        "diff": [
            ("Training", "A course or programme someone completed. It shows knowledge gained, not a qualification."),
            ("Programme certificate", "A school's document confirming completion. It is not an ICF qualification, even if the programme is ICF-accredited."),
            ("ICF credential", "An individual professional qualification (ACC, PCC, MCC) awarded by ICF itself after training, practice, mentor coaching, evaluation and an exam."),
        ],
        "practice_h": "Practice and ethics",
        "practice": "Learning case notes will appear here only anonymised and with participants' consent, without session details. Client testimonials and cases are not published on this site.",
        "std_h": "ICF standards — official sources",
        "std": [("core", "ICF Core Competencies"), ("ethics", "ICF Code of Ethics"), ("acc", "ACC requirements"), ("paths", "ACC application paths")],
        "refl_h": "Reflection log",
        "refl_intro": "No entries yet — the log will start together with training. Entry format:",
        "tpl_sum": "Reflection entry template",
        "tpl": ["Date", "What I practised (exercise, practice session)", "Which ICF competency", "What worked",
                "What didn't", "Question for the mentor", "Next step"],
        "tpl_how": "To add an entry: create content/posts/YYYY-MM-DD-slug.md with the “coaching” tag. No names or details that could identify a person.",
        "posts_h": "Entries",
        "desc": "Roman Ponurov's path into business coaching: a route towards ICF standards, practice and reflection. Status: planning.",
    },
}


def coaching_body(L: str, posts_feed: str) -> str:
    T = COACH[L]
    route = "".join(f'<li><span class="rt-n">{i}</span><div><h3>{esc(a)} {badge("plan", L)}</h3><p>{esc(b)}</p></div></li>'
                    for i, (a, b) in enumerate(T["route"], 1))
    diff = "".join(f'<li class="skill"><b>{esc(a)}</b><span>{esc(b)}</span></li>' for a, b in T["diff"])
    std = " · ".join(f'<a href="{ICF[k]}" target="_blank" rel="noopener">{esc(n)}</a>' for k, n in T["std"])
    refl = (f'<h3>{esc(T["posts_h"])}</h3><ul class="feed">{posts_feed}</ul>' if posts_feed else f'<p class="intro">{esc(T["refl_intro"])}</p>')
    return f"""<p class="status-line">{esc(T['status'])}: {badge('plan', L)}</p>
<p class="intro">{esc(T['intro'])}</p>
<p class="note">{esc(T['honest'])}</p>
<h2>{esc(T['goal_h'])}</h2>
<p class="intro">{esc(T['goal'])}</p>
<h2>{esc(T['route_h'])}</h2>
<p class="intro">{esc(T['route_note'])}</p>
<ol class="route">{route}</ol>
<h2>{esc(T['diff_h'])}</h2>
<ul class="skills">{diff}</ul>
<h2>{esc(T['practice_h'])}</h2>
<p class="intro">{esc(T['practice'])}</p>
<h2>{esc(T['std_h'])}</h2>
<p class="intro">{std}</p>
<h2>{esc(T['refl_h'])}</h2>
{refl}
{template_box(T['tpl_sum'], T['tpl'], T['tpl_how'])}"""


# ---------------------------------------------------------------- «Студентам»
DOCS = [
    ("Python Tutorial", "https://docs.python.org/3/tutorial/"),
    ("Pro Git", "https://git-scm.com/book/ru/v2"),
    ("GitHub Docs", "https://docs.github.com/"),
    ("Claude Docs", "https://docs.claude.com/"),
    ("OpenAI API Docs", "https://platform.openai.com/docs"),
    ("Model Context Protocol", "https://modelcontextprotocol.io/"),
]
STU = {
    "ru": {
        "title": "Студентам",
        "intro": "Бесплатная практическая база знаний для тех, кто хочет освоить AI Product Engineering — не только понимать ИИ-продукты, но и создавать, проверять и сопровождать их. Раздел только начинается: ниже учебный маршрут и формат материалов. Готовое помечено, остальное — в плане.",
        "legend_h": "Метки материалов",
        "legend": [("Уровень", "Начальный · Средний · Продвинутый"), ("Статус", "Проверено на практике · Черновик · В процессе"), ("Тип", "Теория · Практика · Проект · Инструмент")],
        "route_h": "Начать здесь: учебный маршрут",
        "route_note": "Это учебный план, а не готовый курс. Где есть реальный пример из моих проектов, даю ссылку.",
        "route": [
            ("Основы Python, терминала, Git и GitHub", "Начальный", [("Python Tutorial", DOCS[0][1]), ("Pro Git", DOCS[1][1])]),
            ("Простое приложение с языковой моделью", "Начальный", [("Планировщик: запуск без ключей на модели-заглушке", WP + "#%D0%B1%D1%8B%D1%81%D1%82%D1%80%D1%8B%D0%B9-%D1%81%D1%82%D0%B0%D1%80%D1%82")]),
            ("API, конфигурация и обработка ошибок", "Средний", [("Планировщик: ретраи и запасные модели", WP + "/blob/main/docs/ARCHITECTURE.md")]),
            ("Работа с документами и поиск по ним (RAG)", "Средний", []),
            ("ИИ-помощник для конкретного сценария", "Средний", [("Кейс: Планировщик выходных", "projects/weekend-planner.html")]),
            ("Тестирование и оценка качества", "Средний", [("Планировщик: 32 эвал-кейса", WP + "/tree/main/evals")]),
            ("Безопасность, стоимость и задержка", "Продвинутый", []),
            ("Развёртывание и кейс в портфолио", "Продвинутый", [("Шаблон кейса на примере Планировщика", "projects/weekend-planner.html")]),
        ],
        "cats_h": "Разделы базы знаний",
        "cats": [
            ("Начать здесь", "Учебный маршрут и порядок тем", [("Маршрут выше", "#route")]),
            ("Технический фундамент", "Python, терминал, Git, GitHub, API и окружение", []),
            ("Языковые модели", "Принципы работы, вызовы моделей, контекст и ограничения", [("Карта пути: ИИ-агенты", "agents.html#stage-1")]),
            ("Данные и RAG", "Подготовка документов, поиск и передача контекста модели", []),
            ("Создание приложений", "Интерфейс, сервер, интеграции и развёртывание", []),
            ("Качество и безопасность", "Тестирование, оценка ответов, приватность, обработка ошибок", []),
            ("Продуктовое мышление", "Постановка задачи, выбор сценария, метрики и экономика", [("Лекция 1 «ИТ-менеджмент», PDF", "assets/decks/it-management-lecture-1.pdf"), ("О курсе", "blog/lekcii-it-menedzhment.html"), ("Инструментарий продакта", "tools.html")]),
            ("Практические проекты", "Пошаговые задания с проверяемым результатом", [("Открытый код Планировщика", WP)]),
            ("Инструменты и источники", "Официальная документация и полезные ресурсы", [("ИИ-скиллы", "skills.html"), ("Документация ниже", "#docs")]),
        ],
        "ready": "Готово:", "planned": "Материалы в плане",
        "tpl_h": "Формат учебного материала",
        "tpl_note": "Каждый материал строится по одному шаблону. Если код не проверен, это пишется прямо в начале.",
        "tpl": ["Что изучаем", "Зачем это нужно AI Product Engineer", "Короткое объяснение", "Пример или схема",
                "Практическое задание", "Полный код, если задание на программирование", "Команды запуска и требования к окружению",
                "Как проверить результат", "Типичные ошибки и как их диагностировать", "Ограничения и дополнительные источники"],
        "docs_h": "Официальная документация",
        "teach": "Я также веду курс «ИТ-менеджмент» в университете — <a href=\"blog/lekcii-it-menedzhment.html\">о курсе</a> и <a href=\"decks.html\">слайды лекций</a>.",
        "desc": "Бесплатная база знаний по AI Product Engineering: учебный маршрут, разделы, формат практических материалов и официальная документация.",
        "step": "Шаг",
    },
    "en": {
        "title": "For students",
        "intro": "A free practical knowledge base for those who want to master AI Product Engineering — not just understand AI products, but build, test and maintain them. The section is just starting: below are the learning route and the material format. What's ready is marked; the rest is planned.",
        "legend_h": "Material labels",
        "legend": [("Level", "Beginner · Intermediate · Advanced"), ("Status", "Tested in practice · Draft · In progress"), ("Type", "Theory · Practice · Project · Tool")],
        "route_h": "Start here: learning route",
        "route_note": "This is a learning plan, not a finished course. Where there's a real example from my projects, I link to it.",
        "route": [
            ("Basics of Python, the terminal, Git and GitHub", "Beginner", [("Python Tutorial", DOCS[0][1]), ("Pro Git", DOCS[1][1])]),
            ("A simple app that uses a language model", "Beginner", [("Weekend Planner: running without keys on a stub model", WP + "#%D0%B1%D1%8B%D1%81%D1%82%D1%80%D1%8B%D0%B9-%D1%81%D1%82%D0%B0%D1%80%D1%82")]),
            ("APIs, configuration and error handling", "Intermediate", [("Weekend Planner: retries and fallback models", WP + "/blob/main/docs/ARCHITECTURE.md")]),
            ("Working with documents and search (RAG)", "Intermediate", []),
            ("An AI assistant for a specific scenario", "Intermediate", [("Case: Weekend Planner", "projects/weekend-planner.html")]),
            ("Testing and quality evaluation", "Intermediate", [("Weekend Planner: 32 eval cases", WP + "/tree/main/evals")]),
            ("Security, cost and latency", "Advanced", []),
            ("Deployment and a portfolio case", "Advanced", [("A case template using Weekend Planner", "projects/weekend-planner.html")]),
        ],
        "cats_h": "Knowledge base sections",
        "cats": [
            ("Start here", "The learning route and order of topics", [("The route above", "#route")]),
            ("Technical foundations", "Python, terminal, Git, GitHub, APIs and environment", []),
            ("Language models", "How they work, model calls, context and limitations", [("Roadmap: AI agents", "agents.html#stage-1")]),
            ("Data and RAG", "Preparing documents, retrieval and passing context to the model", []),
            ("Building applications", "Interface, server, integrations and deployment", []),
            ("Quality and safety", "Testing, answer evaluation, privacy, error handling", []),
            ("Product thinking", "Framing the problem, choosing a scenario, metrics and economics", [("IT Management lecture 1, PDF (Russian)", "assets/decks/it-management-lecture-1.pdf"), ("About the course", "blog/lekcii-it-menedzhment.html"), ("Product toolkit", "tools.html")]),
            ("Practical projects", "Step-by-step assignments with a verifiable result", [("Weekend Planner source code", WP)]),
            ("Tools and sources", "Official documentation and useful resources", [("AI skills", "skills.html"), ("Documentation below", "#docs")]),
        ],
        "ready": "Ready:", "planned": "Materials planned",
        "tpl_h": "Learning material format",
        "tpl_note": "Every material follows one template. If code hasn't been tested, that's stated right at the start.",
        "tpl": ["What we're learning", "Why an AI Product Engineer needs it", "A short explanation", "An example or diagram",
                "A practical assignment", "Full code, if the assignment involves programming", "Run commands and environment requirements",
                "How to check the result", "Common mistakes and how to diagnose them", "Limitations and further sources"],
        "docs_h": "Official documentation",
        "teach": "I also teach an IT Management course at a university — <a href=\"blog/lekcii-it-menedzhment.html\">about the course</a> and <a href=\"decks.html\">lecture slides</a>.",
        "desc": "A free knowledge base on AI Product Engineering: learning route, sections, practical material format and official documentation.",
        "step": "Step",
    },
}


def students_body(L: str) -> str:
    T = STU[L]
    legend = "".join(f'<li><b>{esc(a)}</b> — {esc(b)}</li>' for a, b in T["legend"])
    route = []
    for i, (name, level, links) in enumerate(T["route"], 1):
        ex = (" · ".join(f'<a href="{esc(u)}"{" target=\"_blank\" rel=\"noopener\"" if u.startswith("http") else ""}>{esc(t)}</a>' for t, u in links))
        route.append(f'<li><span class="rt-n">{i}</span><div><h3>{esc(name)}</h3><p class="tags-line"><span class="lbl">{esc(level)}</span>{badge("plan", L)}</p>'
                     + (f'<p>{ex}</p>' if ex else "") + "</div></li>")
    cats = []
    for name, about, links in T["cats"]:
        ready = " · ".join(f'<a href="{esc(u)}"{" target=\"_blank\" rel=\"noopener\"" if u.startswith("http") else ""}>{esc(t)}</a>' for t, u in links)
        cats.append(f'<li class="skill"><b>{esc(name)}</b><span>{esc(about)}</span>'
                    + (f'<em>{esc(T["ready"])} {ready}</em>' if ready else f'<em class="muted">{esc(T["planned"])}</em>') + "</li>")
    tpl = "".join(f"<li>{esc(x)}</li>" for x in T["tpl"])
    docs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in DOCS)
    return f"""<p class="intro">{esc(T['intro'])}</p>
<h2>{esc(T['legend_h'])}</h2>
<ul class="facts">{legend}</ul>
<h2 id="route">{esc(T['route_h'])}</h2>
<p class="intro">{esc(T['route_note'])}</p>
<ol class="route">{"".join(route)}</ol>
<h2>{esc(T['cats_h'])}</h2>
<ul class="skills">{"".join(cats)}</ul>
<h2>{esc(T['tpl_h'])}</h2>
<p class="intro">{esc(T['tpl_note'])}</p>
<ol class="tpl-list">{tpl}</ol>
<h2 id="docs">{esc(T['docs_h'])}</h2>
<ul class="doc-list">{docs}</ul>
<p class="related-row">{T['teach']}</p>"""


# ---------------------------------------------------------------- подробный кейс: Планировщик выходных
WPC = {
    "ru": {
        "title": "Планировщик выходных",
        "lead": "Агентный Telegram-бот, который за минуту собирает план выходных по часам: смотрит погоду, афишу и места, укладывается в бюджет и учитывает возраст детей.",
        "status_l": "Статус",
        "status_t": "MVP собран за три дня в октябре 2026 года, код открыт. На реальных пользователях ещё не запускался — результатов использования пока нет.",
        "sec": [
            ("Проблема и контекст", "<p>Чтобы спланировать выходные, люди 30–40 минут переключаются между афишей, картами и прогнозом погоды. Это оценка из постановки проекта, а не измерение.</p><p><b>Гипотеза:</b> готовым планом по часам за минуту — с учётом погоды, бюджета и детей — будут пользоваться и возвращаться к нему.</p>"),
            ("Аудитория и ключевой сценарий", "<p>Люди, которые планируют выходные в своём городе, — в том числе с детьми; афиша берётся из KudaGo. Сценарий: написать боту «суббота с ребёнком 6 лет, до 3000» и получить расписание со ссылками; если не нравится — «Другой вариант», «Дешевле» или правка своими словами.</p>"),
            ("Моя роль", "<p>Проект мой целиком: постановка задачи, требования, архитектура, код, эвалы и план запуска. Код писал вместе с ИИ-ассистентом для программирования.</p>"),
            ("Требования и критерии успеха", "<ul><li>В плане только реальные события и места — из найденных инструментами.</li><li>Соблюдение бюджета, возраста детей, исключённых категорий и погоды.</li><li>Устойчивость к сбоям моделей и источников данных.</li><li>Продуктовые метрики заложены: activation, time-to-value, return 7d, доля 👍, refine rate. Целевые значения до запуска не зафиксированы.</li></ul>"),
            ("Архитектура и поток данных", "<ol><li>Пользователь пишет в Telegram-бот; оркестратор разбирает запрос в предпочтения (JSON с валидацией).</li><li>Агент-разведчик по протоколу A2A собирает кандидатов через собственный MCP-сервер: погода, афиша, места, чтение страниц браузером.</li><li>Оркестратор собирает план только из реальных id; факты (названия, цены, время) подставляет код.</li><li>Агент-критик по A2A проверяет план: 18 детерминированных проверок и LLM-ревью.</li><li>До двух раундов исправлений; если ошибки остались — ошибочные пункты вырезаются.</li></ol>"),
            ("Технологии", "<p>Python 3.13 · MCP · собственная реализация A2A (JSON-RPC) · Playwright · KudaGo, Open-Meteo, OpenStreetMap · любой OpenAI-совместимый API или GigaChat · Telegram (long polling) · Docker · GitHub Actions.</p>"),
            ("Реализация и код", f'<p>Исходный код, инструкция запуска и документация — <a href="{WP}">в репозитории на GitHub</a>. Подробная архитектура — <a href="{WP}/blob/main/docs/ARCHITECTURE.md">ARCHITECTURE.md</a>, план первых пользователей — <a href="{WP}/blob/main/docs/LAUNCH_PLAN.md">LAUNCH_PLAN.md</a>. Публичного демо нет: бот запускается локально или на VPS со своими ключами.</p>'),
            ("Как проверяется качество", "<ul><li>55 юнит-тестов и CI на каждый коммит (по README).</li><li>32 эвал-кейса на фиксированных данных: бюджет, дети, дождь, даты, неизвестный город, off-topic и prompt injection — в том числе спрятанная на странице события.</li><li>Таксономия провалов, сравнение моделей между прогонами, LLM-as-judge как дополнительный сигнал.</li></ul>"),
            ("Результаты", "<p>Не измерялись: бот ещё не запускался на реальных пользователях. После запуска здесь появятся данные по activation, возвратам и оценкам.</p>"),
            ("Ограничения, риски и безопасность", "<ul><li>Зависимость от внешних источников данных — ретраи, кэш, circuit breaker и запасной источник мест.</li><li>Prompt injection через веб-страницы — текст помечается как недоверенный, а в план попадают только объекты из реестра найденного.</li><li>SSRF — браузерный агент открывает только публичные адреса.</li><li>Стоимость — лимит шагов агента и планов в час на пользователя.</li></ul>"),
            ("Выводы и следующие шаги", "<p>Главный вывод проектирования: модель выбирает, код отвечает за факты — это защищает от галлюцинаций надёжнее промптов. Дальше: запуск на первых пользователях, стриминг ответа и кэш для снижения задержки, трассировка по стадиям, онлайн-эвалы на реальных диалогах.</p>"),
        ],
        "back": "Проекты",
        "fig": "Кто с кем работает внутри бота",
        "desc": "Кейс: агентный Telegram-бот на LLM с MCP-сервером, агентами по A2A и эвалами. Статус — прототип.",
    },
    "en": {
        "title": "Weekend Planner",
        "lead": "An agentic Telegram bot that builds an hour-by-hour weekend plan in a minute: it checks the weather, events and places, stays within budget and takes children's ages into account.",
        "status_l": "Status",
        "status_t": "The MVP was built in three days in October 2026, and the code is open. It hasn't been launched to real users yet, so there are no usage results so far.",
        "sec": [
            ("Problem and context", "<p>To plan a weekend, people spend 30–40 minutes switching between event listings, maps and the weather forecast. This is an estimate from the project brief, not a measurement.</p><p><b>Hypothesis:</b> people will use and come back to a ready hour-by-hour plan made in a minute that accounts for weather, budget and children.</p>"),
            ("Audience and key scenario", "<p>People planning a weekend in their city, including with children; event data comes from KudaGo. Scenario: write to the bot “Saturday with a 6-year-old, under 3,000 roubles” and get a schedule with links; if it doesn't fit — “Another option”, “Cheaper” or a correction in your own words.</p>"),
            ("My role", "<p>The project is entirely mine: problem framing, requirements, architecture, code, evals and launch plan. I wrote the code together with an AI coding assistant.</p>"),
            ("Requirements and success criteria", "<ul><li>Only real events and places found by the tools go into the plan.</li><li>Respecting budget, children's ages, excluded categories and weather.</li><li>Resilience to model and data source failures.</li><li>Product metrics are instrumented: activation, time-to-value, return 7d, 👍 share, refine rate. Target values haven't been set before launch.</li></ul>"),
            ("Architecture and data flow", "<ol><li>The user writes to the Telegram bot; the orchestrator parses the request into preferences (validated JSON).</li><li>A scout agent, over the A2A protocol, collects candidates through my own MCP server: weather, events, places, reading pages with a browser.</li><li>The orchestrator builds a plan only from real ids; facts (names, prices, times) are filled in by code.</li><li>A critic agent over A2A checks the plan: 18 deterministic checks plus an LLM review.</li><li>Up to two rounds of fixes; if errors remain, the faulty items are cut.</li></ol>"),
            ("Technologies", "<p>Python 3.13 · MCP · own A2A implementation (JSON-RPC) · Playwright · KudaGo, Open-Meteo, OpenStreetMap · any OpenAI-compatible API or GigaChat · Telegram (long polling) · Docker · GitHub Actions.</p>"),
            ("Implementation and code", f'<p>Source code, setup instructions and documentation are <a href="{WP}">in the GitHub repository</a> (in Russian). Detailed architecture: <a href="{WP}/blob/main/docs/ARCHITECTURE.md">ARCHITECTURE.md</a>; first-users plan: <a href="{WP}/blob/main/docs/LAUNCH_PLAN.md">LAUNCH_PLAN.md</a>. There is no public demo: the bot runs locally or on a VPS with your own keys.</p>'),
            ("How quality is tested", "<ul><li>55 unit tests and CI on every commit (per the README).</li><li>32 eval cases on fixed data: budget, children, rain, dates, an unknown city, off-topic and prompt injection — including one hidden on an event page.</li><li>Failure taxonomy, model comparison between runs, LLM-as-judge as an additional signal.</li></ul>"),
            ("Results", "<p>Not measured: the bot hasn't been launched to real users yet. After launch, data on activation, returns and ratings will appear here.</p>"),
            ("Limitations, risks and security", "<ul><li>Dependence on external data sources — retries, caching, a circuit breaker and a fallback source for places.</li><li>Prompt injection via web pages — the text is marked as untrusted, and only objects from the registry of found items can enter the plan.</li><li>SSRF — the browser agent opens only public addresses.</li><li>Cost — limits on agent steps and plans per user per hour.</li></ul>"),
            ("Conclusions and next steps", "<p>The main design takeaway: the model chooses, the code is responsible for facts — this protects against hallucinations more reliably than prompts. Next: launch to first users, streaming responses and caching to reduce latency, per-stage tracing, online evals on real conversations.</p>"),
        ],
        "back": "Projects",
        "fig": "Who works with whom inside the bot",
        "desc": "Case: an agentic LLM Telegram bot with an MCP server, A2A agents and evals. Status: prototype.",
    },
}


def wp_case_body(L: str) -> str:
    T = WPC[L]
    secs = "".join(f"<h2>{esc(h)}</h2>{b}" for h, b in T["sec"])
    return f"""<article class="page"><div class="wrap">
<a class="back" href="../projects.html">{esc(T['back'])}</a>
<h1>{esc(T['title'])}</h1>
<p class="lead-p">{esc(T['lead'])}</p>
<p class="status-line">{esc(T['status_l'])}: {badge('proto', L)} <span>{esc(T['status_t'])}</span></p>
<figure class="case-fig"><img src="../assets/weekend-planner-arch.png" width="1344" height="960" alt="{esc(T['fig'])}" loading="lazy"><figcaption>{esc(T['fig'])}</figcaption></figure>
<div class="prose">{secs}</div>
</div></article>"""


# статусы собственных проектов на странице «Проекты» (по фактам из кейсов)
OWN_STATUS = {"po-sosedstvu": "closed", "dobster": "closed", "bolz-dev": "proto", "bolz-tech": "closed"}
OWN_STATUS_NOTE = {
    "ru": {"po-sosedstvu": "моё участие — 2022–2024", "dobster": "моё участие — 2022–2023", "bolz-dev": "MVP — август 2025", "bolz-tech": "моё участие — 2023–2025"},
    "en": {"po-sosedstvu": "my involvement: 2022–2024", "dobster": "my involvement: 2022–2023", "bolz-dev": "MVP, August 2025", "bolz-tech": "my involvement: 2023–2025"},
}
