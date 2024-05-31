import os

from flask import Flask, request, render_template_string
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Constants
GITHUB_API_URL = 'https://api.github.com'
# Just add you github Token here, navigate to this link to add a guthub token (https://github.com/settings/tokens)
GITHUB_TOKEN = "your github token here"
MIN_STARS = 100
MAX_PROJECTS = 100
ISSUES_WITHIN_DAYS = 30

def get_repositories(skill):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }

    query = f'{skill} in:description,topics'
    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
        'per_page': MAX_PROJECTS
    }
    try:
        response = requests.get(f'{GITHUB_API_URL}/search/repositories', headers=headers, params=params)
        response.raise_for_status()
        return response.json()['items']
    except requests.exceptions.HTTPError as http_err:
        print("HTTP error occurred: Check your name")
        print(f"HTTP error details: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print("Connection error occurred: Check your name")
        print(f"Connection error details: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print("Timeout error occurred: Check your name")
        print(f"Timeout error details: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print("An error occurred: Check your name")
        print(f"Error details: {req_err}")

def get_recent_issues(owner, repo):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }

    since_date = (datetime.now() - timedelta(days=ISSUES_WITHIN_DAYS)).isoformat()
    params = {
        'since': since_date
    }

    response = requests.get(f'{GITHUB_API_URL}/repos/{owner}/{repo}/issues', headers=headers, params=params)
    response.raise_for_status()
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        skills = [skill.strip() for skill in request.form['skills'].split(',')]
        results = {}

        for skill in skills:
            repositories = get_repositories(skill)
            filtered_repositories = []

            for repo in repositories:
                if repo['stargazers_count'] < MIN_STARS:
                    continue

                owner = repo['owner']['login']
                repo_name = repo['name']

                issues = get_recent_issues(owner, repo_name)

                if issues:
                    filtered_repositories.append({
                        'name': repo_name,
                        'url': repo['html_url'],
                        'stars': repo['stargazers_count']
                    })

                if len(filtered_repositories) >= MAX_PROJECTS:
                    break

            results[skill] = filtered_repositories

        return render_template_string(TEMPLATE, results=results)

    return render_template_string(TEMPLATE)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Repo Finder</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
        
  font-family: 'Comic Sans MS', cursive, sans-serif;
  background-color: #24292e; /* GitHub text color as background */
  color: #f5f5f5; /* Light gray for text */
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Open Sans', sans-serif; /* Clean sans-serif font for headings */
  color: #e1e4e8; /* GitHub input border color for headings */
}

label {
  color: #e1e4e8; /* GitHub input border color for labels */
}

input[type="text"], input[type="submit"] {
  border: 2px solid #424a53; /* Darker border color */
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  width: 100%;
  background-color: #30363d; /* Lighter dark background for inputs */
  color: #f5f5f5; /* Light gray text for inputs */
}

input[type="submit"] {
  background-color: #4caf50; /* Lighter green for submit button */
  color: white;
  font-weight: bold;
  cursor: pointer;
}

input[type="submit"]:hover {
  background-color: #388e3c; /* Darker green hover color for submit button */
}

ul {
  padding: 0;
}

.card {
  border: 1px solid #424a53; /* Darker border color */
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* Slightly stronger shadow */
}

.card-header {
  background-color: #30363d; /* Lighter dark background for card header */
  border-bottom: 1px solid #424a53; /* Darker border color */
  padding: 10px;
  border-radius: 10px 10px 0 0;
}

.card-body {
  padding: 15px;
}

.card-title {
  color: #90caf9; /* Lighter blue for card titles */
  font-weight: bold;
  font-size: 18px;
}

.card-title:hover {
  text-decoration: underline;
}

.stars {
  color: #ffc107; /* Lighter yellow for stars */
  font-weight: bold;
}
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <h1 class="text-center mt-5 mb-4">GitHub Repo Finder</h1>
                <form method="post">
                    <label for="skills">Enter your skills (comma-separated, e.g., django,python):</label><br>
                    <input type="text" id="skills" name="skills" required><br><br>
                    <input type="submit" value="Search" class="btn btn-success btn-block">
                </form>
                <p>The results may take upto 5 minutes to load since I am trying to fetch around 100 projects for each skill that have atleast  100 stars ⭐️each and issues that have recently been updated .So please be patient 😊!  <p>
                {% if results %}
                    <h2 class="mt-5">Search Results:</h2>
                    {% for skill, repos in results.items() %}
                        <h3>Repositories for skill: {{ skill }}</h3>
                        {% if repos %}
                            {% for repo in repos %}
                                <div class="card">
                                    <div class="card-header">
                                        <a href="{{ repo.url }}" target="_blank" class="card-title">{{ repo.name }}</a>
                                    </div>
                                    <div class="card-body">
                                        <p class="stars">Stars: {{ repo.stars }}</p>
                                    </div>
                                </div>
                                <br>
                                <hr>
                                <br>
                            {% endfor %}
                        {% else %}
                            <p>No repositories found with recent issues.</p>
                        {% endif %}
                    {% endfor %}
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>


"""

if __name__ == '__main__':
    app.run()
