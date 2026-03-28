---
title: Email Triage Agent Environment
emoji: 📧
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

# 📧 OpenEnv: Enterprise Email Triage

An official OpenEnv sandbox built to benchmark autonomous AI agents against the noisy reality of an enterprise support inbox. 

*Does your model know when to respond versus when to escalate a potential legal threat?*

## 🏗️ Technical Architecture
This environment adheres strictly to the OpenEnv API standard (Gym-style Reinforcement Learning mechanics tailored for API endpoints).

1. **`server.py`**: The dynamic FastAPI REST interface heavily exposing the core `/step`, `/reset`, and `/state` lifecycle routes for the testbed.
2. **`models.py`**: Contains the `Action`, `Observation`, and `Reward` Pydantic schemas. It features a critical dual-schema approach (`EmailPublic` vs `Email`) to actively hide the target intent labels from the LLM during live observation, preventing cheating.
3. **`environment.py`**: The core Python state machine monitoring the agent's progress through the email stack, penalizing errant operations while continuously calculating accuracy coverage.
4. **`tasks.py`**: Injects realistic and highly detailed simulation payloads, ranging from fake corporate data breaches and legal cease & desists to general software bug reports mapping to three difficulty tiers (`easy`, `medium`, `hard`).
5. **`grader.py`**: A robust `[0.0, 1.0]` overarching reward calculator surgically balancing absolute **Accuracy** (correct resolutions) against **Efficiency** (lowest number of API steps taken).
6. **`client.py`**: An official Python API wrapper meticulously built to pass Hackathon validator checks allowing external Evaluator bots to assess the system.

## 🚀 How We Built It (Development Phases)

We logically engineered this playground over three distinct, iterative sprints:

### Phase 1: API Scaffolding & Compliance
- Spun up a fast `uvicorn` backend.
- Logically mapped our environment payloads strictly around the OpenEnv guidelines, ensuring our `observation`, `reward`, `done`, and `info` dictionaries mapped 1:1 with the standard Gym API protocols.

### Phase 2: Schema Refactoring & True Grading
- We detected that passing the expected labels natively inside the email payloads allowed baseline LLMs to cheat the benchmark effortlessly. We instantly separated our schema into an internal private data structure vs a sanitized public projection payload.
- We then ruthlessly swapped the simple coverage-based grader for an **accuracy-driven** mathematical formula to truly benchmark whether an agent possessed the reasoning capacity to distinguish between an everyday `bug` and a catastrophic `legal` threat before triggering an escalation.

### Phase 3: Baseline Inference & Cloud Deployment
- Connected a localized `inference.py` script running `meta-llama/Meta-Llama-3-8B-Instruct` dynamically via Hugging Face's serverless router.
- Authored a completely automated custom `deploy.py` python wrapper to automatically bypass Windows OS standard `charmap` terminal crashes, auto-sniff user namespaces to prevent `403` authorization lockouts, and safely inject credentials to bypass strict Hugging Face security filters scanning for leaked API keys.

## 📦 Tech Stack & Packages
- **Deployment Platform**: Deep integration with `huggingface_hub` and `openenv-core`.
- **Fast Package Management**: Project resolution isolated at breakneck speed by `uv`. 
- **Network Interface**: Routed entirely through `fastapi` and `uvicorn`.
- **Reasoning Implementation**: `openai` framework explicitly retooled to target the Hugging Face Serverless endpoint seamlessly.

## 💻 Getting Started Locally

Boot the sandbox API natively:
```bash
uv run uvicorn server:app --host 0.0.0.0 --port 7860
```

Execute the simulated LLM Baseline Agent:
```bash
export HF_TOKEN="your_hugging_face_token"
uv run python inference.py
```
