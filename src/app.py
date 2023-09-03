from flask import Flask, render_template, request
from dotenv import dotenv_values

import requests

app = Flask(__name__)
env_variables = dotenv_values(".env")

def check_user(username):
    "Checks if it's a valid user"
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, auth=(env_variables['GH-USER'], env_variables['GH-TOKEN']))
    
    if response.status_code == 200:
        return True
    else:
        return False

def get_repo_timelines(username):
    "Gets the Timeline of the user's repos"

    username_status = check_user(username)

    if username_status:
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url, auth=(env_variables['GH-USER'], env_variables['GH-TOKEN']))
        repos = response.json()
        repos_list = []
        for repo in repos:
            repos_list.append([repo['name'], repo['created_at'], repo['updated_at'], repo['html_url'], repo['description'], repo['language']]) 
        return list(repos_list)
    else:
        raise Exception("Invalid Username")
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Timeline', methods=['POST'])
def timeline():
    if request.method == 'POST':

        username = request.form['userName']
        repos = get_repo_timelines(username)

        print(repos)
        
        repos.sort(key=lambda x: x[1], reverse=True)

        if repos:
            print(repos)
            return render_template('timeline.html', repos=repos, userName=username, length=len(repos))
        else:
            return render_template('error.html', username=username)
    
if __name__ == '__main__':
    app.run(debug=True)