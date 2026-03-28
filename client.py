import requests
from typing import Dict, Any

class Client:
    """
    Standard OpenEnv Client wrapper for interacting with the Email Triage environment 
    over HTTP REST endpoints.
    """
    def __init__(self, base_url="http://localhost:7860"):
        self.base_url = base_url.rstrip("/")

    def reset(self, task: str = "easy") -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/reset", params={"task": task})
        response.raise_for_status()
        return response.json()

    def step(self, action: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}/step", json=action)
        response.raise_for_status()
        return response.json()

    def state(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/state")
        response.raise_for_status()
        return response.json()

    def grade(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/grader")
        response.raise_for_status()
        return response.json()
