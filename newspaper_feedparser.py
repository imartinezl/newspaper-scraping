# -*- coding: utf-8 -*-
import feedparser
d = feedparser.parse('https://www.diariovasco.com/rss/2.0/portada')

import html

import newspaper
for i in range(len(d.entries)):
	d.entries[i].title =  html.unescape(d.entries[i].title)
	# article = newspaper.Article(d.entries[i].link);
	# try:
	#     article.download()
	#     article.parse()
	# except:
	#     print('***FAILED TO DOWNLOAD***', article.url)
	#     del d.entries[i]
	#     continue
	# d.entries[i].text = article.text

from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
def base():
    return render_template('base.html', title='DV')

@app.route('/index')
def index():
    return render_template('index.html', title='DV', entries=d.entries)

if __name__ == '__main__':
    app.run(debug=True, port=5000)