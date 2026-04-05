import os
from src.reviewer import run_review


def main():
    repo = os.environ["REPO"]
    pr_number = int(os.environ["PR_NUMBER"])
    github_token = os.environ["GITHUB_TOKEN"]
    groq_api_key = os.environ["GROQ_API_KEY"]

    run_review(
        repo=repo,
        pr_number=pr_number,
        github_token=github_token,
        groq_api_key=groq_api_key,
    )


if __name__ == "__main__":
    main()
