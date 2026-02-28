"""
Generate static site data for AJ's GitHub Pages portfolio.

The site itself is a small static frontend that reads the generated JavaScript
payload from assets/generated/site-data.js. Repo inventory remains automated via
the GitHub API, while featured tools and live apps stay hand-curated here.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

SITE_ROOT = Path(__file__).parent
OUTPUT_PATH = SITE_ROOT / "assets" / "generated" / "site-data.js"
README_PATH = SITE_ROOT / "README.md"

PROFILE = {
    "title": "AJ's Data Tools and Projects",
    "tagline": "Applied data tools for agriculture, water quality, and decision support.",
    "about": (
        "A curated portfolio of research software, field tools, teaching material, "
        "and live applications. The repo inventory below is refreshed from GitHub "
        "so the catalog stays current."
    ),
    "back_link": "https://sites.google.com/view/ansleyjbrown",
    "primary_email": "Ansley.Brown@colostate.edu",
    "secondary_email": "ansleybrown1337@gmail.com",
}

ONLINE_APPS = [
    {
        "name": "Lysimeter Analysis",
        "url": "https://csu-lysimeter-analysis.streamlit.app/",
        "description": "Interactive analysis workflow for weighing lysimeter data.",
        "icon": "chart",
    },
    {
        "name": "Weather Forecasting Tool",
        "url": "https://rushmgmt.streamlit.app/",
        "description": "Live forecasting interface for weather-driven planning.",
        "icon": "cloud",
    },
]

FEATURED_PROJECTS = [
    {
        "repo": "lysimeter-analysis",
        "headline": "Quantifies crop water use from weighing lysimeter observations.",
    },
    {
        "repo": "AWQP-Water-Analysis-Report",
        "headline": "Builds standardized water quality reports with automated analytics.",
    },
    {
        "repo": "bayes-tss-uncertainty",
        "headline": "Applies Bayesian inference to uncertainty in suspended solids data.",
    },
]

ORGANIZATIONS = [
    {
        "name": "CSU-Agricultural-Water-Quality-Program",
        "label": "CSU Agriculture Water Quality Program",
        "github_url": "https://github.com/CSU-Agricultural-Water-Quality-Program",
        "website_url": "https://waterquality.colostate.edu/",
    }
]

ICON_RULES = [
    ("lysimeter", "chart"),
    ("forecast", "cloud"),
    ("weather", "cloud"),
    ("bayes", "beaker"),
    ("stan", "beaker"),
    ("water", "droplet"),
    ("runoff", "droplet"),
    ("salinity", "leaf"),
    ("crop", "leaf"),
    ("yield", "leaf"),
    ("iot", "chip"),
    ("sensor", "chip"),
    ("particle", "chip"),
    ("api", "code"),
    ("python", "code"),
    ("r ", "code"),
]


def fetch_all_repos(url: str) -> list[dict]:
    repos: list[dict] = []
    page = 1
    headers = dict(BASE_HEADERS)
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    while True:
        query = urlencode({"per_page": 100, "page": page, "sort": "updated"})
        request = Request(
            f"{url}?{query}",
            headers=headers,
        )
        try:
            with urlopen(request, timeout=30) as response:
                page_repos = json.load(response)
        except HTTPError as exc:
            raise RuntimeError(f"GitHub API request failed with status {exc.code}") from exc
        except URLError as exc:
            raise RuntimeError(f"GitHub API request failed: {exc.reason}") from exc

        if not page_repos:
            break
        repos.extend(page_repos)
        page += 1

    return repos


def choose_icon(name: str, description: str | None, language: str | None, fork: bool) -> str:
    haystack = f"{name.lower()} {(description or '').lower()} "
    for needle, icon in ICON_RULES:
        if needle in haystack:
            return icon

    language_key = (language or "").lower()
    if language_key in {"python", "r", "jupyter notebook"}:
        return "code"
    if language_key in {"html", "css", "javascript", "typescript"}:
        return "browser"
    if fork:
        return "branch"
    return "folder"


def summarize_repo(repo: dict) -> dict:
    description = repo.get("description") or "No description provided yet."
    return {
        "name": repo["name"],
        "url": repo["html_url"],
        "description": description,
        "fork": bool(repo["fork"]),
        "language": repo.get("language") or "Unknown",
        "homepage": repo.get("homepage") or "",
        "updated_at": repo["updated_at"],
        "stargazers_count": repo.get("stargazers_count", 0),
        "icon": choose_icon(repo["name"], description, repo.get("language"), bool(repo["fork"])),
    }


def build_featured_section(repos: list[dict]) -> list[dict]:
    repo_lookup = {repo["name"]: repo for repo in repos}
    featured_cards: list[dict] = []

    for item in FEATURED_PROJECTS:
        repo = repo_lookup.get(item["repo"])
        if not repo:
            continue
        featured_cards.append(
            {
                **repo,
                "headline": item["headline"],
            }
        )

    return featured_cards


def build_personal_sections(repos: list[dict]) -> dict:
    created = [repo for repo in repos if not repo["fork"]]
    forked = [repo for repo in repos if repo["fork"]]

    return {
        "created": sorted(created, key=lambda repo: repo["name"].lower()),
        "forked": sorted(forked, key=lambda repo: repo["name"].lower()),
    }


def build_org_sections() -> list[dict]:
    sections: list[dict] = []

    for org in ORGANIZATIONS:
        repos = fetch_all_repos(f"https://api.github.com/orgs/{org['name']}/repos")
        normalized = [summarize_repo(repo) for repo in repos]
        sections.append(
            {
                "name": org["label"],
                "github_url": org["github_url"],
                "website_url": org["website_url"],
                "repos": sorted(normalized, key=lambda repo: repo["name"].lower()),
            }
        )

    return sections


def parse_readme_repo_block(lines: list[str]) -> list[dict]:
    repos: list[dict] = []
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        match = re.match(r"- \*\*\[(.+?)\]\((https?://.+?)\)\*\*", line)
        if not match:
            index += 1
            continue

        description = "No description provided yet."
        if index + 1 < len(lines):
            next_line = lines[index + 1].strip()
            if next_line.startswith("- "):
                description = next_line[2:].strip()

        name, url = match.groups()
        repos.append(
            {
                "name": name,
                "url": url,
                "description": description,
                "fork": False,
                "language": "Unknown",
                "homepage": "",
                "updated_at": "",
                "stargazers_count": 0,
                "icon": choose_icon(name, description, None, False),
            }
        )
        index += 1

    return repos


def build_offline_site_data() -> dict:
    readme_text = README_PATH.read_text(encoding="utf-8")

    personal_start = readme_text.index("## My projects")
    collab_start = readme_text.index("## Projects I've done for Others")
    org_start = readme_text.index("#### Projects")
    note_start = readme_text.index("## Note on Private Repositories")

    personal_lines = readme_text[personal_start:collab_start].splitlines()[1:]
    org_lines = readme_text[org_start:note_start].splitlines()[1:]

    personal_repos = parse_readme_repo_block(personal_lines)
    org_repos = parse_readme_repo_block(org_lines)
    featured = build_featured_section(personal_repos)

    return {
        "profile": PROFILE,
        "online_apps": ONLINE_APPS,
        "featured": featured,
        "personal": {
            "created": sorted(personal_repos, key=lambda repo: repo["name"].lower()),
            "forked": [],
        },
        "organizations": [
            {
                "name": ORGANIZATIONS[0]["label"],
                "github_url": ORGANIZATIONS[0]["github_url"],
                "website_url": ORGANIZATIONS[0]["website_url"],
                "repos": sorted(org_repos, key=lambda repo: repo["name"].lower()),
            }
        ],
        "notes": {
            "private_repos": (
                "Many repositories remain private because of data sensitivity, "
                "client constraints, or intellectual property. Reach out directly "
                "if you would like more context on work that is not public. "
                "This local preview is seeded from README because the GitHub API "
                "is unavailable in the current environment."
            )
        },
    }


def build_site_data() -> dict:
    personal_repos = fetch_all_repos("https://api.github.com/users/ansleybrown1337/repos")
    normalized_personal = [summarize_repo(repo) for repo in personal_repos]

    return {
        "profile": PROFILE,
        "online_apps": ONLINE_APPS,
        "featured": build_featured_section(normalized_personal),
        "personal": build_personal_sections(normalized_personal),
        "organizations": build_org_sections(),
        "notes": {
            "private_repos": (
                "Many repositories remain private because of data sensitivity, "
                "client constraints, or intellectual property. Reach out directly "
                "if you would like more context on work that is not public."
            )
        },
    }


def write_site_data(site_data: dict) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(site_data, indent=2)
    OUTPUT_PATH.write_text(
        f"window.SITE_DATA = {payload};\n",
        encoding="utf-8",
    )


def main() -> None:
    try:
        site_data = build_site_data()
    except RuntimeError as exc:
        print(f"{exc}\nFalling back to README seed data.")
        site_data = build_offline_site_data()
    write_site_data(site_data)
    print(f"Wrote {OUTPUT_PATH.relative_to(SITE_ROOT)}")


if __name__ == "__main__":
    main()
