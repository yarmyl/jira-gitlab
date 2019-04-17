#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gitlab
import requests


class Gitapi:

    def __init__(self, auth, relations):
        self.__relations = relations
        if auth['method'] == "OATH":
            self.oath_auth(
                auth['url'],
                self.pass_auth(auth['url'], auth['user'], auth['pass'])
            )
        elif auth['method'] == "TOKEN":
            self.token_auth(auth['url'], auth['token'])

    def token_auth(self, url, token):
        self.gl = gitlab.Gitlab(url, private_token=token)
        self.url = url
        self.token = token
        self.gl.auth()

    def pass_auth(self, url, user, passwd):
        url += 'oauth/token' if url[-1] == '/' else '/oauth/token'
        data = 'grant_type=password&username=' + user + '&password=' + passwd
        r = requests.post(url, data=data)
        self.user = user
        self.passwd = passwd
        return r.json()['access_token']

    def oath_auth(self, url, token):
        self.gl = gitlab.Gitlab(url, oauth_token=token)
        self.url = url
        self.token = token
        self.gl.auth()

    def play(self, path, ref="master"):
        project = self.gl.projects.get(path)
        pipeline = project.pipelines.create({'ref': ref})

    def edit(self, input='', file='jira.file', ref='master'):
        try:
            relations = self.__relations[input[2]]
        except:
            print("Haven't relation", input[2])
            return
        arr = relations.split(',')
        if len(arr) > 0:
            path = arr[0]
            if len(arr) > 1:
                if arr[1]:
                    file = arr[1]
                if len(arr) > 2 and arr[2]:
                    ref = arr[2]
        try:
            project = self.gl.projects.get(path)
        except:
            print("Wrong path", path, "relation:", input[2])
            return
        try:
            f = project.files.get(file_path=file, ref=ref)
        except:
            print("Wrong filename or branchname relation:", input[2])
            return
        f.content = input[1]
        message = 'Updated from Jira API (' + input[0] + ')'
        f.save(branch=ref, commit_message=message)
