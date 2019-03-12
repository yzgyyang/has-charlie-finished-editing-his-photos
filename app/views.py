import requests

from app import app
from flask import render_template


MOCK_DATA = [{'id': 4699285, 'name': 'Photography Ideas',
              'cards': [{'id': 18688660, 'note': 'Test Note 1', 'updated_at': '2019-03-12T04:31:59Z'}]},
             {'id': 4699287, 'name': 'Shooting Finished',
              'cards': [{'id': 18688669, 'note': 'Test Note 2', 'updated_at': '2019-03-12T04:32:08Z'}]},
             {'id': 4699286, 'name': 'Editing In progress',
              'cards': [{'id': 18688672, 'note': 'Test Note 3', 'updated_at': '2019-03-12T04:32:13Z'}]},
             {'id': 4700591, 'name': 'Ready for Publish',
              'cards': [{'id': 18688676, 'note': 'Test Note 5', 'updated_at': '2019-03-12T04:32:24Z'},
                        {'id': 18688674, 'note': 'Test Note 4', 'updated_at': '2019-03-12T04:32:19Z'}]}]


@app.route('/')
def index():
    columns = get_columns()
    return render_template("index.html",
                           columns=columns)


def get_columns():
    columns = [{'id': x['id'],
                'name': x['name']}
               for x in
               gh('projects/{}/columns'.format(app.config['GITHUB_PROJECT']))]

    for column in columns:
        column['cards'] = [{'id': x['id'],
                            'note': x['title'],
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
