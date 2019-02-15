import newspaper
import json

data = []

with open('categories_b.json') as json_categories:           
    categories = json.load(json_categories)


categories = ['https://www.diariovasco.com/']
for category in categories:
    dv_cat = newspaper.Source(category, language='es', request_timeout=10, number_threads=10, memoize_articles=False, keep_article_html=False)
    dv_cat.build()
    print(dv_cat.size())
    for article in dv_cat.articles:
        if((article.url.startswith(category)) and ("#" not in article.url)):
            print(article.url)
            # Try-Except-Continue will skip to the next article in the For loop if there is an exception
            try:
                article.download()
                article.parse()
            except:
                print('***FAILED TO DOWNLOAD***', article.url)
                continue

            print(article.url)
            item = {
            'date': article.publish_date,
            'url': article.url, 
            'author': article.authors,
            'title': article.title,
            'top_image': article.top_image,
            'text': article.text
            }
            data.append(item)

import csv
csv_columns = ['url','author','title','top_image','text','date']
csv_file = "data.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for d in data:
            writer.writerow(d)
except IOError:
    print("I/O error") 