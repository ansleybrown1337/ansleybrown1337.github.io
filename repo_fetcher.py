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
        "repo": "bayes-sampler-comparison",
        "source": "personal",
        "headline": "Compares water sampling methods with Bayesian modeling for applied field research.",
        "image": "assets/images/featured/bayes-sampler-comparison.png",
    },
    {
        "repo": "ALS-Data-Cleaning-Tool",
        "source": "CSU-Agricultural-Water-Quality-Program",
        "headline": "Cleans and standardizes ALS water analysis exports for archiving and reporting.",
        "image": "assets/images/featured/als-data-cleaning-tool.png",
    },
    {
        "repo": "low-cost-iot-water-sampler",
        "source": "CSU-Agricultural-Water-Quality-Program",
        "headline": "Showcases low-cost IoT sampling hardware for scalable water quality monitoring.",
        "image": "assets/images/featured/low-cost-iot-water-sampler.png",
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

REPO_CATEGORIES = {
    ".github": "Documentation/Template",
    "air-quality-kit": "IoT Firmware",
    "ALS-Data-Cleaning-Tool": "Report Generator",
    "ansleybrown1337": "Documentation/Template",
    "ansleybrown1337.github.io": "Web Tool",
    "AWQP-LCS-Etape-Calibration": "Data Analysis",
    "AWQP-Water-Analysis-Report": "Report Generator",
    "AWQP_LCS_pump_calibration": "Data Analysis",
    "awqp-loggers": "IoT Firmware",
    "bayes-sampler-comparison": "Data Analysis",
    "bayes-tss-uncertainty": "Data Analysis",
    "Corn-yield-salinity-response": "Data Analysis",
    "csuthesis": "Documentation/Template",
    "EM38-and-ESAP-material": "Educational Material",
    "etape-calibration-investigation": "Data Analysis",
    "ExtractChem-Wrapper": "Data Analysis",
    "grocerygetter": "API Integration",
    "Hydrus-1D-Python-Wrapper": "Data Analysis",
    "imodels": "Data Analysis",
    "Intro-to-coding-in-R": "Educational Material",
    "Irrigation-inflow-outflow-calculator": "Data Analysis",
    "Letterboxd_Caz": "Data Analysis",
    "load-calc-experiment": "Data Analysis",
    "low-cost-iot-water-sampler": "IoT Firmware",
    "lysimeter-analysis": "Data Analysis",
    "multicolinearity-for-N-leaching-example": "Data Analysis",
    "nimble-csu-2023": "Educational Material",
    "optimal-path-using-dijkstras-algorithm": "Educational Material",
    "Particle-Electron-Modbus-Master-for-Campbell-Sci-Datalogger": "IoT Firmware",
    "pile-temp-sensor-comparison": "Data Analysis",
    "pollinator-strip-runoff": "Data Analysis",
    "QR-code-generator-example": "Educational Material",
    "runoff-mcmc": "Data Analysis",
    "runoff-temp-project": "Data Analysis",
    "sms-api-scrapers": "API Integration",
    "spectral-prediciton-of-salinity-glmulti": "Data Analysis",
    "ubidots-particle": "IoT Firmware",
    "Ubidots-Python-API-Client-Test": "API Integration",
}

CATEGORY_RULES = [
    ("report", "Report Generator"),
    ("html", "Report Generator"),
    ("dashboard", "Report Generator"),
    ("iot", "IoT Firmware"),
    ("particle", "IoT Firmware"),
    ("modbus", "IoT Firmware"),
    ("logger", "IoT Firmware"),
    ("sensor", "IoT Firmware"),
    ("firmware", "IoT Firmware"),
    ("api", "API Integration"),
    ("scraper", "API Integration"),
    ("ubidots", "API Integration"),
    ("kroger", "API Integration"),
    ("site", "Web Tool"),
    ("website", "Web Tool"),
    ("github page", "Web Tool"),
    ("template", "Documentation/Template"),
    ("config", "Documentation/Template"),
    ("documentation", "Documentation/Template"),
    ("course", "Educational Material"),
    ("tutorial", "Educational Material"),
    ("training", "Educational Material"),
    ("workshop", "Educational Material"),
    ("material", "Educational Material"),
    ("example", "Educational Material"),
    ("analysis", "Data Analysis"),
    ("investigation", "Data Analysis"),
    ("model", "Data Analysis"),
    ("mcmc", "Data Analysis"),
    ("bayesian", "Data Analysis"),
    ("calibration", "Data Analysis"),
    ("comparison", "Data Analysis"),
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


def choose_category(name: str, description: str | None, language: str | None) -> str:
    if name in REPO_CATEGORIES:
        return REPO_CATEGORIES[name]

    haystack = f"{name.lower()} {(description or '').lower()} {(language or '').lower()}"
    for needle, category in CATEGORY_RULES:
        if needle in haystack:
            return category

    return "Data Analysis"


def summarize_repo(repo: dict) -> dict:
    description = repo.get("description") or "No description provided yet."
    language = repo.get("language")
    return {
        "name": repo["name"],
        "url": repo["html_url"],
        "description": description,
        "fork": bool(repo["fork"]),
        "category": choose_category(repo["name"], description, language),
        "homepage": repo.get("homepage") or "",
        "updated_at": repo["updated_at"],
        "stargazers_count": repo.get("stargazers_count", 0),
        "icon": choose_icon(repo["name"], description, language, bool(repo["fork"])),
    }


def build_featured_section(repo_sources: dict[str, list[dict]]) -> list[dict]:
    featured_cards: list[dict] = []

    for item in FEATURED_PROJECTS:
        source_name = item.get("source", "personal")
        repo_lookup = {repo["name"]: repo for repo in repo_sources.get(source_name, [])}
        repo = repo_lookup.get(item["repo"])
        if not repo:
            continue
        featured_cards.append(
            {
                **repo,
                "headline": item["headline"],
                "image": item.get("image", ""),
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


def build_repo_sources(personal_repos: list[dict], org_sections: list[dict]) -> dict[str, list[dict]]:
    sources = {"personal": personal_repos}
    for org in ORGANIZATIONS:
        matching = next((section for section in org_sections if section["name"] == org["label"]), None)
        if matching:
            sources[org["name"]] = matching["repos"]
    return sources


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
                "category": choose_category(name, description, None),
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
    org_sections = [
        {
            "name": ORGANIZATIONS[0]["label"],
            "github_url": ORGANIZATIONS[0]["github_url"],
            "website_url": ORGANIZATIONS[0]["website_url"],
            "repos": sorted(org_repos, key=lambda repo: repo["name"].lower()),
        }
    ]
    featured = build_featured_section(
        {
            "personal": personal_repos,
            ORGANIZATIONS[0]["name"]: org_repos,
        }
    )

    return {
        "profile": PROFILE,
        "online_apps": ONLINE_APPS,
        "featured": featured,
        "personal": {
            "created": sorted(personal_repos, key=lambda repo: repo["name"].lower()),
            "forked": [],
        },
        "organizations": org_sections,
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
    org_sections = build_org_sections()

    return {
        "profile": PROFILE,
        "online_apps": ONLINE_APPS,
        "featured": build_featured_section(build_repo_sources(normalized_personal, org_sections)),
        "personal": build_personal_sections(normalized_personal),
        "organizations": org_sections,
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
