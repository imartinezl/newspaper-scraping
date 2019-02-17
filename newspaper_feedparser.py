# -*- coding: utf-8 -*-
import feedparser
import html
import newspaper
import json
import flask
from flask_session import Session

def rssEntries(rss_url):
	d = feedparser.parse(rss_url);

	for i in range(len(d.entries)):
		d.entries[i].title =  html.unescape(d.entries[i].title);
		d.entries[i].summary =  html.unescape(d.entries[i].summary);
		d.entries[i]['downloaded'] = False;
		d.entries[i]['index'] = i;
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

@app.route('/<rss_id>')
def section(rss_id):
    try:
        rss_id = int(rss_id)
    except:
        return
    entries = rssEntries(rss_array[rss_id]['url'])
    flask.session["entries"] = entries;
    return flask.render_template('section.html', rss_array=rss_array, rss_id = rss_id, entries=entries)


@app.route('/<rss_id>/<entry_index>')
def article(rss_id, entry_index):
    try:
        rss_id = int(rss_id)
        i = int(entry_index)
    except:
        return 0

    entries = flask.session.get("entries")

    # Issue with some rss links
    url = entries[i].link
    if url.count('http') > 1 :
        entries[i].link = url[url.rfind('http'):]

    if not entries[i].downloaded:
        article = newspaper.Article(entries[i].link)
        print('***DOWNLOADING***', entries[i].link)
        try:
        	article.download()
        	article.parse()
        except:
        	print('***FAILED TO DOWNLOAD***', entries[i].link)
        	# del rss_data[rss_id].entries[i]
        	return 0
        entries[i].top_image = article.top_image
        entries[i].html = article.html
        entries[i].text = article.text
        entries[i]['downloaded'] = True
    else:
        print('***ALREADY DOWNLOADED***', entries[i].link)
    flask.session["entries"] = entries;

    return flask.render_template('article.html', rss_array=rss_array, entry=entries[i])


if __name__ == '__main__':
    app.run(debug=True, port=5000)