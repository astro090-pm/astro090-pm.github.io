# bolz.dev: an MCP connector that lets AI agents take real-world actions

**Co-founder & CPO** · bolz.dev · 2025 (startup)

| | |
|---|---|
| **Product** | a Model Context Protocol (MCP) platform: services connect once, and AI agents find, book and pay for them on the user's behalf |
| **Stage** | MVP built in August 2025 |
| **Models** | B2B (services and e-commerce) and B2C (AI assistant users) |
| **Predecessor** | [bolz.tech](bolz-tech.html) — sharing ecosystem |

## Problem

AI agents can search and recommend, but rarely finish the job:

- **Agents:** almost always send the user to a website link to complete the action; the best models succeed at real-world tasks less than half the time (MCP-Universe benchmark).
- **Services:** most companies risk not appearing in agent answers at all.
- **Users:** buying a flight via an AI agent today takes longer than doing it yourself — the agent imitates a human: search, links, forms.

## Solution

Bolz Connector sits between agents and services:

- services connect once via plugins, a web interface or REST API;
- agents get normalised JSON, live prices and functions "search / reserve / confirm / refund / pay";
- users go from request to payment in a single conversation.

We designed two scenarios — a marketplace ("find a housewarming gift under $100") and taxi ("call a Comfort car, avoid traffic"). Quality is measured with execution-based evals: success is a completed action, not a model's answer.

## What I did as CPO

- Framed the problem from three sides — services, agents, users — and the value proposition for each.
- Designed user flows from chat request to confirmed payment.
- Described the architecture: agent → MCP server with service connectors → action → result check.
- Analysed competitors: direct (Notte, Firecrawl) and indirect (Google's own AI services, Grab, Loman.ai).
- Built the go-to-market: connector in Claude and ChatGPT, API integrations, sandbox and tutorials for developers.

## What this case shows

A product at the core of the agent layer: MCP, agent tools, outcome-based evaluation and product metrics for agentic scenarios.
