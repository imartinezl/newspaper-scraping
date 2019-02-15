# -*- coding: utf-8 -*-
import feedparser
d = feedparser.parse('https://www.diariovasco.com/rss/2.0/portada')

import html

import newspaper
for i in range(len(d.entries)):
	d.entries[i].title =  html.unescape(d.entries[i].title)
	d.entries[i].summary =  html.unescape(d.entries[i].summary)
	d.entries[i]['downloaded'] = False
	d.entries[i]['index'] = i


from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
def base():
    return render_template('base.html', title='DV')

@app.route('/index')
def index():
    return render_template('index.html', title='DV', entries=d.entries)

@app.route('/index/<entry_index>')
def article(entry_index):
	j = int(entry_index)
	entry = d.entries[j]

	if not d.entries[j].downloaded:
		article = newspaper.Article(d.entries[j].link)
		print('***DOWNLOADING***', article.url)
		try:
			article.download()
			article.parse()
		except:
			print('***FAILED TO DOWNLOAD***', article.url)
			# del d.entries[j]
			return 0
		d.entries[j].top_image = article.top_image
		d.entries[j].text = article.text
		print(article.text)
		d.entries[j]['downloaded'] = True
	return render_template('article.html', title='DV', entry=d.entries[j])



if __name__ == '__main__':
    app.run(debug=True, port=5000)