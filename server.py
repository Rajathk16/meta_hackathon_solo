# server.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from environment import EmailEnv
from models import Action
from grader import grade

app = FastAPI()


class ResetRequest(BaseModel):
    task: Optional[str] = "easy"

env = EmailEnv()


@app.get("/")
def home():
    return {"message": "OpenEnv Email Triage Running"}


@app.post("/reset")
def reset(body: Optional[ResetRequest] = None):
    task = body.task if body and body.task else "easy"
    obs = env.reset(task)
    return obs


@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state")
def state():
    return env.state()


@app.get("/tasks")
def tasks():
    return ["easy", "medium", "hard"]


@app.get("/grader")
def grader():
    return {"score": grade(env.state())}