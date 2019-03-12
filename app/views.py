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
        column['cards'] = []
        for card_info in gh('projects/columns/{}/cards'.format(column['id'])):
            card = {'id': card_info['id'],
                    'updated_at': card_info['updated_at']}
            # Get issue info related to card
            issue_endpoint = card_info['content_url']
            issue = gh(issue_endpoint, full=True)
            card['note'] = issue['title']
            labels = [{'name': x['name'],
                       'color': x['color']}
                      for x in issue['labels']]
            card['labels'] = labels

            column['cards'].append(card)

    return columns


def gh(endpoint, full=False):
    if not full:
        endpoint = 'https://api.github.com/{}'.format(endpoint)
    headers = {
        'Accept': 'application/vnd.github.inertia-preview+json',
        'Authorization': 'token {}'.format(app.config['GITHUB_TOKEN']),
    }
    res = requests.get(endpoint, headers=headers)
    return res.json()
