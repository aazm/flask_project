#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import feedparser
from flask import Flask, render_template, redirect, url_for, request
from flask_caching import Cache

import logging,traceback,pdb

application = Flask(__name__)
cache = Cache(application, config={'CACHE_TYPE': 'simple'})
cache.init_app(application)

@application.route("/")
@cache.cached(timeout=120)
def homepage():
    items = {}
    upload(items)
    print items
    return render_template("welcome.html", items = items)



def upload(items):
    codes = ['9GAGDarkHumorNoGif', '9GAGGIF', '9GAGFunnyNoGif', '9GAGNSFW']
    #codes = ['9GAGDarkHumorNoGif']
    def process(code):
        try:
            url = 'https://9gag-rss.com/api/rss/get?code='+ code +'&format=2'
            feed = feedparser.parse(url)

            items[ url ] = []

            if feed:
                for entry in feed['entries']:
                    items[ url ].append({'id': entry[ 'id' ], 'val': entry[ 'summary_detail' ][ 'value' ]})


        except Exception as e:
            logging.exception('Failed to do something: ' + str(e))


    for code in codes:
        process(code)



if __name__ == "__main__":
    application.run(host=os.getenv('IP', '0.0.0.0'))