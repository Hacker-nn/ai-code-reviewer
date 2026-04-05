import requests


class GitHubClient:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }
        self.base = "https://api.github.com"

    def get_diff(self, repo: str, pr_number: int) -> str:
        url = f"{self.base}/repos/{repo}/pulls/{pr_number}"
        headers = {**self.headers, "Accept": "application/vnd.github.v3.diff"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    def post_comment(self, repo: str, pr_number: int, body: str) -> None:
        url = f"{self.base}/repos/{repo}/issues/{pr_number}/comments"
        response = requests.post(url, headers=self.headers, json={"body": body})
        response.raise_for_status()

    def post_inline_comment(
        self,
        repo: str,
        pr_number: int,
        body: str,
        commit_id: str,
        path: str,
        position: int,
    ) -> None:
        url = f"{self.base}/repos/{repo}/pulls/{pr_number}/comments"
        payload = {
            "body": body,
            "commit_id": commit_id,
            "path": path,
            "position": position,
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
