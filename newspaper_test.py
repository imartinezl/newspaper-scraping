import newspaper

data = []
url = 'https://www.diariovasco.com/'
dv_paper = newspaper.Source(url, language='es', request_timeout=10, number_threads=10, memoize_articles=False, keep_article_html=False)
dv_paper.build()
print(dv_paper.size())
for article in dv_paper.articles[1720:1750]:
    print(article.url)
    # url = 'https://www.diariovasco.com/economia/macroparque-eolico-siemens-asteasu-20190210001331-ntvo.html'
    # article = newspaper.Article(url)
    # Try-Except-Continue will skip to the next article in the For loop if there is an exception
    try:
        article.download()
    except ArticleException:
        continue
    article.parse()

    item = {
    'url': article.url, 
    'author': article.authors,
    'title': article.title,
    'top_image': article.top_image,
    'text': article.text,
    'date': article.publish_date
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