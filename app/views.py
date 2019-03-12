import requests

from app import app
from flask import render_template


@app.route('/')
def index():
    return render_template("index.html",
                           columns=get_columns())


def get_columns():
    columns = [{'id': x['id'],
                'name': x['name']}
               for x in
               gh('projects/{}/columns'.format(app.config['GITHUB_PROJECT']))]

    for column in columns:
        column['cards'] = [{'id': x['id'],
                            'note': x['note'],
                            'updated_at': x['updated_at']}
                           for x in
                           gh("projects/columns/{}/cards".format(column['id']))]

    return columns


def gh(endpoint):
    headers = {
        'Accept': 'application/vnd.github.inertia-preview+json',
        'Authorization': 'token {}'.format(app.config['GITHUB_TOKEN']),
    }
    res = requests.get('https://api.github.com/{}'.format(endpoint), headers=headers)
    return res.json()
