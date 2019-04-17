#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import argparse
import configparser
import re
import web_server
import gitclass


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', nargs='?')
    parser.add_argument('--review', action='store_true')
    return parser


def get_settings(config):
    settings = dict()
    for section in config.sections():
        value = dict()
        for setting in config[section]:
            value.update({setting: config.get(section, setting)})
        settings.update({section: value})
    return settings


def parse_mess(mess):
    try:
        name = mess['comment']['author']['displayName']
        comment = mess['comment']['body']
        issue = re.search(r'(?<=/issue/)\d+', mess['comment']['self']).group(0)
    except:
        print("Message parse error!")
        name, comment, issue = ("", "", "")
    return (name, comment, issue)


def review(settings):
    err = ""
    if settings.get('SERVER') and \
            settings.get('GIT') and \
            settings.get('RELATIONS'):
        if settings['SERVER'].get('host'):
            host = settings['SERVER'].get('host')
        else:
            host = ''
        if settings['SERVER'].get('port'):
            port = int(settings['SERVER'].get('port'))
        else:
            port = 1111
        if settings['GIT'].get('method') and settings['GIT'].get('url'):
            if settings['GIT']['method'] == 'OATH':
                if not (settings['GIT'].get('user') and settings['GIT'].get('pass')):
                    err = "Wrong git auth config!"
            elif settings['GIT']['method'] == 'TOKEN':
                if not settings['GIT'].get('token'):
                    err = "Wrong git auth config!"
            else:
                err = "Wrong method!"
    else:
        err = "Wrong config!"
    return (host, port, err)


def start_server(host, port, git, relations):
    Handler = web_server.Server
    try:
        gitapi = gitclass.Gitapi(git, relations)
    except:
        raise SystemExit("Error git connection!")
    with http.server.HTTPServer((host, port), Handler) as httpd:
        print("serving at port", port)
        while 1:
            request, client_address = httpd.get_request()
            mess = Handler(request, client_address, httpd).message
            request.close()
            if mess:
                if parse_mess(mess)[2]:
                    gitapi.edit(input=parse_mess(mess))
        httpd.server_close()


def main():
    parser = createParser()
    namespace = parser.parse_args()
    parser = configparser.ConfigParser()
    if namespace.conf:
        parser.read(namespace.conf)
    else:
        parser.read('config.conf')
    settings = get_settings(parser)
    host, port, err = review(settings)
    if err:
        raise SystemExit(err)
    if not namespace.review:
        start_server(host, port, settings['GIT'], settings['RELATIONS'])
    else:
        raise SystemExit("Good config!")


if __name__ == "__main__":
    main()
