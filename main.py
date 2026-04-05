import os
import sys
import requests


def get_diff(repo, pr_number, github_token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3.diff",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def review_with_groq(diff, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    system_prompt = """You are a senior software engineer doing a code review.
Analyze the git diff and respond in this exact format:

## Summary
One sentence describing what this PR does.

## Issues Found
For each issue use this format:
**[SEVERITY]** `filename` - Description of the issue.
Severity levels: CRITICAL | HIGH | MEDIUM | LOW | STYLE

## Verdict
One of: APPROVE | REQUEST_CHANGES | NEEDS_DISCUSSION"""

    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Review this diff:\n\n{diff[:8000]}"},
        ],
        "max_tokens": 1500,
        "temperature": 0.2,
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def post_comment(repo, pr_number, github_token, body):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
    }
    response = requests.post(url, headers=headers, json={"body": body})
    response.raise_for_status()


def main():
    repo = os.environ["REPO"]
    pr_number = int(os.environ["PR_NUMBER"])
    github_token = os.environ["GITHUB_TOKEN"]
    groq_api_key = os.environ["GROQ_API_KEY"]

    print(f"Fetching diff for PR #{pr_number} in {repo}...")
    diff = get_diff(repo, pr_number, github_token)

    if not diff.strip():
        print("No diff found. Skipping.")
        return

    print("Sending to Groq...")
    review = review_with_groq(diff, groq_api_key)

    comment = f"## AI Code Review\n\n{review}\n\n---\n*Powered by Groq + Llama 3.3 70B*"

    print("Posting comment...")
    post_comment(repo, pr_number, github_token, comment)

    print("Done!")


if __name__ == "__main__":
    main()
