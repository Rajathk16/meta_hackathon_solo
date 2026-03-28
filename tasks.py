# tasks.py

from models import Email

class EasyTask:
    def generate(self):
        return [
            Email(id="1", sender="user_81@gmail.com", subject="I forgot my password", body="Hi there. It seems I can't log into my account. I forgot the password and the reset link is giving me an error. Please help.", timestamp="2026-03-24T09:00Z", expected_label="support"),
            Email(id="2", sender="alice.smith@work.net", subject="How to change avatar?", body="Hello, I was wondering how I can upload a custom profile picture or avatar? I don't see the option in the settings menu.", timestamp="2026-03-24T10:15Z", expected_label="support"),
        ]

class MediumTask:
    def generate(self):
        return [
            Email(id="3", sender="billing@corp.com", subject="Invoice discrepancy", body="Our records show we were charged twice for our enterprise subscription this month. Please investigate and refund the latter charge immediately.", timestamp="2026-03-24T11:30Z", expected_label="billing"),
            Email(id="4", sender="dev.test@start.io", subject="Server 500 error on dashboard", body="The main reporting dashboard keeps crashing with a 500 internal server error anytime we attempt to query logs older than 30 days.", timestamp="2026-03-24T11:45Z", expected_label="bug"),
        ]

class HardTask:
    def generate(self):
        return [
            Email(id="5", sender="anon_hacker_42@darkweb.net", subject="Bounty submission - SQLi", body="There is an unauthenticated blind SQL injection vulnerability in your main checkout page. I have successfully dumped the user table. Contact me.", timestamp="2026-03-24T14:20Z", expected_label="security"),
            Email(id="6", sender="legal@bigfirm.com", subject="CEASE AND DESIST", body="It has come to our attention that your organization is using our registered trademarks without permission in your current marketing campaign. Cease immediately or face legal action.", timestamp="2026-03-24T16:00Z", expected_label="legal"),
        ]


TASKS = {
    "easy": EasyTask,
    "medium": MediumTask,
    "hard": HardTask
}