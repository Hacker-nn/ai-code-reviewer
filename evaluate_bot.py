import os
import csv
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = "Hacker-nn/ai-code-reviewer"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

EXPECTED = {
    "pr01": {"has_bug": True, "bug_type": "hardcoded password", "severity": "CRITICAL"},
    "pr02": {"has_bug": True, "bug_type": "SQL injection", "severity": "CRITICAL"},
    "pr03": {"has_bug": True, "bug_type": "divide by zero", "severity": "HIGH"},
    "pr04": {"has_bug": True, "bug_type": "no input validation", "severity": "MEDIUM"},
    "pr05": {"has_bug": True, "bug_type": "infinite loop", "severity": "HIGH"},
    "pr06": {"has_bug": True, "bug_type": "unused imports", "severity": "STYLE"},
    "pr07": {"has_bug": True, "bug_type": "mutable default", "severity": "HIGH"},
    "pr08": {"has_bug": True, "bug_type": "swallowed exception", "severity": "HIGH"},
    "pr09": {"has_bug": True, "bug_type": "hardcoded secrets", "severity": "CRITICAL"},
    "pr10": {"has_bug": True, "bug_type": "no error handling", "severity": "MEDIUM"},
    "pr11": {"has_bug": True, "bug_type": "XSS vulnerability", "severity": "CRITICAL"},
    "pr12": {"has_bug": True, "bug_type": "insecure random", "severity": "HIGH"},
    "pr13": {"has_bug": True, "bug_type": "memory leak", "severity": "MEDIUM"},
    "pr14": {"has_bug": True, "bug_type": "race condition", "severity": "HIGH"},
    "pr15": {"has_bug": True, "bug_type": "plaintext password", "severity": "CRITICAL"},
    "pr16": {"has_bug": False, "bug_type": "none", "severity": "none"},
    "pr17": {"has_bug": False, "bug_type": "none", "severity": "none"},
    "pr18": {
        "has_bug": True,
        "bug_type": "global variable abuse",
        "severity": "MEDIUM",
    },
    "pr19": {"has_bug": True, "bug_type": "type confusion", "severity": "MEDIUM"},
    "pr20": {"has_bug": True, "bug_type": "debug code left in", "severity": "HIGH"},
}


def get_pr_comments(pr_number):
    url = f"https://api.github.com/repos/{REPO}/issues/{pr_number}/comments"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def get_all_prs():
    url = f"https://api.github.com/repos/{REPO}/pulls?state=open&per_page=50"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def extract_verdict(comment_body):
    if "APPROVE" in comment_body:
        return "APPROVE"
    elif "REQUEST_CHANGES" in comment_body:
        return "REQUEST_CHANGES"
    elif "NEEDS_DISCUSSION" in comment_body:
        return "NEEDS_DISCUSSION"
    return "NO_VERDICT"


def extract_severities(comment_body):
    found = []
    for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "STYLE"]:
        if f"[{level}]" in comment_body:
            found.append(level)
    return found


def evaluate():
    print("Fetching all PRs...")
    prs = get_all_prs()

    results = []

    for pr in prs:
        pr_number = pr["number"]
        pr_title = pr["title"].lower()

        # match to expected by finding pr01..pr20 in branch name
        branch = pr["head"]["ref"]
        pr_key = None
        for key in EXPECTED:
            if key in branch:
                pr_key = key
                break

        if not pr_key:
            print(f"  Skipping PR #{pr_number} — no matching key in branch '{branch}'")
            continue

        expected = EXPECTED[pr_key]

        print(f"Evaluating PR #{pr_number} ({pr_key}) — {expected['bug_type']}...")

        comments = get_pr_comments(pr_number)
        bot_comments = [c for c in comments if "AI Code Review" in c["body"]]

        if not bot_comments:
            results.append(
                {
                    "pr_key": pr_key,
                    "pr_number": pr_number,
                    "bug_type": expected["bug_type"],
                    "has_bug": expected["has_bug"],
                    "bot_commented": False,
                    "verdict": "NO_COMMENT",
                    "severities": "",
                    "bug_caught": False,
                    "false_positive": False,
                    "correct": False,
                }
            )
            continue

        latest = bot_comments[-1]["body"]
        verdict = extract_verdict(latest)
        severities = extract_severities(latest)

        bug_caught = expected["has_bug"] and verdict == "REQUEST_CHANGES"
        false_positive = not expected["has_bug"] and verdict == "REQUEST_CHANGES"
        correct = bug_caught or (not expected["has_bug"] and verdict == "APPROVE")

        results.append(
            {
                "pr_key": pr_key,
                "pr_number": pr_number,
                "bug_type": expected["bug_type"],
                "has_bug": expected["has_bug"],
                "bot_commented": True,
                "verdict": verdict,
                "severities": ", ".join(severities),
                "bug_caught": bug_caught,
                "false_positive": false_positive,
                "correct": correct,
            }
        )

    # sort by pr_key
    results.sort(key=lambda x: x["pr_key"])

    # write CSV
    with open("evaluation_report.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    # print summary
    total = len(results)
    commented = sum(1 for r in results if r["bot_commented"])
    bugs_caught = sum(1 for r in results if r["bug_caught"])
    false_pos = sum(1 for r in results if r["false_positive"])
    correct = sum(1 for r in results if r["correct"])
    buggy_prs = sum(1 for r in results if r["has_bug"])

    print("\n" + "=" * 50)
    print("EVALUATION SUMMARY")
    print("=" * 50)
    print(f"Total PRs evaluated:     {total}")
    print(f"Bot commented:           {commented}/{total}")
    print(f"Bugs caught:             {bugs_caught}/{buggy_prs}")
    print(f"False positives:         {false_pos}/2 clean PRs")
    print(f"Overall correct:         {correct}/{total}")
    print(f"Catch rate:              {bugs_caught / buggy_prs * 100:.1f}%")
    print(f"Accuracy:                {correct / total * 100:.1f}%")
    print("\nCSV saved to evaluation_report.csv")


if __name__ == "__main__":
    evaluate()
