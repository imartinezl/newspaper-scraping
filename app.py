import newspaper

data = []
url = 'https://www.diariovasco.com/'
dv_paper = newspaper.Source(url, language='es', request_timeout=10, number_threads=40, memoize_articles=False, keep_article_html=False)
dv_paper.build()
print(dv_paper.size())
for article in dv_paper.articles[0:10]:
    print(article.url)
    # url = 'https://www.diariovasco.com/economia/macroparque-eolico-siemens-asteasu-20190210001331-ntvo.html'
    # article = newspaper.Article(url)
    # Try-Except-Continue will skip to the next article in the For loop if there is an exception
    try:
        article.download()
    except ArticleException:
        continue
    article.parse()

    item = { 'url':article.url, 'author':article.authors,'title':article.title,
    'top_image':article.top_image,'text': article.text,'date': article.publish_date
    }
    data.append(item)

import json
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

url = 'https://www.diariovasco.com/'
dv_paper = newspaper.Source(url, language='es', request_timeout=10, number_threads=40, memoize_articles=False)
dv_paper.download()
dv_paper.parse()
dv_paper.set_categories()
dv_paper.download_categories()
dv_paper.parse_categories()
dv_paper.set_feeds()
dv_paper.download_feeds()
dv_paper.generate_articles()
print(dv_paper.size())


if(False):
    from flask import Flask
    from flask import render_template
    app = Flask(__name__)


    @app.route('/')
    def hello():
        return article.title

    @app.route('/index')
    def index():
        user = {'username': 'Miguel'}
        posts = [
            {
                'author': {'username': 'John'},
                'body': article.title
            },
            {
                'author': {'username': 'Susan'},
                'body': 'The Avengers movie was so cool!'
            }
        ]
        return render_template('index.html', title='Home', user=user, posts=posts)

    if __name__ == '__main__':
        app.run(debug=True, port=5000)





