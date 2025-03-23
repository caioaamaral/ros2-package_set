import requests

def get_latest_commit_from_upstream(owner, repo, path, branch):
    api_url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    params = {
        'path': path,
        'sha': branch,
        'per_page': 1  # only need the most recent commit
    }

    resp = requests.get(api_url, headers=None, params=params)
    resp.raise_for_status()

    data = resp.json()
    if not data:
        raise ValueError(f'No commits found in {api_url}')

    return data[0]['sha']

OWNER = "ros"
REPO = "rosdistro"
BRANCH = "master"
PATH = "humble/distribution.yaml"

# print(get_latest_commit_from_upstream(OWNER, REPO, PATH, BRANCH))