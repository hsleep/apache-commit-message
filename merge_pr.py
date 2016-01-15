#!/usr/bin/env python3
import netrc
from urllib.parse import urlparse

import github
import sys

OUTPUT = '''git checkout -b {label} {base}
git pull {repo} {branch}'''


def get_pull(url):
    github_id, _, token = netrc.netrc().authenticators('api.github.com')
    api = github.Github(github_id, token)

    parsed = urlparse(url)
    _, owner, repo, _, pr = parsed.path.split('/')
    repo = api.get_repo('{}/{}'.format(owner, repo))
    return repo.get_pull(int(pr))


def usage():
    print('Usage: {} <github pull request url>'.format(sys.argv[0]))
    sys.exit(-1)


# Input
#   - Pull request url
# Output
#   - Command for checkout new branch with PR
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()

    pull = get_pull(sys.argv[1])
    head = pull.head
    base = pull.base

    print(OUTPUT.format(label=head.label.replace(':', '-'), base=base.label.replace(':', '/'), repo=head.repo.clone_url,
                        branch=head.ref))
