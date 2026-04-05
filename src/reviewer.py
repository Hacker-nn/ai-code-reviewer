from src.github_client import GitHubClient
from src.llm_client import LLMClient


def run_review(repo: str, pr_number: int, github_token: str, groq_api_key: str) -> str:
    github = GitHubClient(token=github_token)
    llm = LLMClient(api_key=groq_api_key)

    print(f"Fetching diff for PR #{pr_number} in {repo}...")
    diff = github.get_diff(repo=repo, pr_number=pr_number)

    if not diff.strip():
        print("No diff found. Skipping review.")
        return "No diff"

    print("Sending diff to LLM...")
    review_text = llm.review_diff(diff=diff)

    comment = f"## 🤖 AI Code Review\n\n{review_text}\n\n---\n*Powered by Groq + Llama 3.3 70B*"

    print("Posting comment to PR...")
    github.post_comment(repo=repo, pr_number=pr_number, body=comment)

    print("Done!")
    return review_text
