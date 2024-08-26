"""
GitHub Repository Fetcher

This script allows the user to fetch and format a list of GitHub repositories
in Markdown format. It includes functions to get repositories for both individual
users and organizations. The script makes use of the GitHub API to retrieve
repository information.

Author: Ansley Brown
GitHub API Documentation: https://docs.github.com/en/rest?apiVersion=2022-11-28
"""

import requests

def get_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    
    if response.status_code == 200:
        repos = response.json()
        markdown_list = ""
        for repo in repos:
            name = repo['name']
            html_url = repo['html_url']
            description = repo['description'] if repo['description'] else "No description"
            markdown_list += f"- **[{name}]({html_url})**\n  - {description}\n"
        return markdown_list
    else:
        print("Failed to retrieve repositories")
        return None

def get_organization_repos(org_name):
    url = f"https://api.github.com/orgs/{org_name}/repos"
    response = requests.get(url)
    
    if response.status_code == 200:
        repos = response.json()
        markdown_list = ""
        for repo in repos:
            name = repo['name']
            html_url = repo['html_url']
            description = repo['description'] if repo['description'] else "No description"
            markdown_list += f"- **[{name}]({html_url})**\n  - {description}\n"
        return markdown_list
    else:
        print("Failed to retrieve repositories")
        return None

def create_readme():
    user_repo_section = get_user_repos("ansleybrown1337")
    org_repo_section = get_organization_repos("CSU-Agricultural-Water-Quality-Program")

    readme_content = f"""
# Introduction
A website created to easily direct users to my data tools and projects. To view a project, click on the project title, and it will direct you to the project's GitHub repository.

If you see any that interest you, feel free to reach out to me at [Ansley.Brown@colostate.edu](mailto:Ansley.Brown@colostate.edu) or [ansleybrown1337@gmail.com](mailto:ansleybrown1337@gmail.com).

> [!TIP]
> The contents of this website are automatically generated from a python script I created. The script uses the GitHub API to pull all of my repositories and then formats them into a markdown file. The markdown file is then converted into a website using GitHub Pages. Please feel free to use the script for your own purposes and modify as needed! The script can be found [in this repository](repo_fetcher.py).

# Table of Contents
- [My projects](#my-projects)
- [Projects I've done for Others](#projects-ive-done-for-others)
  - [CSU Agriculture Water Quality Program](#csu-agriculture-water-quality-program)

# My projects
{user_repo_section}

# Projects I've done for Others

## CSU Agriculture Water Quality Program
- [AWQP GitHub Page](https://github.com/CSU-Agricultural-Water-Quality-Program)
- [AWQP Website](https://waterquality.colostate.edu/)

### Projects
{org_repo_section}

# Note on Private Repositories
Please note that many repositories never go public due to various reasons (e.g., data privacy, intellectual property, etc.). If you are interested in seeing more of my work, please reach out to me directly, and I may be able to provide you with more information.
    """

    with open('README.md', 'w', encoding='utf-8') as readme_file:
        readme_file.write(readme_content)

create_readme()
