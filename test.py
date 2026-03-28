from environment import EmailEnv
from models import Action
from grader import grade

env = EmailEnv()

obs = env.reset(task="easy")

while True:
    email = obs.current_email
    if not email:
        break

    action = Action(
        type="classify",
        email_id=email.id,
        label=email.type
    )

    obs, reward, done, _ = env.step(action)

    print(f"\nEmail: {email.subject}")
    print("Reward:", reward)

    if done:
        break

# FINAL SCORE
score = grade(env.state())
print("\nFinal Score:", score)