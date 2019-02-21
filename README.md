# newspaper-scraping

Open & free access to subscription-based regional newspaper through RSS + article scraping


### A bit of history

The [diariovasco](https://www.diariovasco.com/) is a regional newspaper from Gipuzkoa, in Spain.
The online version of the newspaper was open-access until 2017, but since then an over-priced subscription is mandatory. Even though we usually read the national news through other mediums, we were missing lots of info about local matters.

That is the reason why I set out to provide a open and free access to this regional newspaper.

### Overview

- [Feedparser](https://pythonhosted.org/feedparser/) python library for parsing RSS feed
- [Flask](http://flask.pocoo.org/) as web framework
- [Newspaper3k](https://newspaper.readthedocs.io/en/latest/) python library for extracting & curating articles
- [Heroku](https://www.heroku.com/) for python hosting + deployment

### In detail

RSS from the newspaper is used as the source of information. The sections of interest are indicated in the json file *rss_data.json*:
```json
[
{"url": "https://www.diariovasco.com/rss/2.0/?section=ultima-hora", "title":"Ultima Hora"},
{"url": "https://www.diariovasco.com/rss/2.0/?section=gipuzkoa","title":"Gipuzkoa"},
{"url": "https://www.diariovasco.com/rss/2.0/?section=san-sebastian","title":"San Sebastian"}
]
```

After importing this data, I set

The final webpage looks like this (very basic design, but functional):



