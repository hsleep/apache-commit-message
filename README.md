# Apache Commit Message Generator

Writing a commit message for Apache project is very complicated to me. So, I have made this tool.
When you merge a pull request and write a commit message for it, just copy the url of the pull request. And run this script with the url.

Then a commit message is generated automatically. Just copy the message and use it.

## Usage

```sh
$ ./acm.py <github pull request url>
```

## Preliminary

Install python3

## Setup

1. Clone this repository.
	- `git clone https://github.com/hsleep/apache-commit-message.git`
2. Install requirements.
	- `pip3 install -r requirements.txt`
3. Append the authentication information for Github and Apache Jira into ~/.netrc.
4. Change file mode 600 `chmod 600 ~/.netrc`

### .netrc sample

```
machine api.github.com
  login <github id>
  password <github password or token>
machine issue.apache.org/jira
  login <jira id>
  password <jira password>
```

## Example

### Input

```
$ ./acm.py https://github.com/apache/incubator-s2graph/pull/1
```

### Output

```
[S2GRAPH-24] Add counter config for readonly graph

  S2GRAPH-24: Add counter config for readonly graph

JIRA:
  [S2GRAPH-24] https://issues.apache.org/jira/browse/S2GRAPH-24

Pull Request:
  Closes #1

Authors:
  Jaesang Kim jaesang@apache.org
```

## For OS X

Below command generate a commit message and copy it to the clipboard.

```
$ ./acm.py https://github.com/apache/incubator-s2graph/pull/1 | pbcopy
```
