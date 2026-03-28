import os
import json
from openai import OpenAI
from environment import EmailEnv
from models import Action

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY", "hf_your_token_here")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3-8B-Instruct")

def run_agent(task_name: str, env: EmailEnv):
    print(f"\n--- Starting Task: {task_name} ---")
    obs = env.reset(task=task_name)
    
    # Initialize OpenAI client using the global variables
    client = OpenAI(api_key=API_KEY, base_url=API_BASE_URL)
    
    while True:
        # Pydantic models to dict for easy viewing
        obs_dict = {
            "inbox": [e.model_dump() for e in obs.inbox],
            "current_email": obs.current_email.model_dump() if obs.current_email else None,
            "steps": obs.steps
        }
        
        if not obs.current_email:
            break
            
        prompt = f"""
You are an AI Email agent. Your goal is to triage the inbox efficiently.
Current Observation:
{json.dumps(obs_dict, indent=2)}

Available Actions:
1. classify: Set a label for the email. Requires `email_id` and `label`. Labels vary by task (e.g., support, billing, bug, security, legal).
2. respond: Reply to the email. Requires `email_id`. Good for simple 'support' emails.
3. escalate: Escalate to a human. Requires `email_id`. Good for 'bug', 'billing', 'security', 'legal'.

Output MUST be a valid JSON dictionary matching this schema:
{{"type": "action_type", "email_id": "123", "label": "optional_label"}}

What is your next action?
"""
        
        try:
            # When testing without a valid token/url, we simulate an LLM fallback
            if API_KEY == "dummy" or not API_KEY:
                # Mock a correct action based on simple rule-based approach just to demonstrate it runs
                simulated_type = "respond"
                simulated_label = "support"
                subject = obs.current_email.subject.lower()
                
                if "invoice" in subject:
                    simulated_type, simulated_label = "escalate", "billing"
                elif "500" in subject:
                    simulated_type, simulated_label = "escalate", "bug"
                elif "sqli" in subject:
                    simulated_type, simulated_label = "escalate", "security"
                elif "cease" in subject:
                    simulated_type, simulated_label = "escalate", "legal"
                elif "password" in subject or "avatar" in subject:
                    simulated_type, simulated_label = "respond", "support"

                action_dict = {"type": simulated_type, "email_id": obs.current_email.id, "label": simulated_label}
            else:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                action_dict = json.loads(response.choices[0].message.content)
        except Exception as e:
            print("Error parsing LLM response:", e)
            action_dict = {"type": "noop", "email_id": obs.current_email.id, "label": ""}

        # Step the environment
        try:
            action = Action(**action_dict)
            obs, reward, done, info = env.step(action)
            print(f"Action Taken: {action_dict} | Reward: {reward.value} ({reward.reason})")
        except Exception as e:
            print(f"Error executing action {action_dict}: {e}")
            break

        if done:
            break

    from grader import grade
    final_state = env.state()
    score = grade(final_state)
    print(f"Task '{task_name}' finished. Final Score: {score}")
    return score

if __name__ == "__main__":
    env = EmailEnv()
    for t in ["easy", "medium", "hard"]:
        run_agent(t, env)
