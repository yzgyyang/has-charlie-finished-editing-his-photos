# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Enable the development environment
DEBUG = True

# Get GitHub Token
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

# GitHub Project Setting
GITHUB_PROJECT = '2307554'
