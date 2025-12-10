# README

## Problem Statement
Design and implement a modular agentic automation system that takes a single product dataset and produces structured machine readable content pages. The system must demonstrate multi agent workflows, reusable content logic, template based generation, and clear orchestration. The goal is to show system design and engineering ability rather than domain research.

## Solution Overview
This project implements a linear agent pipeline that transforms one product object into three JSON pages. The pipeline uses small agents with single responsibilities and a central orchestrator that passes explicit payloads. The system produces:
* An answered FAQ page
* A product description page
* A comparison page with a fictional competitor

All outputs are deterministic or grounded in product fields. The generator avoids external factual enrichment.

## Scopes and Assumptions
* Input is a single product JSON object with fixed fields
* No external web calls are used to enrich facts
* Fictional competitor is created only when a second product is not provided
* All agents operate on structured data only
* Output must be valid JSON and include minimal metadata

## System Design

### High level architecture
The system is organized into three layers
1. Data layer that stores the input product object
2. Agent layer with small independent agents
3. Orchestration layer that runs agents in sequence and writes outputs

Visual flow
Product JSON → Orchestrator → Question Agent → FAQ Agent → Product Page Agent → Comparison Agent → Writer → Outputs


### Agent responsibilities
* Question Agent
  * Input product model
  * Produce categorized question lists
  * Output a simple JSON of categories and questions
* FAQ Agent
  * Input product model and question lists
  * Produce fully answered, grouped FAQ JSON
  * Enforce safe and concise language using product fields only
* Product Page Agent
  * Input product model
  * Produce a structured product page JSON with highlights ingredients usage safety and price
* Comparison Agent
  * Input product model and optional product B
  * If product B is missing the agent generates a realistic fictional competitor
  * Produce a structured comparison JSON listing similarities differences and recommendations
* Writer
  * Persist final JSON files
  * Add generation metadata such as ISO timestamp and system version

### Data model
* Canonical product model fields
  * product_name string
  * concentration string
  * skin_type array of strings
  * key_ingredients array of strings
  * benefits array of strings
  * how_to_use string
  * side_effects string
  * price numeric

All agents accept and return plain JSON compatible objects based on this model.

### Template engine
Templates are simple JSON schemas stored in templates files. Each template defines required fields and where block outputs are placed. Templates are rendered by a template agent that composes block objects into the final shape.

### Orchestration
The orchestrator performs these steps
1. Load and validate the product JSON into the canonical model
2. Call Question Agent to obtain categorized questions
3. Call FAQ Agent to generate answered FAQ JSON
4. Call Product Page Agent to build the product page JSON
5. Call Comparison Agent to build comparison JSON with product B or with a generated competitor
6. Call Writer to persist faq.json product_page.json and comparison_page.json

### Error handling and validation
* All agents validate inputs and raise explicit errors for missing required fields
* Agents sanitize model outputs by stripping markdown wrappers then validating JSON
* The orchestrator catches agent level errors logs them and fails with a clear message

### Testing and evaluation
* Unit tests for
  * parsing and canonical model validation
  * block generation functions
  * template rendering functions
* Integration test that runs the orchestrator end to end and validates output JSON against schemas
* Failure mode tests include invalid input malformed JSON and simulated empty agent response

### Security and secrets
* API keys are loaded from environment variables and never committed
* If an LLM is used the system validates responses before writing outputs

## How to run locally
1. Create a virtual environment and install dependencies
2. Populate data with the product JSON in data folder
3. Run the orchestrator
python -m core.orchestrator

pgsql
Copy code
4. Check outputs in the outputs folder

## Evaluation checklist
* All three JSON pages are produced and valid
* Each FAQ question has a non empty answer
* Comparison page exists and includes a competitor object and comparison fields
* System uses modular agents with no hidden global state
* Tests cover key logic and transformations

## Optional diagrams and notes
Simple sequence diagram
1. Orchestrator invokes Question Agent
2. Orchestrator invokes FAQ Agent with question payload
3. Orchestrator invokes Product Page Agent
4. Orchestrator invokes Comparison Agent
5. Writer persists outputs

End of document
EOF






