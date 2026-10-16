---
title: What holds AI back in management — findings from interviews at a large bank
date: 2026-10-16
thumb: assets/posts/en/interviews.png
tags: research, AI in management, fintech
---

For the empirical part of my PhD I ran a series of semi-structured interviews inside a large Russian bank. The question is simple: how does AI actually get built into a company's management system — and what gets in the way? Below are generalised findings, without the bank's name, people's names or internal figures.

## The case

**Object.** A large Russian bank with a wide branch network, moving from isolated pilots to systematic use of AI.

**Who I interviewed.** Four groups of respondents:

- product and project managers who implement AI initiatives;
- specialists from the AI technology centre;
- top management;
- employees who use AI tools in their work.

**How.** One interview guide: a common block for everyone and a specialised block per role. Interviews are anonymised, key quotes extracted, answers coded into a thematic matrix — which themes repeat across groups.

## How AI is governed

- **A dedicated structure above departments.** There's an AI centre with its own strategy and a data management function next to it. Strategic goals and adoption KPIs are set at the top and cascade down to department heads.
- **Initiatives come from the business.** A unit brings a problem; together with the AI centre it's turned into an AI task with a target metric. Business units have "AI advocates" — people who know the processes and understand what AI can and can't do.
- **Selection by three criteria:** economic effect, data readiness and process repeatability. If the effect is large but the data isn't ready, the initiative becomes "preparatory": fix data and processes first, then pilot.
- **Accountability stays with the business.** If AI scoring is built into the lending process, the risk manager owns the decision. AI is a tool, not the accountable party.

## Where AI already works

Maturity differs a lot by area. Classic machine learning has long been in production: anti-fraud, scoring, speech analytics in the contact centre. Generative AI is moving from pilots to scale: internal assistants for staff, document summarisation, drafts of analytical reports. Agentic systems are at an early pilot stage.

## Five barriers

1. **Process, not the model.** The most common answer: the blocker isn't model accuracy but the lack of a business process where the output becomes a step rather than "one more dashboard for reference". It's an organisational problem, and it's slow to fix because it touches people's areas of responsibility.
2. **Data.** In a pilot the data is pulled by hand; production needs an automated pipeline — and it turns out sources update at the wrong frequency and have no availability guarantees.
3. **People and trust.** Employees either blindly trust the model's suggestion — making its error their error — or ignore it. A tool can be technically available for months while only a small share of staff use it. Plus a shortage of specialists and dependence on a few experts.
4. **Line managers.** Adoption hinges on line managers: if they don't understand what AI can and can't do, "pseudo-AI" initiatives appear and real opportunities are missed.
5. **Regulation and security.** Customers' personal data rules out external models — you need a closed environment, which limits model choice. Final decisions need explainability and a fallback: why the model decided this and how to challenge it. Models drift with the portfolio and the economy and need constant monitoring.

## Takeaways

- **Autonomous AI-based management decisions are unacceptable in a bank today.** The model is an adviser: it collects and structures information, highlights risks, double-checks data. The decision stays with a human.
- **A gap between the model and the decision is normal, not a failure.** The model optimises one objective; a management decision balances several, some of which can't be formalised.
- **Start narrow.** An example from the interviews: instead of a churn model for the whole portfolio, it was launched for one segment and one channel where data and a retention process already existed. A smaller but measurable and fast effect — and the right to scale.
- **If you change one thing** — build AI literacy into line managers' planning and create a single platform of reusable components so a new initiative launches in weeks, not months.

## What it means for a product manager

Almost all barriers are product problems, not technical ones: which process the output plugs into, who owns it, how users know when to trust the model, which metric defines success. I follow the same principles building a service with an AI agent at work and in my [own AI projects](../agents.html).

More about the PhD on the [research](../research.html) page. I wrote about AI risks in banks in an [article](statya-riski-ii.html) and a [talk](doklad-riski-ii-banki.html).
