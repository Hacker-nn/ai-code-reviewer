import requests

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """You are a senior software engineer doing a code review.
If the code is clean and follows good practices, do not invent issues.
Only report real, meaningful problems.
Avoid generic suggestions like "add comments" or "add tests".

Analyze the git diff and respond in this exact format:

## Summary
One sentence describing what this PR does.

## Issues Found
For each issue, use this format:
**[SEVERITY]** `filename:line` — Description of the issue.

Severity levels: CRITICAL | HIGH | MEDIUM | LOW | STYLE

## Verdict
One of: APPROVE | REQUEST_CHANGES | NEEDS_DISCUSSION
"""


class LLMClient:
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model

    def review_diff(self, diff: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Review this diff:\n\n{diff[:8000]}"},
            ],
            "max_tokens": 1500,
            "temperature": 0.2,
        }
        response = requests.post(GROQ_URL, headers=headers, json=body)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
