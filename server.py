# server.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from environment import EmailEnv
from models import Action, Observation, Reward
from grader import grade

app = FastAPI(
    title="OpenEnv Email Triage",
    version="1.0.0",
    description="Enterprise Email Triage OpenEnv Environment",
)


class ResetRequest(BaseModel):
    task: Optional[str] = "easy"


env = EmailEnv()


# ─── Core lifecycle ───────────────────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "OpenEnv Email Triage Running"}


@app.post("/reset")
def reset(body: Optional[ResetRequest] = None):
    task = body.task if body and body.task else "easy"
    obs = env.reset(task)
    return {"observation": obs.model_dump()}


@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward.value,
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    st = env.state()
    return {
        "emails": [e.model_dump() for e in st["emails"]],
        "handled": st["handled"],
        "correct_resolutions": st["correct_resolutions"],
        "steps": st["steps"]
    }


@app.get("/tasks")
def tasks():
    return ["easy", "medium", "hard"]


@app.get("/grader")
def grader():
    return {"score": grade(env.state())}


# ─── openenv validate — runtime endpoints ─────────────────────────────────────

@app.get("/health")
def health():
    """Required by openenv validate: must return {"status": "healthy"}."""
    return {"status": "healthy"}


@app.get("/metadata")
def metadata():
    """Required by openenv validate: must return {"name": str, "description": str}."""
    return {
        "name": "openenv_email",
        "description": (
            "Enterprise Email Triage environment: benchmark autonomous AI agents "
            "against a realistic corporate support inbox."
        ),
    }


@app.get("/schema")
def schema():
    """Required by openenv validate: must return action, observation, and state schemas."""
    return {
        "action": {
            "type": "object",
            "properties": {
                "type": {"type": "string", "description": "Action type: respond, escalate, archive"},
                "email_id": {"type": "string", "description": "ID of the email to act on"},
                "label": {"type": "string", "description": "Optional label for the action"},
            },
            "required": ["type", "email_id"],
        },
        "observation": {
            "type": "object",
            "properties": {
                "inbox": {"type": "array", "items": {"type": "object"}},
                "current_email": {"type": "object"},
                "steps": {"type": "integer"},
            },
        },
        "state": {
            "type": "object",
            "properties": {
                "emails": {"type": "array"},
                "handled": {"type": "array"},
                "correct_resolutions": {"type": "integer"},
                "steps": {"type": "integer"},
            },
        },
    }


@app.post("/mcp")
def mcp(body: Optional[dict] = None):
    """Required by openenv validate: must return a JSON-RPC 2.0 payload."""
    return {
        "jsonrpc": "2.0",
        "id": (body or {}).get("id", None),
        "result": {
            "tools": [
                {
                    "name": "reset",
                    "description": "Reset the email triage environment",
                    "inputSchema": {"type": "object", "properties": {"task": {"type": "string"}}},
                },
                {
                    "name": "step",
                    "description": "Take an action in the environment",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "email_id": {"type": "string"},
                            "label": {"type": "string"},
                        },
                        "required": ["type", "email_id"],
                    },
                },
                {
                    "name": "state",
                    "description": "Get the current environment state",
                    "inputSchema": {"type": "object", "properties": {}},
                },
            ]
        },
    }