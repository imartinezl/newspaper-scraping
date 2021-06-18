# -*- coding: utf-8 -*-
import feedparser
import html
import newspaper
import json
import flask
from flask_session import Session
from lxml.html import fromstring
import requests
import hashlib
import datetime

m = hashlib.md5()
def str2md5(text):
	m.update(text.encode())
	num = str(int(m.hexdigest(), 16))
	return num

def rssEntries(rss_url):
	print(rss_url)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	web_page = requests.get(rss_url, headers=headers)
	d = feedparser.parse(web_page.content) # rss_url

	for i in range(len(d.entries)):
		# Unescape title and summary
		d.entries[i].title =  html.unescape(d.entries[i].title)
		d.entries[i].summary =  html.unescape(d.entries[i].summary)

		# Generate md5 ID from title
		d.entries[i]['index'] = str2md5(d.entries[i].title)

		# Feature to cache downloaded articles
		d.entries[i]['downloaded'] = False

		# Date feature
		if d.entries[i].published:
			d.entries[i]['date'] = datetime.datetime.strptime(d.entries[i].published, '%a, %d %b %Y %H:%M:%S %z')
			d.entries[i]['date_text'] = d.entries[i]['date'].strftime("%Y-%m-%d %H:%M")
		
		# Extract text and img from summary
		summary = d.entries[i].summary
		if len(summary) > 0:
			doc = fromstring(summary)
			img_src = doc.xpath('//img/@src')
			if img_src:
				img_src = img_src[-1]
			d.entries[i]['imagen'] = img_src
			d.entries[i].summary = doc.text_content()
	return d.entries

# def getAllRss(rss_array):
#     rss_data = [];
#     print('***GETTING ALL ENTRIES***')
#     for rss in rss_array:
#         rss_data.append(rssEntries(rss['url']))
#     return rss_data
 
with open('rss_data.json') as rss_file:
    rss_array = json.load(rss_file)
# rss_data = getAllRss(rss_array);


app = flask.Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/')
def base():
    return flask.render_template('base.html', rss_array=rss_array)

@app.route('/<rss_title>')
def section(rss_title):
	rss_id = 0
	for i in range(len(rss_array)):
		if rss_array[i]['title'] == rss_title:
			rss_id = i
			break
	entries = rssEntries(rss_array[rss_id]['url'])
	flask.session["entries"] = entries
	return flask.render_template('section.html', rss_title=rss_title, rss_array = rss_array, entries=entries)


@app.route('/<rss_title>/<entry_index>')
def article(rss_title, entry_index):
	entries = flask.session.get("entries")

	entry_id = 0
	for i in range(len(entries)):
		if entries[i]['index'] == entry_index:
			entry_id = i
			break
	print("entry id =>", entry_id)
	# Issue with some rss links
	url = entries[entry_id].link
	if url.count('http') > 1 :
		entries[entry_id].link = url[url.rfind('http'):]

	if not entries[entry_id].downloaded:
		web_page = requests.get(entries[entry_id].link)
		article = newspaper.Article(entries[entry_id].link, verbose=True)
		print('***DOWNLOADING***', entries[entry_id].link)
		try:
			article.download()
			print('***DOWNLOADED***', article.download_state)
			article.parse()
		except:
			print('***FAILED TO DOWNLOAD***', entries[entry_id].link)
			return flask.render_template('base.html', rss_array=rss_array)
			# del rss_data[rss_id].entries[i]
			# return 0
		entries[entry_id].top_image = article.top_image
		entries[entry_id].html = article.html
		entries[entry_id].text = article.text
		entries[entry_id]['downloaded'] = True
	else:
		print('***ALREADY DOWNLOADED***', entries[entry_id].link)
	flask.session["entries"] = entries

	return flask.render_template('article.html', rss_array=rss_array, entry=entries[entry_id])


if __name__ == '__main__':
    app.run(debug=True, port=5000)