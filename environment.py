from tasks import TASKS
from models import Email, EmailPublic, Observation, Action, Reward


class EmailEnv:
    def __init__(self):
        self.emails = []
        self.handled = []
        self.step_count = 0
        self.correct_resolutions = 0

    def reset(self, task="easy"):
        self.step_count = 0
        self.handled = []
        self.correct_resolutions = 0

        task_obj = TASKS[task]()
        self.emails = task_obj.generate()

        return self._get_obs()

    def step(self, action: Action):
        self.step_count += 1

        email = next((e for e in self.emails if e.id == action.email_id), None)

        if not email:
            return self._get_obs(), Reward(value=-1.0, reason="Invalid email"), False, {}

        reward_value = 0.0
        reason = ""

        # --- ACTION LOGIC ---
        is_correct = False
        if action.type == "classify":
            if action.label == email.expected_label:
                reward_value = 1.0
                reason = "Correct classification"
                is_correct = True
            else:
                reward_value = -0.5
                reason = "Wrong classification"

        elif action.type == "respond":
            if email.expected_label == "support":
                reward_value = 0.8
                reason = "Good response"
                is_correct = True
            else:
                reward_value = 0.3
                reason = "Weak response"

        elif action.type == "escalate":
            if email.expected_label in ["bug", "billing", "security", "legal"]:
                reward_value = 1.0
                reason = "Correct escalation"
                is_correct = True
            else:
                reward_value = -0.5
                reason = "Wrong escalation"

        self.handled.append(email.id)
        if is_correct:
            self.correct_resolutions += 1

        done = len(self.handled) == len(self.emails)

        return self._get_obs(), Reward(value=reward_value, reason=reason), done, {}

    def state(self):
        return {
            "emails": self.emails,
            "handled": self.handled,
            "correct_resolutions": self.correct_resolutions,
            "steps": self.step_count
        }

    def _get_obs(self):
        remaining_public = []
        for e in self.emails:
            if e.id not in self.handled:
                # Use model_dump to extract safe fields for EmailPublic view
                public_data = {k: v for k, v in e.model_dump().items() if k != 'expected_label'}
                remaining_public.append(EmailPublic(**public_data))

        return Observation(
            inbox=remaining_public,
            current_email=remaining_public[0] if remaining_public else None,
            steps=self.step_count
        )