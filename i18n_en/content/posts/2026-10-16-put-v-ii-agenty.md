---
title: Starting to document my path into AI agents
date: 2026-10-16
thumb: assets/posts/agents.jpg
tags: AI agents, AI, product
---

I'm opening the [AI agents](../agents.html) section. In it I'll describe step by step how I learn agents: from theory to practice.

## Why agents

I've been launching products for six years and now build a service with an AI agent at a bank. Agents change how products are built: users increasingly don't press buttons but set a task, and the system decides which steps to take. A product manager in such a team needs more than understanding users and metrics — you need to understand how the agent makes decisions, where it fails and how to measure it.

## How the section works

It's a map of twelve stages: from how language models work to an agent in production. For each stage — a short explanation, a link to the code where I tried it hands-on, and notes.

My practice ground is the [Weekend Planner](../projects.html): a Telegram bot that builds an hour-by-hour weekend plan. Inside, three agents talk over the A2A protocol, tools live in a custom MCP server, and 32 eval cases check quality. I've already tried nine of the twelve stages on it; ahead are memory and RAG, observability and safety, and launching with real users.

## What's next

Each stage will get its own note: what I understood, where I got it wrong and what I'd do differently. The first is about the key question: when does a product need an agent, and when is a regular flow enough?
