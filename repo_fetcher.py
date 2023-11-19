"""
GitHub Repository Fetcher

This script allows the user to fetch and format a list of GitHub repositories
in Markdown format. It includes functions to get repositories for both individual
users and organizations. The script makes use of the GitHub API to retrieve
repository information.

Author: Ansley Brown
GitHub API Documentation: https://docs.github.com/en/rest?apiVersion=2022-11-28

Usage:
1. Call get_user_repos() with a GitHub username to get repositories of that user.
2. Call get_organization_repos() with a GitHub organization name to get repositories of that organization.
3. The output will be printed in Markdown format, suitable for use in documentation or GitHub README files.
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

my_list = get_user_repos("ansleybrown1337")
print(my_list)

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

awqp_list = get_organization_repos("CSU-Agricultural-Water-Quality-Program")
print(awqp_list)
