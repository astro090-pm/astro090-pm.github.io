---
title: bolz.dev — an MCP connector that lets AI agents take real-world actions
date: 2025-08-31
thumb: assets/posts/en/bolz-dev.png
tags: startup, AI agents, AI
stage: 4
---

In August 2025 we built the MVP of bolz.dev — a Model Context Protocol platform that lets AI agents not just recommend but finish the job: find, book and pay for real services.

## The problem

Agents are great at search but almost always end by sending the user to a website link — "take it from here". The best models complete real-world tasks less than half the time (MCP-Universe benchmark). Buying a flight via an AI agent today takes longer than doing it yourself: the agent imitates a human — search, links, forms.

On the other side are services: most companies risk not appearing in agent answers at all and losing customers.

## The solution

Bolz Connector sits between agents and services:

- a service connects once — via a plugin, web interface or REST API;
- the agent gets normalised data, live prices and functions "search / reserve / confirm / refund / pay";
- the user goes from request to payment to done in a single conversation.

We designed two scenarios: a marketplace ("find a housewarming gift under $100") and taxi ("call a Comfort car and avoid traffic").

## How to measure quality

The key lesson: for such an agent, judging the model's answer isn't enough. Success is a completed action: a paid order, a car on its way, a purchased ticket. So we built in execution-based evals — checking the outcome, not the text.

## Why it matters to me

bolz.dev grew out of bolz.tech, our sharing ecosystem: we saw users increasingly arrive via AI assistants rather than apps. For me it's also the most direct experience in the agent layer: MCP, agent tools, evals and metrics for agentic scenarios. I later applied the same approach in the [Weekend Planner](../projects.html).

More in the [bolz.dev case study](../cases/bolz-dev.html) and the [AI agents](../agents.html) section.
