# AI Code Review Bot

An LLM-powered GitHub bot that automatically reviews every Pull Request and posts structured feedback with severity levels.

## How it works

1. Developer opens a Pull Request
2. GitHub Actions triggers automatically
3. Bot fetches the PR diff via GitHub REST API
4. Diff is sent to Groq API (Llama 3.3 70B)
5. Bot posts a structured review comment on the PR

## Results

Evaluated on 20 test PRs (18 with intentional bugs, 2 with clean code):

| Metric | Result |
|---|---|
| Bugs caught | 18/18 (100%) |
| False positive rate | 2/2 clean PRs flagged |
| Overall accuracy | 20/20 (100%) |

## Review format

Every review includes:
- **Summary** — one line describing what the PR does
- **Issues Found** — each issue tagged with severity: `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` / `STYLE`
- **Verdict** — `APPROVE` / `REQUEST_CHANGES` / `NEEDS_DISCUSSION`

## Setup

### 1. Add your Groq API key to GitHub Secrets
Go to your repo → Settings → Secrets → Actions → New secret:
- Name: `GROQ_API_KEY`
- Value: your key from https://console.groq.com

### 2. The bot runs automatically
Every PR triggers the workflow. No manual steps needed.

### 3. Run locally with Docker
```bash
docker build -t ai-reviewer .
docker run -e GROQ_API_KEY=... -e GITHUB_TOKEN=... -e REPO=owner/repo -e PR_NUMBER=1 ai-reviewer
```

## Tech stack

- GitHub Actions — CI/CD trigger
- Groq API — free LLM inference
- Llama 3.3 70B — the model doing the review
- Python + requests — no heavy frameworks

## Known limitations

- False positive rate on clean code is high (2/2 in testing) — the model tends to find style issues even in good code
- Diff truncated at 8000 characters — very large PRs may get incomplete reviews
- No inline comments yet — review posted as one comment, not on specific lines

## Future improvements

- Inline PR comments on specific diff lines
- Auto-apply GitHub labels based on severity
- Support multiple LLM providers (OpenAI, Claude)
- Fine-tune the prompt to reduce false positives