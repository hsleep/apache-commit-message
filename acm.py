#!/usr/bin/env python3

import netrc
import re
import sys
from urllib.parse import urlparse

import github
from jira import JIRA

OUTPUT = '''[{jira}] {title}

  {description}

JIRA:
  [{jira}] https://issues.apache.org/jira/browse/{jira}

Pull Request:
  Closes #{pr}

Authors:
  {authors}
'''


def get_pull(url):
    github_id, _, token = netrc.netrc().authenticators('api.github.com')
    api = github.Github(github_id, token)

    parsed = urlparse(url)
    _, owner, repo, _, pr = parsed.path.split('/')
    repo = api.get_repo('{}/{}'.format(owner, repo))
    return repo.get_pull(int(pr))


def make_commit_message(pull):
    return '\n  '.join(list(map(lambda c: c.commit.message, pull.get_commits())))


def make_authors(pull):
    return '\n  '.join(
            set(map(lambda c: '{} {}'.format(c.commit.author.name, c.commit.author.email), pull.get_commits())))


def get_issue(pull):
    # title to jira
    jira_id = re.search('[0-9A-Z]+-[0-9]+', pull.title).group(0)
    jira = JIRA('http://issues.apache.org/jira')
    return jira.issue(jira_id)


def usage():
    print('Usage: {} <github pull request url>'.format(sys.argv[0]))
    sys.exit(-1)

# Input
#   - PR Url
# Output
#   - Commit message
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()

    url = sys.argv[1]
    # urllib.request.Request(url)
    pull = get_pull(url)
    commit_msg = make_commit_message(pull)
    authors = make_authors(pull)
    issue = get_issue(pull)
    output_msg = OUTPUT.format(jira=issue.key, title=issue.fields.summary, description=commit_msg, pr=pull.number,
                               authors=authors)
    print(output_msg)
