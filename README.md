# jira-gitlab

Issue <-> Project relation

## Install

```
pip3 install -r /app/requirements.txt
```

## Run

```
./jira-webhook.py
```
### Keys:
* *--review* - review config;
* *--conf* - config file.

## Config

### [SERVER]

* **HOST** - listen IP-address;
* **PORT** - listen port;

### [GIT]

* **METHOD** - gitlab api method **OATH** or **TOKEN**;
* **URL** - gitlab api url;
* **USER** - username if **OATH** method;
* **PASS** - password if **OATH** method;
* **TOKEN** - private token if **TOKEN** method.

### [RELATIONS]

\<JIRA ISSUE\>=\<PATH\>[,\<FILE\>][,\<BRANCH\>]

Example:

10108=root/test,,master

## [JIRA]

In Jira add webhook https://developer.atlassian.com/server/jira/platform/webhooks/

## [GitLab]
