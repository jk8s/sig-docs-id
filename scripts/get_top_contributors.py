#!/usr/bin/env python

from github import Github
import requests
import json
from collections import defaultdict

def get_pull_requests(page, state='merged', per_page=100):
  url = 'https://api.github.com/search/issues?q=type:pr+label:language/id+is:merged&sort=created&per_page=%s&page=%s' % (per_page, page)
  r = requests.get(url)
  return json.loads(r.content)['items']

def main():
  """
  Find the contributor list sorted by number of PRs

  ex:
    ./get_top_contributors.py
  """
  print('These are the top contributors to kubernetes.io/id, sorted based on number of PRs merged:')

  page_number = 1
  all_pull_requests = []
  pull_requests = get_pull_requests(page=page_number)
  while len(pull_requests) > 0:
    all_pull_requests += pull_requests
    page_number += 1
    pull_requests = get_pull_requests(page=page_number)

  contributions = defaultdict(int)
  for pull_request in all_pull_requests:
    contributions[pull_request['user']['login']] += 1

  sorted_contributions = sorted(contributions, key=contributions.get, reverse=True)
  for i, contributor in enumerate(sorted_contributions):
    print('%s. %s\t\t%s' % (i+1, contributor, contributions[contributor]))

  print('\nTotal number of PRs merged: %s' % (len(all_pull_requests)))

if __name__ == '__main__':
  main()
